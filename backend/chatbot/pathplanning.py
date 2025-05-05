import networkx as nx

import folium
import requests
import os
import urllib.parse




G = nx.Graph()

G.add_node("Corda 1", pos=(50.95172313144371, 5.352094844226686)) # pos = coordinaten
G.add_node("Corda 2", pos=(50.951626678583736, 5.351265521695136))
G.add_node("Corda 3", pos=(50.95165882955858, 5.350433009461545))
G.add_node("Corda 4", pos=(50.95200595607143, 5.350126082209007))
G.add_node("Corda 5", pos=(50.952752101243064, 5.350403954268296))
G.add_node("Corda 6", pos=(50.95302491524673, 5.351816284225618))
G.add_node("Corda 7", pos=(50.95335244240987, 5.353433463162143))
G.add_node("Corda 8", pos=(50.95383267745878, 5.353749243664546))
G.add_node("Corda 9", pos=(50.953402505567155, 5.356952211206652))
G.add_node("Corda A", pos=(50.953440154061774, 5.351114049143033))
G.add_node("Corda B", pos=(50.953616977248466, 5.351946561376623))
G.add_node("Corda C", pos=(50.95379580911118, 5.352728038377514))
G.add_node("Corda D", pos=(50.95434636579674, 5.3534233934232))
G.add_node("Corda bar", pos=(50.95249971666138, 5.352156110611767))
G.add_node("Bushalte", pos=(50.952629250889025, 5.348729340739601))
G.add_node("Treinstation", pos=(50.95451179958787, 5.349206509818355))

G.add_edge("Corda 9", "Corda 1", weight=393) 
G.add_edge("Corda 1", "Corda 2", weight=60)
G.add_edge("Corda 2", "Corda 3", weight=57)
G.add_edge("Corda 3", "Corda 4", weight=50)
G.add_edge("Corda 4", "Corda 5", weight=75)
G.add_edge("Corda 5", "Bushalte", weight=90)
G.add_edge("Corda 5", "Treinstation", weight=218)
G.add_edge("Corda 5", "Corda A", weight=112)
G.add_edge("Corda 4", "Corda bar", weight=150)
G.add_edge("Corda 2", "Corda bar", weight=112)
G.add_edge("Corda 1", "Corda bar", weight=85)
G.add_edge("Corda A", "Corda 6", weight=64)
G.add_edge("Corda A", "Corda B", weight=64)
G.add_edge("Corda B", "Corda 6", weight=54)
G.add_edge("Corda B", "Corda C", weight=60)
G.add_edge("Corda 7", "Corda bar", weight=132)
G.add_edge("Corda C", "Corda D", weight=90)
G.add_edge("Corda D", "Corda 8", weight=59)
G.add_edge("Corda C", "Corda 8", weight=67)
G.add_edge("Corda 7", "Corda 8", weight=58)
G.add_edge("Corda 8", "Corda 9", weight=233)


def generate_map(start, destination, api_key, path):
    import json
    import urllib.parse

    start_coords = G.nodes[start]['pos']
    destination_coords = G.nodes[destination]['pos']

    # Prepare GeoJSON LineString (coords in lon,lat order)
    geojson = {
        "type": "LineString",
        "coordinates": [(lon, lat) for lat, lon in [G.nodes[node]['pos'] for node in path]]
    }

    # Encode GeoJSON as URL-safe string
    geojson_encoded = urllib.parse.quote(json.dumps(geojson))

    # Markers
    start_marker = f"pin-s-a+000000({start_coords[1]},{start_coords[0]})"
    end_marker = f"pin-s-b+ff0000({destination_coords[1]},{destination_coords[0]})"

    # Center the map
    center_lat = (start_coords[0] + destination_coords[0]) / 2
    center_lon = (start_coords[1] + destination_coords[1]) / 2

    # Final URL with geojson overlay
    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"
        f"geojson({geojson_encoded}),{start_marker},{end_marker}/"
        f"{center_lon},{center_lat},15/800x600"
        f"?access_token={api_key}"
    )

    print("Generated Mapbox URL:", url)

    # Save image
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.abspath(os.path.join(script_dir, "..", "project", "public", "maps"))
    os.makedirs(output_path, exist_ok=True)
    full_map_path = os.path.join(output_path, "map.png")

    print("Saving map to:", full_map_path)

    response = requests.get(url)
    if response.status_code == 200:
        with open(full_map_path, "wb") as f:
            f.write(response.content)
        return "/maps/map.png"
    else:
        raise Exception(f"Failed to fetch map: {response.status_code}, {response.text}")

def heuristic(source, destination):
    pos_source = G.nodes[source]["pos"]
    pos_destination = G.nodes[destination]["pos"]
    return ((pos_source[0] - pos_destination[0]) ** 2 + (pos_source[1] - pos_destination[1]) ** 2) ** 0.5 # euclidische afstand

# A* algoritme voor pathfinding
def calculate_path(start, destination):
    # Mapping van lowercase naar echte node namen
    api_key = "pk.eyJ1IjoiZmFzdGFtZXJyYSIsImEiOiJjbThzbHlzZmIwMWlsMm1zZDIwcWZtYmprIn0.NnOKCTjBJfavxl9n9KNDig"



    location_mapping = {loc.lower(): loc for loc in G.nodes}

    start_normalized = start.lower().strip()
    destination_normalized = destination.lower().strip()

    if start_normalized not in location_mapping or destination_normalized not in location_mapping:
        raise ValueError("Onbekende locatie.")

    start_node = location_mapping[start_normalized]
    destination_node = location_mapping[destination_normalized]

    path = nx.astar_path(G, source=start_node, target=destination_node, weight="weight", heuristic=heuristic)

    image_path = generate_map( start, destination,api_key, path)
    total_distance = 0
    for i in range(len(path) - 1):
        edge_weight = G[path[i]][path[i + 1]]["weight"]
        total_distance += edge_weight

    path_string = " -> ".join(path)

    # Return netjes geformatteerd: echte nodes (start_node en destination_node)
    return {"path": path_string, "total_distance": str(total_distance) + " meter", "start_node": start_node, "destination_node": destination_node, "image_path" : image_path}
