# Aplicação de Grafos de Alta Dimensionalidade (Pajek) - TDE7

Integrantes do grupo:
- Gustavo Lazzari
- Mateus Roese
- Matheus Yamamoto
- Victor Ryuki

Projeto referente à matéria *Resolução de Problemas com Grafos* que reutiliza a representação de grafo com listas de adjacências dos TDEs anteriores e a estende para uma aplicação de alta dimensionalidade. O programa implementa gravação e carregamento de grafos direcionados e ponderados no formato Pajek, verificação de conexidade, identificação de componentes fracamente conectados, verificação de grafo Euleriano e cíclico, cálculo de Centralidade de Proximidade (Closeness) e de Intermediação (Betweenness) com base no melhor caminho, além de um gerador de grafo aleatório. As operações são aplicadas a uma rede modelada de fluxo financeiro e direitos autorais entre artistas (DRM), com 5.000 nós e 20.000 arestas.

## 1. Como executar

```zsh
python main.py
```

O programa gera um grafo aleatório de 5.000 nós e 20.000 arestas, grava o resultado em `relatorio.net` (formato Pajek) e executa todas as análises em sequência. A pasta `tests` contém grafos de exemplo prontos (`relatorio_euleriano.net`, `relatorio_nconexo.net`) que podem ser carregados via `carregar_pajek` para testar os casos específicos.

## 2. Estrutura do Repositório

```
.
├── aresta.py      # Classe Aresta, armazena o destino e o peso de uma aresta
├── vertice.py     # Classe Vertice, armazena id, rótulo e lista de adjacências, com incremento de peso em arestas repetidas
├── grafo.py       # Classe Grafo, implementa todas as operações (I/O Pajek, conexidade, componentes, Euleriano, ciclo, Dijkstra e centralidades) e o gerador de grafo aleatório
├── main.py        # Script principal que gera o grafo da rede DRM e executa todas as análises em sequência
├── tests/         # Grafos de exemplo no formato Pajek (relatorio.net, relatorio_euleriano.net, relatorio_nconexo.net)
└── README.md
```

## 3. Operações disponíveis

- `adicionar_aresta(origem, destino, peso=1)` - cria os vértices caso não existam e adiciona ou incrementa o peso da aresta direcionada entre eles
- `obter_ou_criar_vertice(rotulo)` - retorna o id do vértice associado ao rótulo, criando-o caso ainda não exista
- `salvar_pajek(caminho_arquivo)` - grava o grafo direcionado e ponderado em arquivo no formato Pajek (`*Vertices` e `*Arcs`, indexação base 1)
- `carregar_pajek(caminho_arquivo)` - reconstrói o grafo a partir de um arquivo no formato Pajek, aceitando seções `*Arcs` e `*Edges`
- `is_conexo()` - verifica se o grafo é conexo, retornando verdadeiro quando existe um único componente
- `componentes_conectados()` - retorna os componentes fracamente conectados via BFS, ignorando o sentido das arestas
- `is_euleriano()` - verifica se o grafo é Euleriano, exigindo que seja conexo e que o grau de entrada seja igual ao grau de saída em todos os nós
- `is_ciclico()` - verifica se o grafo possui ao menos um ciclo utilizando DFS com pilha de recursão
- `distancias_minimas(origem_id)` - calcula as menores distâncias da origem para todos os nós via Dijkstra com fila de prioridade, retornando as distâncias e os predecessores de cada caminho mínimo
- `centralidade_proximidade(rotulo_no)` - calcula a Centralidade de Proximidade (Closeness) do nó pela fórmula `(num_vertices - 1) / soma das menores distâncias`
- `centralidade_intermediacao(rotulo_no, aproximado=True)` - calcula a Centralidade de Intermediação (Betweenness) do nó contando em quantos caminhos mínimos ele aparece como intermediário; quando `aproximado=True`, usa uma amostra de 50 nós de origem para viabilizar grafos grandes
- `gerar_grafo(num_nos, num_arestas, conexo=True)` - gera um grafo aleatório com a quantidade de nós e arestas informada; quando `conexo=True`, liga cada novo nó a um anterior aleatório antes de distribuir as arestas restantes

## 4. Exemplo de uso

Saída do programa `main.py`, que gera a rede DRM com 5.000 nós e 20.000 arestas e executa todas as análises. Os valores de centralidade variam a cada execução, já que o grafo é gerado aleatoriamente:

```
======================================================================
REDE MUSICAL DRM (Digital Rights Management) - Rede de Fluxo Financeiro e Dependência Econômica.
Identifica quais artistas estão a poucos 'passos' de distância de toda a cadeia de pagamentos.
Um artista com alta proximidade consegue espalhar ou receber fundos/direitos autorais muito mais rápido do que os outros.
  - Alta Centralidade de Proximidade: Significa que o artista é um grande influenciador ou lançador de tendências...
  - Alta Centralidade de Intermediação: Significa que o artista 'Chave de Conectividade' (podendo representar grandes produtoras), que transita em muitos gêneros diferentes...
======================================================================
[*] Gerando grafo (Nós: 5000, Arestas: 20000)
[+] Gerado em 0.05 segundos.

[*] Testando Gravação Pajek...
[+] Salvo em 'relatorio.net'.

[*] Verificando Propriedades Estruturais...
CONEXO: SIM
EULERIANO: NÃO
CICLICO: SIM

[*] Testando Centralidades
 Centralidade de Proximidade: 0.012198
 Centralidade de Intermediação (Aproximada): 0.135204

[*] Testando Carregamento Pajek...
* Carregado - Vértices: 5000)
============================================================
```
