

def bubbleSort(vetor, tam):
    aux: int
    for i in range(tam - 1):
        for j in range(tam - 1 - i):
            if vetor[j] > vetor[j+1]:
                aux = vetor[j]
                vetor[j] = vetor[j+1]
                vetor[j+1] = aux



vetor = [8 ,7,6,5,4,3,2,2,1,0]
bubbleSort(vetor, len(vetor))
print(vetor)