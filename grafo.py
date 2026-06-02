import random
import heapq
from collections import deque
from vertice import Vertice

class Grafo:
    def __init__(self):
        self.vertices = []
        self.rotulo_para_id = {}
        self.num_vertices = 0

    def obter_ou_criar_vertice(self, rotulo):
        if rotulo not in self.rotulo_para_id:
            novo_id = self.num_vertices
            self.rotulo_para_id[rotulo] = novo_id
            self.vertices.append(Vertice(novo_id, rotulo))
            self.num_vertices += 1
        return self.rotulo_para_id[rotulo]

    def adicionar_aresta(self, origem, destino, peso=1):
        id_origem = self.obter_ou_criar_vertice(origem)
        id_destino = self.obter_ou_criar_vertice(destino)
        self.vertices[id_origem].adicionar_ou_incrementar_adjacencia(id_destino, peso)

    # SALVAR PAJEK
    def salvar_pajek(self, caminho_arquivo):
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(f"*Vertices {self.num_vertices}\n")
            for v in self.vertices:
                f.write(f'{v.id + 1} "{v.informacao}"\n')
            
            f.write("*Arcs\n")  # Direcionadas
            for v in self.vertices:
                for a in v.adjacencias:
                    f.write(f"{v.id + 1} {a.destino + 1} {a.peso}\n")
    # CARREGAR PAJEK
    def carregar_pajek(self, caminho_arquivo):
        self.__init__() # Limpa grafo
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
        modo = None
        for linha in linhas:
            linha = linha.strip()
            if not linha: continue
            
            if linha.lower().startswith("*vertices"):
                modo = "vertices"
                continue
            elif linha.lower().startswith("*arcs") or linha.lower().startswith("*edges"):
                modo = "arestas"
                continue
                
            if modo == "vertices":
                partes = linha.split(' ', 1)
                if len(partes) > 1:
                    rotulo = partes[1].replace('"', '')
                    self.obter_ou_criar_vertice(rotulo)
                    
            elif modo == "arestas":
                partes = linha.split()
                if len(partes) >= 2:
                    # Pajek salva usando base 1, subtraímos 1 para voltar ao padrão do Python (que começa no índice 0)
                    idx_origem = int(partes[0]) - 1
                    idx_destino = int(partes[1]) - 1
                    peso = float(partes[2]) if len(partes) > 2 else 1
                    
                    origem = self.vertices[idx_origem].informacao
                    destino = self.vertices[idx_destino].informacao
                    self.adicionar_aresta(origem, destino, peso)

    # CONEXO
    # Conexo se não existirem pontos isoladas
    def is_conexo(self):
        if self.num_vertices == 0: return False
        return len(self.componentes_conectados()) == 1

    # EULERIANO
    # Um grafo é euleriano se for possível dar a volta em TODAS as arestas da rede sem repetir nenhuma e terminar onde começou.
    def is_euleriano(self):
        if not self.is_conexo():
            return False # Se tiver ponto isolado, não é euleriano.
            
        grau_entrada = [0] * self.num_vertices
        grau_saida = [0] * self.num_vertices
        
        # Conta quantas setas saem e entram em cada artista
        for v in self.vertices:
            grau_saida[v.id] = len(v.adjacencias)
            for a in v.adjacencias:
                grau_entrada[a.destino] += 1
                
        # Se um único artista tiver entrada diferente de saída, não é Euleriano.
        for i in range(self.num_vertices):
            if grau_entrada[i] != grau_saida[i]:
                return False
        return True

    # CICLICO
    # Um grafo é cíclico se tiver pelo menos um ciclo (loop de pagamentos). Se não tiver nenhum ciclo, é acíclico (ex: uma cadeia linear onde A paga B, B paga C, mas C não paga ninguém).
    def is_ciclico(self):
        # DFS (Busca em Profundidade)
        visitados = [False] * self.num_vertices
        pilha_recursao = [False] * self.num_vertices

        def dfs_ciclo(v):
            visitados[v] = True
            # Marca o nó como "estamos no meio do caminho passando por ele"
            pilha_recursao[v] = True 
            
            for a in self.vertices[v].adjacencias:
                viz = a.destino
                if not visitados[viz]:
                    if dfs_ciclo(viz): return True
                # Se batermos em um vizinho que já está na pilha do caminho atual, achamos um ciclo!
                elif pilha_recursao[viz]:
                    return True
                    
            # Tira o nó da pilha ao terminar de explorar as ramificações dele
            pilha_recursao[v] = False
            return False

        # Tenta achar ciclos partindo de todos os nós (caso o grafo seja desconexo)
        for i in range(self.num_vertices):
            if not visitados[i]:
                if dfs_ciclo(i): return True
        return False

    def componentes_conectados(self):
        # Identifica pontos na rede (Componentes Fracamente Conectados), ignorando o sentido das setas (trata como rua de mão dupla) para ver quem faz parte do mesmo grupo. 
        # BFS (Busca em Largura).

        # Cria uma versão temporária da rede onde toda rua tem mão dupla
        adj_bidi = [[] for _ in range(self.num_vertices)]
        for v in self.vertices:
            for a in v.adjacencias:
                adj_bidi[v.id].append(a.destino)
                adj_bidi[a.destino].append(v.id) # volta
                
        visitados = set()
        componentes = []
        
        for i in range(self.num_vertices):
            if i not in visitados:
                comp = []
                # Fila para explorar os vizinhos em ondas (camadas)
                fila = deque([i])
                visitados.add(i)
                
                while fila:
                    atual = fila.popleft()
                    comp.append(self.vertices[atual].informacao)
                    
                    # Coloca todos os vizinhos não visitados na fila
                    for vizinho in adj_bidi[atual]:
                        if vizinho not in visitados:
                            visitados.add(vizinho)
                            fila.append(vizinho)
                # Guarda o ponto encontrado
                componentes.append(comp)
        return componentes

    # CENTRALIDADE
    # Algoritmo de Dijkstra
    def distancias_minimas(self, origem_id):
        # Calcula o caminho "mais barato/curto" do nó de origem até TODOS os outros.
        # Usa uma Fila de Prioridade (Heap) para sempre explorar o caminho mais curto primeiro.

        dist = [float('inf')] * self.num_vertices
        pais = [[] for _ in range(self.num_vertices)]
        dist[origem_id] = 0
        heap = [(0, origem_id)]
        
        while heap:
            d, u = heapq.heappop(heap) # Pega o nó mais próximo no momento
            if d > dist[u]: continue # Ignora se já achamos um caminho melhor antes
            
            for a in self.vertices[u].adjacencias:
                v = a.destino
                # Se passar por 'u' for mais rápido para chegar em 'v', atualizamos
                if dist[u] + a.peso < dist[v]:
                    dist[v] = dist[u] + a.peso
                    pais[v] = [u]
                    heapq.heappush(heap, (dist[v], v))

                # Se for um caminho alternativo com o mesmo custo exato, empatamos
                elif dist[u] + a.peso == dist[v]:
                    pais[v].append(u)
        return dist, pais

    # CENTRALIDADE DE PROXIMIDADE (CLOSENESS)
    # O algoritmo calcula a soma das menores distâncias desse artista para todos os outros artistas da rede.
    # Ter um valor alto significa que a soma dessas distâncias é muito pequena.
    # Ou seja, este artista está a pouquíssimos "saltos" (arestas) de distância de qualquer outro membro do grafo, possuindo um tempo de resposta ou transmissão mínimo para espalhar dados pela topologia de forma direta, sem depender de longas cadeias de terceiros.
    def centralidade_proximidade(self, rotulo_no):
        # CLOSELENESS: Mede o quão "perto" este artista está de todo o resto da rede.
        # Alta proximidade = consegue espalhar informações/royalties rapidamente.
        
        if rotulo_no not in self.rotulo_para_id: return 0
        v_id = self.rotulo_para_id[rotulo_no]
        
        # Pega as menores distâncias dele para todo mundo
        dist, _ = self.distancias_minimas(v_id)

        # Soma todas as distâncias válidas
        soma_dist = sum(d for d in dist if d != float('inf'))
        
        if soma_dist == 0 or self.num_vertices <= 1:
            return 0
        
        # Se a soma das distâncias for pequena, a centralidade de proximidade é alta. Se for grande, a centralidade é baixa.
        # Fórmula padrão de proximidade: (Total de nós - 1) / Soma das distâncias
        return (self.num_vertices - 1) / soma_dist

    # CENTRALIDADE DE INTERMEDIAÇÃO (BETWEENNESS)
    # O algoritmo mapeia todos os caminhos mais curtos possíveis entre todos os pares de artistas da rede. 
    # Em seguida, ele conta em quantos desses caminhos ideais o artista em questão aparece como um intermediário obrigatório. 
    # Ter um valor alto significa que uma quantidade massiva de fluxos de informação ou caminhos dependem diretamente desse vértice para transitar de uma região do grafo para outra.
    def centralidade_intermediacao(self, rotulo_no):
        # Betweenness Centrality: Mede o quanto este artista age como uma "ponte" no sistema. 
        # Se tirar ele, os caminhos curtos entre os outros artistas quebram?

        if rotulo_no not in self.rotulo_para_id: return 0
        v_alvo = self.rotulo_para_id[rotulo_no]
        
        travessias = 0
        # Usando Dijkstra 
        # limitamos a uma amostra aleatória de 50 nós para grafos gigantes.
        amostra = min(self.num_vertices, 50) 
        
        for i in range(amostra):
            if i == v_alvo: continue
            # Calcula todos os caminhos mínimos saindo do nó 'i'
            _, pais = self.distancias_minimas(i)
            
            for j in range(self.num_vertices):
                # Se o nosso 'v_alvo' estiver no meio do caminho ideal entre 'i' e 'j', pontua
                if i != j and v_alvo in pais[j]:
                    travessias += 1
                    
        # Normalização matemática para devolver um valor entre 0 e 1
        return travessias / ((amostra - 1) * (amostra - 2) + 1e-9)


def gerar_grafo(num_nos, num_arestas, conexo=True):
    grafo = Grafo()
    prefixo = "Artista_"
    
    # 1. Cria todos os nós primeiro
    for i in range(num_nos):
        grafo.obter_ou_criar_vertice(f"{prefixo}{i}")
        
    arestas_add = 0
    
    # 2. Se a rede precisa ser conexa (um bloco só), ligamos cada novo artista a um artista anterior aleatório, criando uma árvore inicial.
    if conexo:
        for i in range(1, num_nos):
            pai = random.randint(0, i - 1)
            peso = random.randint(1, 50)
            grafo.adicionar_aresta(f"{prefixo}{pai}", f"{prefixo}{i}", peso)
            arestas_add += 1

    # 3. Distribui o restante das arestas aleatoriamente para atingir a meta
    while arestas_add < num_arestas:
        origem = random.randint(0, num_nos - 1)
        destino = random.randint(0, num_nos - 1)
        
        # Evita que um artista faça uma transação para ele mesmo
        if origem != destino:
            peso = random.randint(1, 50)
            grafo.adicionar_aresta(f"{prefixo}{origem}", f"{prefixo}{destino}", peso)
            arestas_add += 1
            
    return grafo