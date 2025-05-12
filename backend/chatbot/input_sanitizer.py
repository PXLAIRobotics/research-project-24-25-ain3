import re
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import os

# Set cache path (must match Dockerfile ENV)
os.environ['HF_HOME'] = '/app/.cache/huggingface'

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Sentiment analysis function
def robbert_sentiment_analysis(message: str):
    # Tokenize the message
    inputs = tokenizer(message, return_tensors="pt", truncation=True, padding=True)
    
    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the probabilities for the 5 sentiment labels (very negative, negative, neutral, positive, very positive)
    probs = F.softmax(outputs.logits, dim=1)
    
    # Get the label index with the highest probability
    sentiment_class = torch.argmax(probs).item()
    
    # Define the labels for the sentiment classes
    sentiment_labels = ["zeer negatief", "negatief", "neutraal", "positief", "zeer positief"]
    
    # Get the sentiment label for the predicted sentiment
    sentiment_label = sentiment_labels[sentiment_class]
    
    # Get the confidence (probability) of the predicted label
    confidence = probs[0][sentiment_class].item()

    # If the sentiment is negative, return a warning
    if sentiment_label == "negatief" or sentiment_label == "zeer negatief" and confidence >= 0.37:
        return (
            f"⚠️ Bericht gedetecteerd als negatief of onbeleefd. "
            f"(Label: {sentiment_label}, Vertrouwen: {confidence:.2f}). "
            "Gelieve je boodschap beleefder te formuleren."
        )

    return None

    
#Tokenization betekent message in kleine delen splitsen, ontology is kijken of die delen dan overeenkomen met foute categorien of woorden
def tokenization_with_ontology(message):
    """
    Controleer op verdachte tokens die duiden op injectie, scripting of command attempts.
    Returnt een waarschuwing indien gevonden, anders None.
    """
    tokens = re.findall(r'\b\w+\b', message.lower())

    ontology = {
    "injection_attack": [
        "drop", "delete", "insert", "update", "alter", "shutdown", "truncate",
        "exec", "union", "select", "from", "where", "or", "and", "--", ";", "'", "\"",
        "sleep", "benchmark", "xp_cmdshell", "load_file", "outfile"
    ],
    "system_commands": [
        "system", "os", "eval", "exec", "compile", "input", "open", "read", "write",
        "subprocess", "popen", "getenv", "setenv", "fork", "kill", "signal", "thread", 
        "pickle", "marshal", "socket", "openai.api_key"
    ],
    "security": [
        "admin", "root", "access", "control", "privilege", "security", "token",
        "auth", "authorization", "authentication", "apikey", "password", "credentials",
        "user", "users", "permission", "login", "logout", "session"
    ],
    "malicious_activity": [
        "hack", "hacker", "exploit", "reverse", "ddos", "attack", "malware",
        "trojan", "worm", "keylogger", "spyware", "botnet", "virus", "backdoor",
        "ransomware", "rootkit", "payload"
    ],
    "phishing_keywords": [
        "phish", "phishing", "fake", "email", "click", "link", "http", "https",
        "login", "account", "reset", "verify", "update", "confirm", "bank", "urgent",
        "attachment", "invoice", "document"
    ],
    "vuln_exploit": [
        "buffer", "overflow", "heap", "stack", "format", "vuln", "vulnerability",
        "cve", "cwe", "rce", "lfi", "rfi", "sqli", "xss", "csrf", "deserialization",
        "injection", "sandbox", "bypass", "privilege", "zero-day"
    ]
    }


   
    # Check voor verdachte woorden in de ontology
    for category, keywords in ontology.items():
        for token in tokens:
            if token in keywords:
                return (
                    f"🛑⚠️ \nDe input bevat een verdacht woord: '{token}' (categorie: {category}). "
                    "Om veiligheidsredenen wordt deze invoer niet verwerkt. "
                    "Gelieve je vraag op een veilige en normale manier te formuleren."
                )
    return None


#Het onderwerp van een chat bepalen
def preprocess_text(text, stop_words):
    # Tokenize the text
    tokens = nltk.word_tokenize(text.lower())
    # Remove stopwords
    cleaned = [word for word in tokens if word not in stop_words]
    return cleaned

def topic_modelling(history):
    stop_words = set(stopwords.words('dutch') + stopwords.words('english'))

    # Als history een enkele string is, zet het dan om naar een lijst
    if isinstance(history, str):
        history = [history]

    # Verwerk de tekst voor stopwoordenverwijdering en tokenisatie
    cleaned = [
        ' '.join(preprocess_text(msg, stop_words))
        for msg in history
    ]

    if not any(cleaned):
        return None  # Geen bruikbare tekst

    suspicious_topic_keywords = {
    "security threat": [
        "attack", "bomb", "hack", "malware", "exploit", "breach", "ddos", "ransomware",
        "trojan", "worm", "virus", "rootkit", "payload", "spyware", "threat", "infiltrate"
    ],
    "admin abuse": [
        "admin", "sudo", "access", "backdoor", "root", "privilege", "escalation",
        "superuser", "bypass", "login", "credentials"
    ],
    "phishing": [
        "verify", "account", "password", "bank", "click", "link", "email", "login", "urgent",
        "reset", "security", "suspicious", "credential", "phishing", "update"
    ],
    "vulnerability exploit": [
        "xss", "csrf", "sqli", "lfi", "rfi", "zero-day", "heap", "overflow", "buffer",
        "cve", "cwe", "injection", "sandbox", "token", "auth"
    ],
    "scripting/system abuse": [
        "eval", "exec", "subprocess", "os", "system", "bash", "shell", "script", "command",
        "run", "terminal", "input", "output", "compile"
    ]
}

    # Vectoriseer de teksten (met stopwoorden verwijderd)
    vectorizer = CountVectorizer(max_df=1.0, min_df=1)
    doc_term_matrix = vectorizer.fit_transform(cleaned)

    # Voer LDA uit om de topics te identificeren
    lda = LatentDirichletAllocation(n_components=5, random_state=42)
    lda.fit(doc_term_matrix)

    terms = vectorizer.get_feature_names_out()
    for idx, topic in enumerate(lda.components_):
        topic_keywords = [terms[i] for i in topic.argsort()[:-6:-1]]
        print(f"🔍 Topic {idx}: {topic_keywords}") 
        for category, keywords in suspicious_topic_keywords.items():
            if any(word in topic_keywords for word in keywords):
                return (
                    f"⚠️ Verdacht onderwerp gedetecteerd in de conversatie (categorie: '{category}'). "
                    "Je verzoek wordt niet verwerkt en uit voorzorg sluiten we deze conversatie."
                )
    
    return None 

