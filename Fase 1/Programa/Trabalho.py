import re
from collections import deque
import math


class Grafo:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        # Lista de adjacência: para cada vértice, guarda uma lista de dicionários
        # representando as arestas/arcos que saem do vértice.
        self.lista_adj = [[] for _ in range(num_vertices + 1)]
        # Vértices requeridos
        self.vr = set()
        # Arestas (edges) requeridos (não direcionadas)
        self.er = set()
        # Arcos requeridos (direcionados)
        self.ar = set()

    def adicionar_aresta(
        self, u, v, custo=1, demanda=0, requerida=False, dirigido=False
    ):
        # Adiciona aresta/arco de u para v
        self.lista_adj[u].append(
            {
                "dest": v,
                "custo": custo,
                "demanda": demanda,
                "requerida": requerida,
                "dirigido": dirigido,
            }
        )
        if not dirigido:
            # Se não for dirigido, adiciona aresta "espelhada" de v para u
            self.lista_adj[v].append(
                {
                    "dest": u,
                    "custo": custo,
                    "demanda": demanda,
                    "requerida": requerida,
                    "dirigido": dirigido,
                }
            )
            if requerida:
                # Evita duplicidade
                self.er.add(tuple(sorted((u, v))))
        else:
            if requerida:
                self.ar.add((u, v))

    def adicionar_vertice_requerido(self, v):
        self.vr.add(v)

    # Método usado na depuração do código
    def imprimir_lista_adj(self):
        print("Lista de Adjacência:")
        for u in range(1, self.num_vertices):
            print(f"Vértice {u}:")
            for aresta in self.lista_adj[u]:
                print(
                    f"  -> {aresta['dest']} (custo={aresta['custo']}, demanda={aresta['demanda']}, "
                    f"requerida={aresta['requerida']}, dirigido={aresta['dirigido']})"
                )
            print()

    # 1. Quantidade de vértices
    def contar_vertices(self):
        return self.num_vertices

    # 2. Quantidade de arestas (edges não direcionadas)
    def contar_edges(self):
        num_edges = 0
        contadas = set()
        for u in range(self.num_vertices):
            for aresta in self.lista_adj[u]:
                if not aresta["dirigido"]:
                    v = aresta["dest"]
                    chave = tuple(sorted((u, v)))
                    if chave not in contadas:
                        num_edges += 1
                        contadas.add(chave)
        return num_edges

    # 3. Quantidade de arcos (direcionados)
    def contar_arcos(self):
        num_arcos = 0
        for u in range(self.num_vertices):
            for aresta in self.lista_adj[u]:
                if aresta["dirigido"]:
                    num_arcos += 1
        return num_arcos

    # 4. Quantidade de vértices requeridos
    def qtd_vertices_req(self):
        return len(self.vr)

    # 5. Quantidade de arestas requeridas
    def qtd_edges_req(self):
        return len(self.er)

    # 6. Quantidade de arcos requeridos
    def qtd_arcos_req(self):
        return len(self.ar)

    # 7. Densidade do grafo (order strength)
    def calc_densidade(self):
        # Conto o total de conexões do grafo
        total_conexoes = self.contar_arcos() + self.contar_edges()
        num_vertices = self.contar_vertices()
        # Obtenho o número maxímo de arcos no grafo
        max_arc = num_vertices * (num_vertices - 1)
        # Ontenho o número maxímo de arestas no grafo
        max_ed = num_vertices * (num_vertices - 1) / 2

        densidade = total_conexoes / (max_ed + max_arc)
        return round(densidade, 2)

    # 8. Contar componentes conectados (ignorando a direção) utilizando BFS
    def contar_componentes_conectados(self):
        visitado = [False] * self.num_vertices
        componentes = 0

        # Função para obter vizinhos ignorando a direção
        def obter_vizinhos(u):
            vizinhos = set()
            # Vizinhos dos quais u é a origem
            for aresta in self.lista_adj[u]:
                vizinhos.add(aresta["dest"])
            # Vizinhos onde u é o destino (percorre todos os vértices)
            for v in range(self.num_vertices):
                for aresta in self.lista_adj[v]:
                    if aresta["dest"] == u:
                        vizinhos.add(v)
            return vizinhos

        for v in range(self.num_vertices):
            if not visitado[v]:
                componentes += 1
                fila = deque([v])
                visitado[v] = True

                while fila:
                    u = fila.popleft()
                    for w in obter_vizinhos(u):
                        if not visitado[w]:
                            visitado[w] = True
                            fila.append(w)
        return componentes

    # 9. Grau mínimo dos vértices
    def grau_minimo(self):
        min_grau = len(self.lista_adj[1])
        for i in range(1, self.num_vertices):
            graus = len(self.lista_adj[i])
            if min_grau > graus:
                min_grau = graus
        return min_grau

    # 10. Grau maxímo
    def grau_maximo(self):
        max_grau = len(self.lista_adj[1])
        for i in range(1, self.num_vertices):
            graus = len(self.lista_adj[i])
            if max_grau < graus:
                max_grau = graus
        return max_grau

    def calcular_matriz_caminhos_minimos(self):
        """
        Calcula a matriz de distâncias e a matriz de predecessores usando o algoritmo de Floyd Warshall.
        Para cada par (i, j), usamos o custo mínimo dentre todas as arestas que saem de i para j,
        se houver múltiplas.
        """
        n = self.num_vertices

        # Inicializa a matriz de distâncias e predecessores
        # dist[i][j] = custo mínimo conhecido de i para j.
        # pred[i][j] = predecessor de j no caminho mais curto partindo de i.
        dist = [[math.inf] * n for _ in range(n)]
        pred = [[None] * n for _ in range(n)]

        # Inicializa: custo zero para i==j
        for i in range(n):
            dist[i][i] = 0
            pred[i][i] = i

        # Para cada aresta (ou arco) em cada lista de adjacência,
        # seleciona o menor custo (se houver mais de uma conexão).
        for u in range(n):
            for aresta in self.lista_adj[u]:
                v = aresta["dest"]
                custo = aresta["custo"]
                # Se já houver outra aresta entre u e v, usa o menor custo
                if custo < dist[u][v]:
                    dist[u][v] = custo
                    pred[u][v] = u

        # Aplica o algoritmo de Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j]

        return dist, pred

    def reconstruir_caminho(self, s, t, pred):
        """
        Reconstrói o caminho de s até t utilizando a matriz de predecessores.
        Retorna uma lista de vértices representando o caminho.
        Se não houver caminho, retorna lista vazia.
        """
        if pred[s][t] is None:
            return []
        caminho = [t]
        while t != s:
            t = pred[s][t]
            caminho.append(t)
        caminho.reverse()
        return caminho

    # 11 Intermediação
    def calcular_intermediacao(self):
        """
        Calcula a intermediação (betweenness) de cada vértice.
        Para cada par de vértices (s, t), conta quantas vezes um vértice aparece
        como intermediário no caminho mais curto entre s e t.
        """
        dist, pred = self.calcular_matriz_caminhos_minimos()
        intermed = [0] * self.num_vertices

        # Para cada par (s, t) s ≠ t
        for s in range(self.num_vertices):
            for t in range(self.num_vertices):
                if s != t and dist[s][t] < math.inf:
                    caminho = self.reconstruir_caminho(s, t, pred)
                    # Se existir caminho, incrementa para os vértices intermediários (excluindo s e t)
                    if len(caminho) > 2:
                        for v in caminho[1:-1]:
                            intermed[v] += 1
        return intermed

    # 12 Caminho médio
    def calcular_caminho_medio(self):
        """
        Calcula o caminho médio (average shortest path length) considerando
        somente os pares (i, j) conectados (ou seja, com distância < inf).
        """

        dist, _ = self.calcular_matriz_caminhos_minimos()
        soma = 0.0
        contador = 0
        n = self.num_vertices
        for i in range(n):
            for j in range(n):
                # Considera apenas caminhos entre vértices diferentes que sejam alcançáveis
                if i != j and dist[i][j] < math.inf:
                    soma += dist[i][j]
                    contador += 1

        return round(soma / contador, 2)

    # 13 Diâmetro
    def calcular_diametro(self):
        """
        Calcula o diâmetro do grafo, isto é, o maior custo entre os menores caminhos
        de todos os pares de vértices conectados.
        """

        # Obtém a matriz de distâncias, ignorando a matriz de predecessores aqui.
        dist, _ = self.calcular_matriz_caminhos_minimos()
        diametro = 0
        n = self.num_vertices
        for i in range(n):
            for j in range(n):
                # Considera apenas pares diferentes e conexos
                if i != j and dist[i][j] < math.inf:
                    diametro = max(diametro, dist[i][j])
        return diametro


def ler_arq(arq):
    with open(arq, "r") as f:
        linhas = f.readlines()

    num_vertices = None
    grafo = None
    secao = None

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        # Cabeçalho
        if linha.startswith("#Nodes:"):
            num_vertices = int(linha.split(":")[1])
            grafo = Grafo(num_vertices)
            continue

        if re.match(r"ReN\.", linha):
            secao = "ReN"
            continue
        if re.match(r"ReE\.", linha):
            secao = "ReE"
            continue
        if re.match(r"EDGE", linha):
            secao = "EDGE"
            continue
        if re.match(r"ReA\.", linha):
            secao = "ReA"
            continue
        if re.match(r"ARC", linha):
            secao = "ARC"
            continue

        if secao == "ReN":
            if m := re.match(r"N(\d+)", linha):
                v = int(m.group(1)) - 1
                grafo.adicionar_vertice_requerido(v)

        elif secao == "ReE":
            partes = linha.split()
            if len(partes) >= 6:
                _, u, v, custo, demanda, _ = partes
                grafo.adicionar_aresta(
                    int(u) - 1,
                    int(v) - 1,
                    int(custo),
                    int(demanda),
                    requerida=True,
                    dirigido=False,
                )

        elif secao == "EDGE":
            partes = linha.split()
            if (
                len(partes) >= 4
                and partes[-3].isdigit()
                and partes[-2].isdigit()
                and partes[-1].isdigit()
            ):
                u = int(partes[-3]) - 1
                v = int(partes[-2]) - 1
                custo = int(partes[-1])
                grafo.adicionar_aresta(u, v, custo, 0, requerida=False, dirigido=False)

        elif secao == "ReA":
            partes = linha.split()
            if len(partes) >= 6:
                _, u, v, custo, demanda, _ = partes
                grafo.adicionar_aresta(
                    int(u) - 1,
                    int(v) - 1,
                    int(custo),
                    int(demanda),
                    requerida=True,
                    dirigido=True,
                )

        elif secao == "ARC":
            partes = linha.split()
            if (
                len(partes) >= 4
                and partes[-3].isdigit()
                and partes[-2].isdigit()
                and partes[-1].isdigit()
            ):
                u = int(partes[-3]) - 1
                v = int(partes[-2]) - 1
                custo = int(partes[-1])
                grafo.adicionar_aresta(u, v, custo, 0, requerida=False, dirigido=True)

    return grafo


grafo = ler_arq("Fase 1/Programa/Testes/BHW1.dat")


grafo.imprimir_lista_adj()

##### Estatísticas do grafo #####
print(f"1. Número de vértices: {grafo.contar_vertices()}")

print(f"2. Número de arestas: {grafo.contar_edges()}")

print(f"3. Númeor de arcos: {grafo.contar_arcos()}")

print(f"4. Número de vértices requeridos: {grafo.qtd_vertices_req()}")

print(f"5. Número de arestas requeridas: {grafo.qtd_edges_req()}")

print(f"6. Número de arcos requeridos: {grafo.qtd_arcos_req()}")

print(f"7. Densidade do grafo: {grafo.calc_densidade()}")

print(f"8. Componentes conectados: {grafo.contar_componentes_conectados()}")

print(f"9. Grau mínimo: {grafo.grau_minimo()}")

print(f"10. Grau maxímo: {grafo.grau_maximo()}")

print()

intermediacao = grafo.calcular_intermediacao()

print("11. Intermediação: ")

for v in range(grafo.num_vertices):
    print(
        f"  Vértice {v} aparece {intermediacao[v]} vezes como intermediário nos caminhos mais curtos."
    )

print()

print(f"12. Caminho médio: {grafo.calcular_caminho_medio()}")

print(f"13. Diâmetro: {grafo.calcular_diametro()}")
