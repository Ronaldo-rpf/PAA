
def sift(vetor, index, tam):
    indexHeap = index + 1
    filhoEsq = 2*indexHeap
    filhoDir = (2*indexHeap) + 1
    maior = indexHeap

    if filhoEsq <= tam and vetor[filhoEsq-1] > vetor[maior-1]:
        maior = filhoEsq

    if filhoDir <= tam and vetor[filhoDir-1] > vetor[maior-1]:
        maior = filhoDir

    if maior != indexHeap:
        vetor[maior-1], vetor[indexHeap-1] = vetor[indexHeap-1], vetor[maior-1]
        sift(vetor, maior-1, tam)
    else:
        return


def constroiHeap(vetor, tam):
    for x in range(tam//2, 0, -1):
        sift(vetor, x-1, tam)


def heapSort(vetor, tam):
    constroiHeap(vetor, tam)
    for i in range(tam-1, -1, -1):
        vetor[0], vetor[i] = vetor[i], vetor[0]
        sift(vetor, 0, i)



vetor1 = [22,33,55,66,99,88,55,66,1235,-4646,-5,-9,-8,-7,1]
print(f"Vetor sem Heap: {vetor1}")
heapSort(vetor1, len(vetor1))
print(f"Vetor Heapado: {vetor1}")