import random
import heapq

itens = [
    ["Arroz (5Kg)", 22, 10],
    ["Açúcar (2Kg)", 3, 5],
    ["Óleo (1L)", 8, 6],
    ["Feijão (1Kg)", 5, 10],
    ["Macarrão (500g)", 5, 8],
    ["Sardinha (1 lata)", 5, 7],
    ["Carne (1Kg)", 32, 9],
    ["Frango (1Kg)", 13, 9],
    ["Queijo (200g)", 8, 5],
    ["Presunto (200g)", 4, 5],
    ["Pão (8un.)", 6, 6],
    ["Banana (1Kg)", 4, 7],
    ["Laranja (1Kg)", 2, 7],
    ["Abacate (1Kg)", 7, 2],
    ["Sabão (1un.)", 2, 9],
    ["Limpador multiuso (1un.)", 4, 6],
    ["Água Tônica (500mL)", 7, 1],
    ["Polpa de Fruta (500mL)", 6, 4],
    ["Refrigerante (2L)", 8, 3],
    ["Cerveja (600mL)", 6, 2]
]

tamanhoPopulacao = 2000
numGeracoes = 2000
percMutacao = 0.05
orcamento = 75

def gerarSolucao():
    return [random.randint(0, 1) for i in range(len(itens))]

def funcaoFitness(solucao):
    precoTotal = 0
    importanciaTotal = 0
    for i in range(len(solucao)):
        if solucao[i] == 1:
            precoTotal += itens[i][1]
            importanciaTotal += itens[i][2]

    if precoTotal > orcamento:
        j = random.randint(0, 19)
        solucao[j] = 1 - solucao[j]
        return funcaoFitness(solucao)

    return importanciaTotal

def selecao(populacao):
    pais = random.choices(populacao, weights=[funcaoFitness(solucao) for solucao in populacao], k=2)
    return pais

def crossover(pai, mae):
    ponto = random.randint(1, len(pai) - 1)
    return pai[:ponto] + mae[ponto:], mae[:ponto] + pai[ponto:]

def mutacao(solucao):
    for i in range(len(solucao)):
        if random.random() < percMutacao:
            solucao[i] = 1 - solucao[i]

populacao = [gerarSolucao() for i in range(tamanhoPopulacao)]

for i in range(numGeracoes):
    proxPopulacao = heapq.nlargest(2, populacao, key=funcaoFitness)
    for j in range((tamanhoPopulacao-2) // 2):
        pai, mae = selecao(populacao)
        filhoUm, filhoDois = crossover(pai, mae)
        mutacao(filhoUm)
        mutacao(filhoDois)
        proxPopulacao.extend([filhoUm, filhoDois])
    populacao = proxPopulacao
    melhorSolucao = max(populacao, key=funcaoFitness)
    importanciaTotal = funcaoFitness(melhorSolucao)
    print(importanciaTotal)

melhorSolucao = max(populacao, key=funcaoFitness)
importanciaTotal = funcaoFitness(melhorSolucao)
custoTotal = sum(itens[i][1] for i in range(len(melhorSolucao)) if melhorSolucao[i] == 1)

print(f"A melhor combinação encontrada tem importância total {importanciaTotal} e custo total de R${custoTotal}:")

for i in range(len(melhorSolucao)):
    if melhorSolucao[i] == 1:
        print(f"{itens[i][0]} - R${itens[i][1]} - Importância {itens[i][2]}")