import networkx as nx
import hashlib
import requests
import os
import json
from geopy.distance import geodesic

# Lees coördinaten uit geo.json
with open("geo.json") as f:
    data = json.load(f)

nodes = {}
for feature in data["features"]:
    name = feature["properties"]["name"]
    lon, lat = feature["geometry"]["coordinates"]
    nodes[name] = (lat, lon)

# Maak graaf en voeg knopen toe
g = nx.Graph()
for name, (lat, lon) in nodes.items():
    g.add_node(name, pos=(lat, lon))

# Lijst met verbindingen (edges)
edge_list = [
    ("A", "Ab"),
    ("Ab", "ingang corda bar"),
    ("ingang corda bar", "corda bar"),
    ("A", "Aba"),
    ("Aba", "ingang corda 1"),
    ("ingang corda 1", "corda 1"),
    ("A", "Ac"),
    ("Ac", "Aca"),
    ("Aca", "corda 1"),
    ("Aca", "B"),
    ("B", "ingang corda 2"),
    ("ingang corda 2", "corda 2"),
    ("B", "Ba"),
    ("Ba", "Baa"),
    ("Baa", "ingang corda 1"),
    ("A",  "Ad"),
    ("Ad", "C"),
    ("A", "Ae"),
    ("Ae","D"),
    ("D", "Ca"),
    ("D", "corda 5 ingang"),
    ("corda 5 ingang", "corda 5"),
    ("C","Ca"),
    ("Ca", "corda 5 ingang"),
    ("corda 5 ingang", "corda 5"),
    ("C","Cb"),
    ("Cb","Cba"),
    ("Cba", "corda 2"),
    ("Cba","Cbb"),
    ("Cbb", "corda 3"),
    ("C", "Cc"),
    ("Cc", "Ccb"),
    ("Cc", "Cca"),
    ("Cca","Ccc"),
    ("Ccb","Ccc"),
    ("Cca", "corda 4"),
    ("Ccaa", "corda 4"),
    ("Ccaa", "Cca"),
    ("D", "ingang 6a a"),
    ("ingang 6a a", "corda 6"),
    ("Ae","Aea"),
    ("corda 6a b","Aea"),
    ("corda 6", "corda 6a b"),
    ("Aea", "F"),
    ("F","corda 7 ingang"),
    ("corda 7 ingang","E"),
    ("corda 7 ingang","corda 7"),
    ("E","Ea"),
    ("E","Eb"),
    ("Eb","Eba"),
    ("Eba", "corda 9 i"),
    ("corda 9 i","corda 9"),
    ("bushalte", "G"),
    ("G","Ga"),
    ("Ga","D")
]

# Voeg edges toe met geodetische afstand als gewicht
for u, v in edge_list:
    pos_u = g.nodes[u]['pos']
    pos_v = g.nodes[v]['pos']
    distance = geodesic(pos_u, pos_v).meters
    g.add_edge(u, v, weight=distance)


def generate_map(start, destination, api_key, path):
    import json
    import urllib.parse

    start_coords = g.nodes[start]['pos']
    destination_coords = g.nodes[destination]['pos']

    # Prepare GeoJSON LineString (lon,lat)
    geojson = {
        "type": "LineString",
        "coordinates": [
            (lon, lat) for lat, lon in [g.nodes[node]['pos'] for node in path]
        ]
    }

    geojson_encoded = urllib.parse.quote(json.dumps(geojson))
    start_marker = f"pin-s-a+000000({start_coords[1]},{start_coords[0]})"
    end_marker = f"pin-s-b+ff0000({destination_coords[1]},{destination_coords[0]})"

    center_lat = (start_coords[0] + destination_coords[0]) / 2
    center_lon = (start_coords[1] + destination_coords[1]) / 2

    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"
        f"geojson({geojson_encoded}),{start_marker},{end_marker}/"
        f"{center_lon},{center_lat},15/800x600"
        f"?access_token={api_key}"
    )
    path_hash = hashlib.md5("->".join(path).encode()).hexdigest()
    filename = f"map_{path_hash}.png"

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "project", "public", "maps")
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)
    if os.path.exists(full_path):
        os.remove(full_path)

    response = requests.get(url)
    if response.status_code == 200:
        with open(full_path, "wb") as img:
            img.write(response.content)
        return f"/public/maps/{filename}"
    else:
        raise Exception(f"Failed to fetch map: {response.status_code}")


def heuristic(u, v):
    pos_u = g.nodes[u]['pos']
    pos_v = g.nodes[v]['pos']
    # Eenvoudige Euclidische heuristiek
    return ((pos_u[0] - pos_v[0])**2 + (pos_u[1] - pos_v[1])**2)**0.5


def calculate_path(start, destination):
    api_key = "pk.eyJ1IjoiZmFzdGFtZXJyYSIsImEiOiJjbThzbHlzZmIwMWlsMm1zZDIwcWZtYmprIn0.NnOKCTjBJfavxl9n9KNDig"

    mapping = {loc.lower(): loc for loc in g.nodes}
    s = start.lower().strip()
    d = destination.lower().strip()
    if s not in mapping or d not in mapping:
        raise ValueError("Onbekende locatie.")

    start_node = mapping[s]
    dest_node = mapping[d]

    path = nx.astar_path(g, start_node, dest_node, weight='weight', heuristic=heuristic)
    image = generate_map(start_node, dest_node, api_key, path)

    total = sum(
        g[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)
    )
    return {
        'path': ' -> '.join(path),
        'total_distance': f"{total:.1f} meter",
        'start_node': start_node,
        'destination_node': dest_node,
        'image_path': image
    }
