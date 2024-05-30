import csv
import random
import networkx as nx
import matplotlib.pyplot as plt

def generar_grafo(csv_file, total_nodes):
    G = nx.Graph()
    # Leer el archivo CSV y seleccionar nodos aleatorios
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        lines = random.sample(list(reader), total_nodes)
        
        # Agregar nodos al grafo
        for line in lines:
            node_name, _ = line
            G.add_node(node_name)
        
        # Asignar distancias aleatorias entre nodos
        for i in range(len(lines)):
            for j in range(i+1, len(lines)):
                distance = random.randint(10, 20)
                G.add_edge(lines[i][0], lines[j][0], weight=distance)
    
    return G

def dibujar_grafo(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


dataset = "names.csv" 
#nota: dejar el mapa en 5 nodos porque con más se ve muy desordenado
nodos_totales = 5
mapa = generar_grafo(dataset, nodos_totales)
dibujar_grafo(mapa)