from aresta import Aresta

class Vertice:
    def __init__(self, id_vertice, email):
        self.id = id_vertice
        self.informacao = email
        self.adjacencias = []

    def adicionar_ou_incrementar_adjacencia(self, destino, peso=1):
        for aresta in self.adjacencias:
            if aresta.destino == destino:
                aresta.peso += peso
                return
            
        self.adjacencias.append(Aresta(destino, peso))