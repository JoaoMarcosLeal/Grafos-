import re


def get_qtd_nos(grafo):
    return len(grafo)


def parse_to_dict(arq):
    # Formato do grafo:
    # Grafo = { 1: [(2, 13, 1, True), (4, 17, 1, True)]}
    grafo = {}
    capacidade = None
    deposito = None
    secao = None

    # A abre e fecha o arquivo assim que as operações estiverem finazilzadas
    with open(arq) as f:
        # For para percorrer o arquivo linha por linha
        for linha in f:
            # Remove os espaços no início e no final do arquivo
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue

            # Retira as informações relevantes do cabeçalho
            if "Capacity" in linha:
                # Usa de expressões regulares para retirar o valor da capacidade
                # (\d+) pega todos os dígitos inteiros
                capacidade = int(re.search(r"\d+", linha).group())
            elif "Depot Node" in linha:
                # Faz o mesmo descrito acima
                deposito = int(re.search(r"\d+", linha).group())

            # Seções
            elif linha.startswith("ReE."):
                secao = "required_edges"
                continue
            elif linha.startswith("EDGE"):
                secao = "edges"
                continue
            elif linha.startswith("ReA."):
                secao = "required_arcs"
                continue
            elif linha.startswith("ARC"):
                secao = "arcs"
                continue

            # Parse conforme seção
            if secao == "required_edges":
                # R
                match = re.match(r"E\d+\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+\d+", linha)
                if match:
                    # Converte para inteiros cada string capturada na expressão regular
                    u, v, cost, demand = map(int, match.groups())
                    grafo.setdefault(u, []).append((v, cost, demand, True))
                    grafo.setdefault(v, []).append((u, cost, demand, True))

            elif secao == "edges":
                match = re.match(r"\w+\s+(\d+)\s+(\d+)\s+(\d+)", linha)
                if match:
                    u, v, cost = map(int, match.groups())
                    grafo.setdefault(u, []).append((v, cost, 0, False))
                    grafo.setdefault(v, []).append((u, cost, 0, False))

            elif secao == "required_arcs":
                match = re.match(r"A\d+\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d)+\s+\d+", linha)
                if match:
                    u, v, cost, demand = map(int, match.groups())
                    grafo.setdefault(u, []).append((v, cost, demand, True))

            elif secao == "arcs":
                match = re.match(r"Nr A\d+\s+(\d+)\s+(\d+)\s+(\d+)", linha)
                if match:
                    u, v, cost = map(int, match.groups())
                    grafo.setdefault(u, []).append((v, cost, 0, False))

    return grafo, capacidade, deposito


grafo, capacidade, deposito = parse_to_dict("Fase 1\Programa\Testes\BHW3.dat")

# Exibe o grafo
for u in grafo:
    for v, cost, demand, required in grafo[u]:
        tipo = "R" if required else "NR"
        print(f"{u} -> {v} | custo={cost}, demanda={demand}, {tipo}")

# Obtém o número de vértices do grafo
qtd_nos = get_qtd_nos(grafo)
