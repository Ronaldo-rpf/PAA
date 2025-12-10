#include <stdio.h>

void TrocoOtimo(int moedas[], int tamanho, int troco) {

    int quantidade[troco + 1];
    int ultima[troco + 1];

    quantidade[0] = 0;
    ultima[0] = 0;

    for (int c = 1; c <= troco; c++) {

        int quantidade_provisoria = c; // pior caso
        int ultima_provisoria = 1;

        for (int j = 0; j < tamanho; j++) {

            if (moedas[j] > c) continue;

            // segue EXATAMENTE sua condição
            if (quantidade[c - moedas[j]] + 1 <= quantidade_provisoria) {
                quantidade_provisoria = quantidade[c - moedas[j]] + 1;
                ultima_provisoria = moedas[j];
            }
        }

        quantidade[c] = quantidade_provisoria;
        ultima[c] = ultima_provisoria;
    }

    // imprimir tabela completa
    printf("c\tquantidade\tultima\n");
    for (int c = 0; c <= troco; c++) {
        printf("%d\t%d\t\t%d\n", c, quantidade[c], ultima[c]);
    }

    // mostrar troco ótimo
    printf("\nMoedas usadas no troco ótimo de %d centavos:\n", troco);
    int valor = troco;
    while (valor > 0) {
        printf("%d ", ultima[valor]);
        valor -= ultima[valor];
    }
    printf("\n");
}

int main() {

    // MATRÍCULA: 202410513 → resto = 13 → X = 13 + 5 = 18
    int moedas[] = {1, 3, 16, 18, 21};
    int tamanho = 5;
    int troco = 45;

    TrocoOtimo(moedas, tamanho, troco);

    return 0;
}