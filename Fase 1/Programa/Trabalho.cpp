#include <iostream>
#include <vector>
#include <fstream>

struct Aresta
{
    int destino;
    int custo_transito;
    int demanda;
    int custo_servico;
    bool requerido;
};

void lerArq(std::ifstream entrada)
{
}

void getCabecalho(std::ifstream &entrada)
{
    std::string text;
    for (int i = 0; i < 11; i++)
    {
        getline(entrada, text);
        std::cout << text << std::endl;
    }
}

int main()
{
    std::string mytext;
    std::ifstream entrada("../testes/BHW1.dat");

    getCabecalho(entrada);
    return 0;
}