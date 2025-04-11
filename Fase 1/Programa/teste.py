import re


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

    def contar_vertices(self):
        return len(self.matriz)

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

    #
    def contar_arcos(self):
        num_arcos = 0
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                for aresta in self.matriz[i][j]:
                    if aresta["dirigido"]:
                        num_arcos += 1
        return num_arcos


def ler_bhw1_formato(arq):
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


grafo = ler_bhw1_formato("Fase 1/Programa/Testes/BHW1.dat")

print(f"Número de vértices: {grafo.contar_vertices()}")

print(f"Número de arestas: {grafo.contar_edges()}")

print(f"Númeor de arcos: {grafo.contar_arcos()}")
