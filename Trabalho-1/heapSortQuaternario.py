
def sift(vetor, index, tam):
    indexHeap = index + 1
    filho1 = 2*indexHeap
    filho2 = (2*indexHeap) + 1
    filho3 = (2*indexHeap) + 2
    filho4 = (2*indexHeap) + 3
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
    for x in range(tam//4, 0, -1):
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