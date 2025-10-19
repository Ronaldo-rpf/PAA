def merge(vetor, esq, meio, dir):
    i = esq
    j = meio + 1
    vetorAux = []
    while i <= meio and j <= dir:
        if vetor[i] > vetor[j]:
            vetorAux.append(vetor[j])
            j += 1
        else:
            vetorAux.append(vetor[i])
            i += 1
        
    while i <= meio:
        vetorAux.append(vetor[i])
        i += 1

    while j <= dir:
        vetorAux.append(vetor[j])
        j += 1

    i = esq
    for x in range(len(vetorAux)):
        vetor[i] = vetorAux[x]
        i += 1


def mergeSort(vetor, esq, dir):
    if esq >= dir:
        return
    meio = (esq + dir) // 2
    mergeSort(vetor, esq, meio)
    mergeSort(vetor, meio + 1, dir)
    merge(vetor, esq, meio, dir)



vetor = [10,9,8,7,6,5,4,3,3,2,1,0]
tam = len(vetor) - 1
mergeSort(vetor, 0, tam)
print(vetor)