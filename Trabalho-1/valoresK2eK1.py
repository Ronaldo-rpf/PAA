
# As classes assintóticas possuem gráficos diferentes, e quando os comparamos podemos achar um ponto de interseção, 
# e a partir daquele ponto uma das funções será melhor do que a outra, porque uma delas terá valores maiores de tempo 
# do que a outra. O eixo X seria o tamanho do vetor de entrada e o Y o tempo de execução.
#
# Bubblesort O(n²)
#
# Heapsort O(n log₄ n)
#
# Mergesort O(n log₄ n)
#
# Inicialmente tenho que achar o K2 e o K1 para fazer o código, quando o vetor de entrada for menor que K2 usarei o Bubblesort, 
# e se for maior (e menor que K1), usarei o Heapsort.
# Ponto de interseção:
# n² = n log₄ n
# n = log₄ n       (a função n, linear, cresce muito mais rápido que a logarítmica, elas nunca se cruzam)
# Logo, não existe solução real para isso, e o Heapsort e o Mergesort possuem a mesma classe assintótica para analisar, 
# então tive que fazer um código que calculasse o tempo de execução de cada algoritmo de ordenação para diferente tamanhos 
# de vetor de entrada, e analisar empiricamente onde o tempo de um seria melhor do que o de outro.

import random
import time
from main import *

def calculaTempoBubble(vetor, tam):
    inicio = time.time()
    bubbleSort(vetor, 0, tam-1)
    fim = time.time()
    tempoExecucao = fim - inicio
    return tempoExecucao


def calculaTempoHeap(vetor, tam):
    inicio = time.time()
    heapSort(vetor, tam)
    fim = time.time()
    tempoExecucao = fim - inicio
    return tempoExecucao


def calculaTempoMerge(vetor, tam):
    inicio = time.time()
    mergeSortQuaternario(vetor, 0, tam-1)
    fim = time.time()
    tempoExecucao = fim - inicio
    return tempoExecucao


def preencheVetor(vetor, tam):
    for i in range(tam):
        num = random.randint(0, 700) # incluso os limites
        vetor.append(num)


def tabelaTempos(vetorB, vetorH, vetorM):
    print("\t\tBubbleSort\t\tHeapsort\t\tMergesort")
    for i in range(len(vetorB)):
        print(f"Tamanho: {vetorB[i][1]}\t{vetorB[i][0]:<15}\t{vetorH[i][0]:^15}\t{vetorM[i][0]:>15}")


vetor = []
bubble = []
heap = []
merge = []
vetorTemposBubble = []
vetorTemposHeap = []
vetorTemposMerge = []

for tam in range(10, 800, 10):
    preencheVetor(vetor, tam)
    bubble = vetor[:]
    heap = vetor[:]
    merge = vetor[:]

    tempo = calculaTempoBubble(bubble, tam)
    tempo = format(tempo, ".18f")
    vetorTemposBubble.append((tempo, tam)) # Tuplas

    tempo = calculaTempoHeap(heap, tam)
    tempo = format(tempo, ".18f")
    vetorTemposHeap.append((tempo, tam))

    tempo = calculaTempoMerge(merge, tam)
    tempo = format(tempo, ".18f")
    vetorTemposMerge.append((tempo, tam))
    
    vetor.clear()

tabelaTempos(vetorTemposBubble, vetorTemposHeap, vetorTemposMerge)
