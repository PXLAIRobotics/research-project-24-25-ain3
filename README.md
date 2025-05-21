# Research Project 24-25: Team 3

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/vvTTilrq)

## Overzicht
Dit project maakt deel uit van het Researchproject van team 3 voor het academiejaar 2024-2025. Het doel is om VIBE te ontwikkelen: een AI-gestuurde assistent met geavanceerde padplanning-algoritmes, geïntegreerd in een functionele webapplicatie.

De applicatie bestaat uit een Vue.js frontend, een Python FastAPI backend en maakt gebruik van Docker voor eenvoudige ontwikkeling en deployment.

---

## Kenmerken
- **Vue.js Frontend**: Interactieve gebruikersinterface die draait op GitHub Pages (https://pxlairobotics.github.io/research-project-24-25-ain3/).  
- **Python FastAPI Backend**: Verwerkt padvindverzoeken en communiceert met de frontend.  
- **Database**: Wordt gehost op AWS (RDS PostgreSQL).  
- **Dockerized**: Backend draait lokaal in een Docker container.  
- **CI/CD**: GitHub Actions draaien backend- en frontendtests en deployen de frontend automatisch bij pushes naar `main` en pull requests.  
- **Model**: Gebaseerd op GPT-4o-mini, met geavanceerde pathplanning-algoritmes.  

---

## Technologieën
- Frontend: Vue.js, JavaScript, HTML, CSS  
- Backend: Python, FastAPI  
- Database: PostgreSQL (AWS RDS)  
- Containerisatie: Docker, Docker Compose  
- CI/CD: GitHub Actions  
- Versiebeheer: Git, GitHub  

---

## Installatie en Setup

### Vereisten
- Docker en Docker Compose (voor backend container).  
- Python 3.x (voor lokaal ontwikkelen en testen backend).  
- Node.js & npm (voor frontend ontwikkeling en testen).  
- [Ngrok](https://ngrok.com/) (voor extern publiekelijk toegankelijk maken van je backend).

---

### Ngrok installeren en gebruiken

1. Download en installeer ngrok via https://ngrok.com/download.  
2. Voeg ngrok toe aan je systeem PATH zodat je het overal kunt aanroepen vanuit de terminal.  
3. Maak een account aan bij ngrok en configureer een static domain (optioneel, maar aanbevolen voor een vast adres).  
4. Start ngrok met je static domain en verbind deze met poort 8000, bijvoorbeeld:  
   ```bash
   ngrok http --url=your-static-subdomain.ngrok-free.app 8000
5. Gebruik de verkregen ngrok URL in je frontend om API calls naar de backend te maken.

---

### Backend lokaal draaien

1. Clone de repository:
   ```bash
   git clone https://github.com/PXLAIRobotics/research-project-24-25-ain3.git
   cd research-project-24-25-ain3/backend
   ```
2. Zorg dat je .env-bestand in de root van de repository staat met de juiste AWS database credentials en API keys.
3. Start de backend met het script:
   ```bash
   ./start_backend.sh
   ```
   Dit script bouwt en start de Docker container met de backend en eventueel ngrok.
4. De backend is nu bereikbaar op http://localhost:8000 lokaal, en via ngrok op je static domain.

---

## Frontend

De frontend is live en wordt gehost via GitHub Pages op:
https://pxlairobotics.github.io/research-project-24-25-ain3/

De frontend maakt verbinding met de backend via de publieke ngrok URL of een andere tunneling service.

---

## Tests & CI/CD
Zowel de backend als frontend bevatten unit- en integratietests.

GitHub Actions zijn opgezet om:

- Backend- en frontendtests automatisch uit te voeren bij elke push en pull request naar `main`.
- De frontend automatisch te bouwen en te deployen naar GitHub Pages bij wijzigingen in `main`.

---

## Gebruik
- Start backend lokaal met `./start_backend.sh`.
- Open de frontend in je browser via de GitHub Pages URL.
- Zorg dat de frontend de juiste publieke backend URL gebruikt (ngrok static domain) voor API-aanroepen.

---

## Erkenningen
PXLAI Robotics, Sam & Sam voor het mentorschap en kader.

Bijdragers:

- @AbdulrahmanAkilPXL
- @XanderThijsPXL
- @MilanFreesPXL
- @SenneReekmansPXL