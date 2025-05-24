import re
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self, numero_de_nos, capacidade, deposito):
        self.numero_de_nos = numero_de_nos
        # Inicializa a lista de adjacência para a representação do grafo
        self.lista_adj = [[] for _ in range(numero_de_nos + 1)]
        # Inicializa um set para os nós requeridos
        self.nos_requeridos = set()
        # Inicializa um set para as arestas requeridas
        self.arestas_requeridas = set()
        # Inicializa um set para os arcos requeridas
        self.arcos_requeridos = set()
        # Capacidade do veículo
        self.capacidade = capacidade
        # Armazena o valor do nó de deposito
        self.deposito = deposito

    def addNohRequerido(self, noh, demanda, custo):
        self.nos_requeridos.add((noh, demanda, custo))

    def auxAddConexao(self, saida: int, destino: int, custo: float, demanda: int = 0):
        """
        _Função auxíliar usada para acrescentar uma aresta ou arco no grafo._
        Args:
            saida (int): Vértice de saída
            destino (int): Vértice destino
            custo (float): Custo para percorrer o caminho
            demanda (int, optional): Demanda usada se a conexão é requerida. Defaults to 0.
        """
        self.lista_adj[saida].append(
            {"saida": saida, "destino": destino, "custo": custo, "demanda": demanda}
        )

    def addArco(
        self, saida: int, destino: int, requerido: bool, custo: float, demanda: int = 0
    ):
        """
        _Adiciona uma aresta direcionada ao grafo._
        _Se a aresta for requerida, ela será armazenada no conjunto de arestas requeridas._
        Args:
            saida (int): Vértice de onde o arco saí.
            destino (int): Vértice onde o arco chega.
            requerido (bool): Se o vértice é requerido.
            custo (float): Custo para percorrer o arco.
        """
        self.auxAddConexao(saida, destino, custo, demanda)
        if requerido:
            # Adiciona o arco ao set de arcos requeridos
            self.arcos_requeridos.add((saida, destino))

    def addAresta(
        self, saida: int, destino: int, requerido: bool, custo: float, demanda: int = 0
    ):
        """
        _Adiciona uma aresta não direcionada no grafo._
        _Se ela é requerida, ela será armazenada no conjunto de arestas requeridas._
        Args:
            saida (int): Vértice de onde a aresta saí.
            destino (int): Vértice onde a aresta chega.
            requerido (bool): Se a aresta é requerida ou não.
            custo (float): Custo para percorrer a aresta.
            demanda (int): Demanda usada se a aresta é requerida. Defaults to 0.
        """
        # Adiciona conexão de um vértice x -> y
        self.auxAddConexao(saida, destino, custo, demanda)
        # Adiciona conexão de um vértice y -> x
        self.auxAddConexao(destino, saida, custo, demanda)
        if requerido:
            # Adiciona a aresta ao set de arestas requeridas. Ordena a tupla antes de adicionar para evitar repetição
            self.arestas_requeridas.add(tuple(sorted((saida, destino))))

    def imprimirGrafo(self):
        """
        _Imprime o grafo no terminal._
        """
        for i in range(1, self.numero_de_nos + 1):
            print(f"Vértice {i}: ")
            for j in self.lista_adj[i]:
                print(f"-> {j["destino"]}")

    def visualizarGrafo(self):
        G = nx.MultiDiGraph()

        for i in range(1, self.numero_de_nos):
            for j in self.lista_adj[i]:
                G.add_edge(j["saida"], j["destino"])

        nx.draw(
            G,
            with_labels=True,
            node_color="lightblue",
            node_size=700,
            font_size=12,
        )

        plt.show()        
        

def ler_arquivo(arq: str):
    """
    _Faz a leitura de um arquivo de teste e retorna o grafo resultante_
    Args:
        arq (str): caminho do arquivo de teste
    """

    # Abre o arquivo
    arquivo = open(arq, "r")

    capacidade = 0
    num_nos = 0
    deposito = 0

    # Faz a leitura do cabeçalho
    num_nos, capacidade, deposito = ler_cabecalho(arquivo)

    # Inicializa o grafo com o númeor de nós informado no cabeçalho
    grafo = Grafo(num_nos, capacidade, deposito)

    # Faz a leirtura dos nós requeridos
    ler_nos_requeridos(arquivo, grafo)

    # Faz a leitura das arestas requeridas
    ler_arestas(arquivo, grafo, True)

    # Lê as arestas não requeridas
    ler_arestas(arquivo, grafo)

    # Faz a leitura dos arcos requeridos
    ler_arcos(arquivo, grafo, True)

    # Lê os arcos não requeridos
    ler_arcos(arquivo, grafo)

    # Fecha o arquivo
    arquivo.close()

    return grafo


def ler_cabecalho(arquivo):
    capacidade = 0
    num_nos = 0
    deposito = 0

    linha = arquivo.readline()

    # Faz a leitura do cabeçalho do arquivo e obtém o número de nós
    while linha != "\n":
        # Retira os espaços em branco da linha
        linha = linha.strip()
        if linha.startswith("#Nodes"):
            # Pera o valor após o ':'(número de nós)
            num_nos = int(linha.split(":")[1])
        if linha.startswith("Capacity"):
            # Pera o valor após o ':'(capacidade)
            capacidade = int(linha.split(":")[1])
        if linha.startswith("Depot"):
            # Pera o valor após o ':'(número de nós)
            deposito = int(linha.split(":")[1])
        # Passa para a proxíma linha do arquivo
        linha = arquivo.readline()

    return num_nos, capacidade, deposito


def ler_nos_requeridos(arquivo, grafo: Grafo):
    # Lê os metadados
    linha = arquivo.readline()
    # Lê a primeira linha
    linha = arquivo.readline()
    # Faz a leitura dos nós requeridos
    while linha != "\n":
        linha = linha.strip()
        # Usa uma expressão regex para separar e retornar o nó, demanda e custo de serviço
        match = re.match(r"N(\d+)\t(\d+)\t(\d+)", linha)

        noh_requerido = int(match.group(1))
        demanda = int(match.group(2))
        custo = int(match.group(3))

        # Adciona o nó requerido
        grafo.addNohRequerido(noh_requerido, demanda, custo)
        linha = arquivo.readline()


def ler_arestas(arquivo, grafo: Grafo, requerido: bool = False):
    # Pega os metadados
    linha = arquivo.readline().strip()

    # Pega a primeira linha de arestas
    linha = arquivo.readline()
    while linha.startswith("E") or linha.startswith("N"):
        linha = linha.strip()
        partes = linha.split()

        demanda = 0
        s_custo = 0

        if requerido:
            _, inicio, destino, t_custo, demanda, s_custo = partes
        else:
            (
                _,
                inicio,
                destino,
                t_custo,
            ) = partes

        grafo.addAresta(
            int(inicio),
            int(destino),
            requerido,
            int(t_custo) + int(s_custo),
            int(demanda),
        )
        linha = arquivo.readline()


def ler_arcos(arquivo, grafo: Grafo, requerido: bool = False):
    # Pega os metadados
    linha = arquivo.readline().strip()

    # Pega a primeira linha de arestas
    linha = arquivo.readline()
    while linha.startswith("A") or linha.startswith("N"):
        linha = linha.strip()
        partes = linha.split()

        demanda = 0
        s_custo = 0

        if requerido:
            _, inicio, destino, t_custo, demanda, s_custo = partes
        else:
            (
                _,
                inicio,
                destino,
                t_custo,
            ) = partes

        grafo.addArco(
            int(inicio),
            int(destino),
            requerido,
            int(t_custo) + int(s_custo),
            int(demanda),
        )

        linha = arquivo.readline()


grafo = ler_arquivo(r"Trabalho\Grafos-\Testes\BHW1.dat")
grafo.imprimirGrafo()

