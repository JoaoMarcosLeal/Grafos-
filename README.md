# 📘 Trabalho para a matéria **GCC262 - Grafos e suas Aplicações**

---

## 📌 Descrição do Problema

O problema base pode ser definido em um grafo conexo **G = (V, E)**, onde:

- **V** é o conjunto de nós (interseções ou esquinas em uma região urbana ou rural),
- **E** é o conjunto de arestas (vias de acesso, como ruas e avenidas).

Um subconjunto **ER ⊆ E** dessas arestas deve ser atendido. Seja **n = |ER|** o número de serviços.

Uma aresta **(i, j) ∈ E** pode ser percorrida qualquer número de vezes, com um custo **cᵢⱼ** a cada passagem. A ela está associada uma demanda **qᵢⱼ**, se for uma aresta requerida **(i, j) ∈ ER**.

🎯 O objetivo é encontrar um **conjunto de viagens de veículos com custo mínimo**, de forma que:

- Cada viagem comece e termine em um nó depósito **v₀ ∈ V**;
- Cada aresta requerida seja atendida por **uma única viagem**;
- A **demanda total de cada veículo** não exceda uma capacidade **Q**.

---

## 🔄 Variação do Problema

A variação estudada neste trabalho redefine o grafo como um **multigrafo conectado**:

> **G = (V, E, A)**

Onde:

- **V**: conjunto de nós,  
- **E**: conjunto de arestas (vias de mão dupla),  
- **A**: conjunto de arcos (vias de mão única).

Serviços são requeridos em:

- Um subconjunto de **nós VR ⊆ V**,  
- Arestas **ER ⊆ E**,  
- Arcos **AR ⊆ A**,  

De modo que o número total de serviços seja:  
> **n = |VR| + |ER| + |AR|**
