#include <stdio.h>
#include <stdlib.h>

void quicksort(int *vet, int esq, int dir);
int particiona (int *vet, int esq, int dir);
void decidePivo(int *vet, int esq, int dir);
void printarVetor(int *vet);

int main(){
    int vet[10] = {10, 9, 8, 2000, 6, 5, 4, 3, 2, 1};
    printarVetor(vet);
    quicksort(vet, 0, 9);
    printarVetor(vet);


    return 0;
}

void decidePivo(int *vet, int esq, int dir){
    if ((dir - esq + 1) < 3){
        return;
    }

    int aux;
    for(int i = esq; i < dir - 1; i++){
        for (int j = esq; j < dir - 1 - i; j++){
            if (vet[j] > vet[j+1]){
                aux = vet[j];
                vet[j] = vet[j+1];
                vet[j+1] = aux;
            }
        }
    }
    aux = vet[esq+1];
    vet[esq+1] = vet[esq];
    vet[esq] = aux;
    return;
}

void quicksort(int *vet, int esq, int dir){
    if (esq >= dir){
        return;
    }
    int indexPivo = particiona(vet, esq, dir);
    quicksort(vet, esq, indexPivo-1);
    quicksort(vet, indexPivo+1, dir);
}

int particiona (int *vet, int esq, int dir){
    decidePivo(vet, esq, dir);
    int pivo = vet[esq];
    int left = esq + 1;
    int right = dir;
    int aux;

    while (1){
        while (left <= right && vet[left] <= pivo){
            left++;
        }
        while (right >= left && vet[right] > pivo){
            right--;
        }
        if (left > right){
            break;
        }
        aux = vet[left];
        vet[left] = vet[right];
        vet[right] = aux;
    }

    vet[esq] = vet[right];
    vet[right] = pivo;
    return right;
}

void printarVetor(int *vet){
    for(int i = 0; i < 10; i++){
        printf("%d ", vet[i]);
    }
    printf("\n");
    return;
}
