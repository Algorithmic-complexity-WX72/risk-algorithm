import csv
import random
import graphviz
from collections import defaultdict

def generar_grafo(csv_file, total_nodes):
    G = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        lines = [line for line in reader if len(line) >= 2]
        lines = random.sample(lines, total_nodes)
        
        for line in lines:
            node_name, _ = line
            G[node_name] = {}
        
        for i in range(len(lines)):
            for j in range(i+1, len(lines)):
                distance = random.randint(1, 20)
                G[lines[i][0]][lines[j][0]] = distance
                #G[lines[j][0]][lines[i][0]] = distance
    
    return G

def dibujar_grafo(G, nombre_archivo='grafo'):
    dot = graphviz.Graph()
    
    for node in G:
        dot.node(node)
        
    for node in G:
        for neighbor, weight in G[node].items():
            dot.edge(node, neighbor, label=str(weight))
    
    dot.render(nombre_archivo, format='svg', view=True)

def dijkstra(G, inicio, destino):
    distancias = {nodo: float('inf') for nodo in G}
    distancias[inicio] = 0
    caminos = {nodo: [] for nodo in G}
    visitados = set()

    while len(visitados) < len(G):
        no_visitados = {nodo: distancias[nodo] for nodo in G if nodo not in visitados}
        if not no_visitados:
            break
        nodo_actual = min(no_visitados, key=no_visitados.get)
        visitados.add(nodo_actual)

        for vecino, peso in G[nodo_actual].items():
            nueva_distancia = distancias[nodo_actual] + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                caminos[vecino] = caminos[nodo_actual] + [nodo_actual]
    
    return distancias, caminos

def dibujar_grafo_con_camino(G, caminos, destino, nombre_archivo='grafo_coloreado'):
    dot = graphviz.Digraph()
    
    for node in G:
        dot.node(node)
        
    camino = caminos[destino] + [destino]
    
    camino_set = set(zip(camino, camino[1:]))
    
    for node in G:
        for neighbor, weight in G[node].items():
            if (node, neighbor) in camino_set or (neighbor, node) in camino_set:
                dot.edge(node, neighbor, label=str(weight), color='red', penwidth='2')
            else:
                dot.edge(node, neighbor, label=str(weight))
    
    dot.render(nombre_archivo, format='svg', view=True)

dataset = "names.csv"
nodos_totales = 6
mapa = generar_grafo(dataset, nodos_totales)

dibujar_grafo(mapa)

nodo_origen = input("Introduce el planeta de origen: ")
nodo_destino = input("Introduce el planeta de destino: ")
distancias, caminos = dijkstra(mapa, nodo_origen, nodo_destino)

if nodo_destino in caminos:
    ruta = ' -> '.join(caminos[nodo_destino] + [nodo_destino])
    distancia = distancias[nodo_destino]
    print(f"El camino más corto desde {nodo_origen} a {nodo_destino} es: {ruta} (Distancia: {distancia})")
else:
    print(f"No hay un camino válido desde {nodo_origen} a {nodo_destino}")

dibujar_grafo_con_camino(mapa, caminos, nodo_destino)
