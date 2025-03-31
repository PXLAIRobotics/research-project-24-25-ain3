import networkx as nx

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

G.add_edge("Corda 9", "Corda 1", weight=393) #weight = afstand
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


def heuristic(source, destination):
    pos_source = G.nodes[source]["pos"]
    pos_destination = G.nodes[destination]["pos"]
    return ((pos_source[0] - pos_destination[0]) ** 2 + (pos_source[1] - pos_destination[1]) ** 2) ** 0.5 # euclidische afstand

# A* algoritme voor pathfinding
def calculate_path(start, destination):
    path = nx.astar_path(G, source=start, target=destination, weight="weight", heuristic=heuristic)

    total_distance = 0
    for i in range(len(path) - 1):
        edge_weight = G[path[i]][path[i + 1]]["weight"]
        total_distance += edge_weight
    
    path_string = " -> ".join(path)
    return {"path": path_string, "total_distance": str(total_distance) + " meters"}


result = calculate_path("Bushalte", "Corda 9")
print(result)
