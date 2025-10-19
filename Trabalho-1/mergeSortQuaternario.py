
def bubbleSort(vetor, esq, dir):
    tam = dir - esq + 1
    for i in range(tam - 1):
        for j in range(esq, dir - i):
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
        valores = []
        
        if i1 <= limite1:
            valores.append((vetor[i1], 0))
            
        if i2 <= limite2:
            valores.append((vetor[i2], 1))
            
        if i3 <= limite3:
            valores.append((vetor[i3], 2))
            
        if i4 <= limite4:
            valores.append((vetor[i4], 3))
        
        menorValor, menorIndex = min(valores)
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


vetor = [99, 88, 77, 66, 44, 55, 33, 222]
tam = len(vetor) - 1
print(f"Vetor Original: {vetor}")
mergeSortQuaternario(vetor, 0, tam)
print(f"Vetor Ordenado: {vetor}")