#include <stdio.h>
#include <stdlib.h>

void printarVetor(int *vet);
void shakesort(int *vet, int tamanho);

int main (){
    int vet[10] = {8 ,4, 33, 66, 200, -2, -5, 1, 0, 64};
    //int vet[7] = {20, 1, 15, 5, 25, 5, 10};
    printarVetor(vet);
    shakesort(vet, 10);
    printarVetor(vet);
    return 0;
}

void printarVetor(int *vet){
    for(int i = 0; i < 10; i++){
        printf("%d ", vet[i]);
    }
    printf("\n");
    return;
}

void shakesort(int *vet, int tamanho){              // Tempos:
    int aux;                                        // 1
    int esq = 0, dir = tamanho-1;                   // 1

    while(dir > esq){                               // A soma dos tempos dos dois laços 'for'
        for (int i = esq; i < dir; i++){            // Somatório 1
            if (vet[i] > vet[i+1]){                 // 1
                aux = vet[i+1];                     // 1
                vet[i+1] = vet[i];                  // 1
                vet[i] = aux;                       // 1
            }
        }    
        
        for (int i = dir-1; i > esq; i--){          // Somatório 2
            if (vet[i] < vet[i-1]){                 // 1
                aux = vet[i-1];                     // 1
                vet[i-1] = vet[i];                  // 1
                vet[i] = aux;                       // 1
            }
        }

        esq++;                                      // 1
        dir--;                                      // 1
    }
    return;
}

