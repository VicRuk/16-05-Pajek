from grafo import Grafo, gerar_grafo
import time

def main():
    print("="*70)
    print("REDE MUSICAL DRM (Digital Rights Management) - Rede de Fluxo Financeiro e Dependência Econômica.")
    print("Identifica quais artistas estão a poucos 'passos' de distância de toda a cadeia de pagamentos.\n"
    "Um artista com alta proximidade consegue espalhar ou receber fundos/direitos autorais muito mais rápido do que os outros.\n"
    "  - Alta Centralidade de Proximidade: Significa que o artista é um grande influenciador ou lançador de tendências. Na rede de transações e direitos autorais, o dinheiro ou a informação que sai dele chega a toda a cadeia musical de forma extremamente rápida\n"
    "  - Alta Centralidade de Intermediação: Significa que o artista 'Chave de Conectividade' (podendo representar grandes produtoras), que transita em muitos gêneros diferentes. Ele controla o fluxo e detém o poder de conectar novos talentos a submercados isolados.\n\n"
    
    "Revela quais produtores, gravadoras ou artistas independentes funcionam como 'pontes' obrigatórias para o dinheiro ou direitos passarem de um nicho para outro.\n"
    "Se um nó com alto Betweenness cair (for removido), o fluxo de royalties de uma comunidade inteira pode ficar isolado.\n\n"
    "Ajuda a plataforma a rastrear se existem fraudes, lavagem de dinheiro ou loops infinitos de pagamentos (onde o artista A paga B, que paga C, que devolve para A de forma suspeita).")
    print("="*70)

    NOS = 5000
    ARESTAS = 20000
    print(f"[*] Gerando grafo (Nós: {NOS}, Arestas: {ARESTAS})")
    inicio = time.time()
    grafo = gerar_grafo(NOS, ARESTAS, conexo=True)
    print(f"[+] Gerado em {time.time() - inicio:.2f} segundos.\n")

    arquivo_pajek = "relatorio.net"

    print("[*] Testando Gravação Pajek...")
    grafo.salvar_pajek(arquivo_pajek)
    print(f"[+] Salvo em '{arquivo_pajek}'.\n")

    print("[*] Verificando Propriedades Estruturais...")
    conexo = grafo.is_conexo()
    print(f"CONEXO: {'SIM' if conexo else 'NÃO'}")
    
    if not conexo:
        comps = grafo.componentes_conectados()
        print(f" * Componentes encontrados: {len(comps)}")
        
    print(f"EULERIANO: {'SIM' if grafo.is_euleriano() else 'NÃO'}")
    print(f"CICLICO: {'SIM' if grafo.is_ciclico() else 'NÃO'}\n")

    print("[*] Testando Centralidades")
    cp = grafo.centralidade_proximidade("Artista_0")
    print(f" Centralidade de Proximidade: {cp:.6f}")
    
    ci = grafo.centralidade_intermediacao("Artista_0")
    print(f" Centralidade de Intermediação (Aproximada): {ci:.6f}\n")

    print("[*] Testando Carregamento Pajek...")
    grafo = Grafo()
    grafo.carregar_pajek(arquivo_pajek)
    print(f"* Carregado - Vértices: {grafo.num_vertices})")
    print("="*60)

if __name__ == "__main__":
    main()