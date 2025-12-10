import random

def bubbleSort(vetor, esq, dir): 
    # Precisam ser dois parâmetro por conta do mergesort quaternário, senão ele ordenario sempre só
    # os primeiros valores do vetor do merge
    tam = dir - esq + 1
    for i in range(tam - 1): # Indica quantas vezes será executado
        for j in range(esq, dir - i): # Indica os índices que serão comparados
            if vetor[j] > vetor[j+1]:
                vetor[j], vetor[j+1] = vetor[j+1], vetor[j]


def mergeQuaternario(vetor, esq, meio1, meio2, meio3, dir):
    i1 = esq
    i2 = meio1 + 1
    i3 = meio2 + 1
    i4 = meio3 + 1
    limite1 = meio1
    limite2 = meio2
    limite3 = meio3
    limite4 = dir
    vetorAux = []

    while i1 <= limite1 or i2 <= limite2 or i3 <= limite3 or i4 <= limite4:
        valores = [] # Reinicia o vetor (clear)
        
        if i1 <= limite1:
            valores.append((vetor[i1], 0)) # Tuplas
            
        if i2 <= limite2:
            valores.append((vetor[i2], 1))
            
        if i3 <= limite3:
            valores.append((vetor[i3], 2))
            
        if i4 <= limite4:
            valores.append((vetor[i4], 3))
        
        menorValor, menorIndex = min(valores) # Por padrão compara o primeiro campo da tupla
        vetorAux.append(menorValor)
        
        if menorIndex == 0:
            i1 += 1
        elif menorIndex == 1:
            i2 += 1
        elif menorIndex == 2:
            i3 += 1
        else: 
            i4 += 1

    i1 = esq
    for x in range(len(vetorAux)):
        vetor[i1] = vetorAux[x]
        i1 += 1


def mergeSortQuaternario(vetor, esq, dir):
    if esq >= dir:
        return

    tamanho = dir - esq + 1

    if tamanho < 4:
        bubbleSort(vetor, esq, dir)
        return

    divisao = tamanho // 4 
    meio1 = esq + divisao - 1
    meio2 = esq + (2*divisao) - 1
    meio3 = esq + (3*divisao) - 1
    
    mergeSortQuaternario(vetor, esq, meio1)
    mergeSortQuaternario(vetor, meio1 + 1, meio2)
    mergeSortQuaternario(vetor, meio2 + 1, meio3)
    mergeSortQuaternario(vetor, meio3 + 1, dir)
    mergeQuaternario(vetor, esq, meio1, meio2, meio3, dir)


def sift(vetor, index, tam):
    indexHeap = index + 1
    filho1 = 4*(indexHeap - 1) + 2
    filho2 = 4*(indexHeap - 1) + 3
    filho3 = 4*(indexHeap - 1) + 4
    filho4 = 4*(indexHeap - 1) + 5
    maior = indexHeap

    if filho1 <= tam and vetor[filho1-1] > vetor[maior-1]:
        maior = filho1

    if filho2 <= tam and vetor[filho2-1] > vetor[maior-1]:
        maior = filho2

    if filho3 <= tam and vetor[filho3-1] > vetor[maior-1]:
        maior = filho3

    if filho4 <= tam and vetor[filho4-1] > vetor[maior-1]:
        maior = filho4

    if maior != indexHeap:
        vetor[maior-1], vetor[indexHeap-1] = vetor[indexHeap-1], vetor[maior-1]
        sift(vetor, maior-1, tam)
    else:
        return


def constroiHeap(vetor, tam):
    # Último índice pai é aquele que pelo menos o primeiro filho ainda exista e esteja dentro do vetor.
    # Ou seja, qual será o último índice "indexHeap" que 4*(indeHeap - 1) + 2 ainda esteja dentro do vetor, 
    # 4*(indeHeap - 1) + 2 <= tam
    # Isolando o "indexHeap": 
    # 4*indexHeap - 4 <= tam - 2
    # 4*indexHeap <= tam + 2
    # indexHeap <= (tam + 2) / 4 
    for x in range((tam + 2)//4, 0, -1):
        sift(vetor, x-1, tam)


def heapSort(vetor, tam):
    constroiHeap(vetor, tam)
    for i in range(tam-1, -1, -1):
        vetor[0], vetor[i] = vetor[i], vetor[0]
        sift(vetor, 0, i)


def preencheVetor(vetor, tam):
    for i in range(tam):
        num = random.randint(0, 700) # incluso os limites
        vetor.append(num)


def main():
    K2 = 60
    K1 = 560

    tamanho = int(input("Qual será o tamanho do vetor de entrada?\n"))
    vetor = []
    preencheVetor(vetor, tamanho)
    if tamanho < K2:
        print("Método de ordenação utilizado: BubbleSort")
        bubbleSort(vetor, 0, tamanho-1)
        print("Vetor ordenado.")
    elif tamanho >= K2 and tamanho < K1:
        print("Método de ordenação utilizado: Heapsort")
        heapSort(vetor, tamanho)
        print("Vetor ordenado.")
    else:
        print("Método de ordenação utilizado: Mergesort")
        mergeSortQuaternario(vetor, 0, tamanho-1)
        print("Vetor ordenado.")


if __name__ == "__main__":
    main()