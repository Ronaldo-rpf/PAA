#!/usr/bin/env python3
import sys

INF = 10**30

def ler_arquivo(nome):
    nums = []
    with open(nome, "r") as f:
        for raw in f:
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            for p in s.split():
                try:
                    nums.append(int(p))
                except ValueError:
                    raise ValueError(f"Token não inteiro encontrado no arquivo: '{p}'")
    return nums

def construir_estruturas(nums):
    idx = 0
    if len(nums) < 2:
        raise ValueError("Arquivo mal formatado: precisa conter L e N.")
    L = nums[idx]; idx += 1
    N = nums[idx]; idx += 1

    # a: tempos de produção
    a = [[0]*N for _ in range(L)]
    for i in range(L):
        for j in range(N):
            a[i][j] = nums[idx]; idx += 1

    # t_mesma: transporte na mesma linha
    t_mesma = [[0]*(N-1) for _ in range(L)]
    for i in range(L):
        for j in range(N-1):
            t_mesma[i][j] = nums[idx]; idx += 1

    # t_troca: transporte trocando de linha (LxLx(N-1))
    t_troca = [[[0]*(N-1) for _ in range(L)] for _ in range(L)]
    for i in range(L):
        for j in range(L):
            if i == j:
                continue
            for k in range(N-1):
                t_troca[i][j][k] = nums[idx]; idx += 1

    # entradas e saídas
    e = nums[idx: idx+L]; idx += L
    x = nums[idx: idx+L]; idx += L

    return L, N, a, t_mesma, t_troca, e, x

def calcular_f_l(L, N, a, t_mesma, t_troca, e, x):
    f = [[0]*N for _ in range(L)]
    l = [[-1]*N for _ in range(L)]

    for i in range(L):
        f[i][0] = e[i] + a[i][0]
        l[i][0] = -1

    for j in range(1, N):
        for i in range(L):
            melhor = INF
            melhorK = -1
            for k in range(L):
                if k == i:
                    tempo = f[k][j-1] + t_mesma[i][j-1] + a[i][j]
                else:
                    tempo = f[k][j-1] + t_troca[k][i][j-1] + a[i][j]
                if tempo < melhor:
                    melhor = tempo
                    melhorK = k
            f[i][j] = melhor
            l[i][j] = melhorK
    return f, l

def melhor_caminho(L, N, f, l, x):
    melhorTempo = INF
    melhorLinha = -1
    for i in range(L):
        custoFinal = f[i][N-1] + x[i]
        if custoFinal < melhorTempo:
            melhorTempo = custoFinal
            melhorLinha = i
    caminho = [-1]*N
    caminho[N-1] = melhorLinha
    for j in range(N-1, 0, -1):
        caminho[j-1] = l[caminho[j]][j]
    return melhorTempo, melhorLinha, caminho

def print_table_f(L, N, f):
    print("\nTabela F (Tempos ótimos acumulados):")
    for i in range(L):
        vals = " ".join(f"{v:6d}" for v in f[i])
        print(f"L{i+1}: {vals}")

def print_table_l(L, N, l):
    print("\nTabela L (Linha anterior ótima):")
    header = "Estação |" + "".join(f"  L{i+1}  |" for i in range(L))
    print(header)
    for j in range(1, N):
        line = f"{j+1:7d} |"
        for i in range(L):
            if l[i][j] >= 0:
                line += f"  {l[i][j]+1:2d}  |"
            else:
                line += "   -  |"
        print(line)

def print_caminho(caminho):
    print("\nCaminho ótimo (linha de cada estação):")
    print("[", end="")
    for j in range(len(caminho)):
        print(f"{caminho[j]+1}", end="")
        if j < len(caminho)-1:
            print(", ", end="")
    print("]")

def soma_por_linha(L, N, a, t_mesma, t_troca, caminho, e, x):
    produ = [0]*L
    transf = [0]*L
    entrada = [0]*L
    saida = [0]*L

    for j in range(N):
        linha = caminho[j]
        produ[linha] += a[linha][j]
        if j > 0:
            linhaAnt = caminho[j-1]
            if linhaAnt == linha:
                transf[linha] += t_mesma[linha][j-1]
            else:
                transf[linha] += t_troca[linhaAnt][linha][j-1]

    linhaInicio = caminho[0]
    linhaFinal = caminho[-1]
    entrada[linhaInicio] += e[linhaInicio]
    saida[linhaFinal] += x[linhaFinal]

    return produ, transf, entrada, saida

def main():
    nome = "estudo_de_caso.txt"
    nums = ler_arquivo(nome)
    L, N, a, t_mesma, t_troca, e, x = construir_estruturas(nums)

    print(f"Dados carregados: L={L}, N={N}")
    print(f"Entradas e: {e}")
    print(f"Saídas x: {x}")

    f, l = calcular_f_l(L, N, a, t_mesma, t_troca, e, x)
    melhorTempo, melhorLinha, caminho = melhor_caminho(L, N, f, l, x)

    print_table_f(L, N, f)
    print_table_l(L, N, l)
    print(f"\nTempo ótimo total (com saída): {melhorTempo} (Linha final {melhorLinha+1})")
    print_caminho(caminho)

    produ, transf, entrada, saida = soma_por_linha(L, N, a, t_mesma, t_troca, caminho, e, x)
    total_por_linha = [produ[i] + transf[i] + entrada[i] + saida[i] for i in range(L)]

    print("\nDetalhamento do custo por linha (entrada + produção + transferências + saída):")
    for i in range(L):
        print(f"Linha {i+1}: Entrada={entrada[i]} Produção={produ[i]} Transferências={transf[i]} Saída={saida[i]} => Total={total_por_linha[i]}")
    print(f"\nSoma dos totais por linha = {sum(total_por_linha)}  (deve ser igual ao Tempo ótimo total: {melhorTempo})")

if __name__ == "__main__":
    main()
