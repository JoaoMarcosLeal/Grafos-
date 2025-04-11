import re
from collections import deque


class Grafo:
    def __init__(self, num_vertices):
        # Quantidade de vértices para montar a matriz de adjacência
        self.num_vertices = num_vertices
        # Matriz de adjacência usada para representar o Grafo
        self.matriz = [[[] for _ in range(num_vertices)] for _ in range(num_vertices)]
        # Vertices requeridas
        self.vr = set()
        # Edges requeridos
        self.er = set()
        # Arcos requeridos
        self.ar = set()

    def adicionar_aresta(
        self, u, v, custo=1, demanda=0, requerida=False, dirigido=False
    ):
        self.matriz[u][v].append(
            {
                "custo": custo,
                "demanda": demanda,
                "requerida": requerida,
                "dirigido": dirigido,
            }
        )
        if not dirigido:
            self.matriz[v][u].append(
                {
                    "custo": custo,
                    "demanda": demanda,
                    "requerida": requerida,
                    "dirigido": dirigido,
                }
            )
            if requerida:
                self.er.add(tuple(sorted((u, v))))
        else:
            if requerida:
                self.ar.add((u, v))

    # Adciona vértices requeridos
    def adicionar_vertice_requerido(self, v):
        self.vr.add(v)

    # Método para ajudar na depuração do código
    def imprimir_matriz(self):
        print("Matriz de Adjacência:")
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.matriz[i][j]:  # só imprime se houver pelo menos uma aresta/arco
                    print(f"{i} -> {j} :")
                    for aresta in self.matriz[i][j]:
                        print(
                            f"    custo={aresta['custo']}, demanda={aresta['demanda']}, requerida={aresta['requerida']}"
                        )

    # 1 Quantidade de vértices
    def contar_vertices(self):
        return len(self.matriz)

    # 2 Quantidade de arestas
    def contar_edges(self):
        num_edges = 0
        percorrido = set()
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                for aresta in self.matriz[i][j]:
                    if not aresta["dirigido"]:
                        chave = tuple(sorted((i, j)))
                        if chave not in percorrido:
                            num_edges += 1
                            percorrido.add(chave)
        return num_edges

    # 3 Quantidade de arcos
    def contar_arcos(self):
        num_arcos = 0
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                for aresta in self.matriz[i][j]:
                    if aresta["dirigido"]:
                        num_arcos += 1
        return num_arcos

    # 4 Quantidade de vértices requeridos
    def qtd_vertices_req(self):
        return len(self.vr)

    # 5 Quantidade de arestas requeridas
    def qtd_edges_req(self):
        return len(self.er)

    # 6 Quantidade de arcos requeridos
    def qtd_arcos_req(self):
        return len(self.ar)

    # 7 Densidade do grafo (order strength)
    def calc_densidade(self):
        # Obtém o número de arcos
        nmr_arcos = self.contar_arcos()
        # Obtém o número de arestas
        nmr_ed = self.contar_edges()
        # Determina o númeor maxímo de arcos
        max_arc = nmr_arcos * (nmr_arcos - 1)
        # Determina o número maxímo de arestas
        max_ed = (nmr_ed * (nmr_ed - 1)) / 2
        # Razão entre o número atual de arestas/arcos e o número maxímo de arestas/arcos
        return round(float((nmr_arcos + nmr_ed) / (max_ed + max_arc)), 2)

    # 8 Componentes conectados
    def contar_componentes_conectados(self):
        visitado = [False] * self.num_vertices
        # Vértice de origem
        s = 0
        # Mantém o tracking do número de componentes conectados entre si
        componentes = 0
        fila = deque(self.matriz[s][s])
        for v in range(self.num_vertices):
            if not visitado[v]:
                componentes += 1
                fila = deque([v])
                visitado[v] = True

                while fila:
                    u = fila.popleft()
                    for w in range(self.num_vertices):
                        if u == w:
                            continue
                        # Ignora a direção: considera conexão em qualquer sentido
                        if (self.matriz[u][w] or self.matriz[w][u]) and not visitado[w]:
                            visitado[w] = True
                            fila.append(w)

        return componentes


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

##### Estatísticas do grafo #####
print(f"1. Número de vértices: {grafo.contar_vertices()}")

print(f"2. Número de arestas: {grafo.contar_edges()}")

print(f"3. Númeor de arcos: {grafo.contar_arcos()}")

print(f"4. Número de vértices requeridos: {grafo.qtd_vertices_req()}")

print(f"5. Número de arestas requeridas: {grafo.qtd_edges_req()}")

print(f"6. Número de arcos requeridos: {grafo.qtd_arcos_req()}")

print(f"7. Densidade do grafo: {grafo.calc_densidade()}")

print(f"8. Componentes conectados: {grafo.contar_componentes_conectados()}")
