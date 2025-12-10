def assembly_dp(times, transfer):
    m = len(times)
    n = len(times[0])

    f = [[float('inf')] * n for _ in range(m)]
    parent = [[None] * n for _ in range(m)]

    # Caso base
    for i in range(m):
        f[i][0] = times[i][0]
        parent[i][0] = -1

    # Programação Dinâmica
    for j in range(1, n):
        for i in range(m):
            melhor = f[i][j-1] + times[i][j]
            origem = i

            for k in range(m):
                if k != i:
                    candidato = f[k][j-1] + transfer[k][i][j-1] + times[i][j]
                    if candidato < melhor:
                        melhor = candidato
                        origem = k

            f[i][j] = melhor
            parent[i][j] = origem

    # Melhor final
    ultima_etapa = n - 1
    melhor_linha = min(range(m), key=lambda i: f[i][ultima_etapa])
    melhor_tempo = f[melhor_linha][ultima_etapa]

    # Reconstrução do caminho
    caminho = [None] * n
    atual = melhor_linha
    for j in range(ultima_etapa, -1, -1):
        caminho[j] = atual
        atual = parent[atual][j]
        if atual == -1:
            break

    return f, melhor_tempo, caminho


# ==============================
# EXEMPLO DE USO (VOCÊ PODE EDITAR)
# ==============================

times = [
    [10, 6, 15, 30],   # Linha 1
    [9, 16, 25, 26]    # Linha 2
]

n = len(times[0])
m = len(times)

transfer = [[[0]*(n-1) for _ in range(m)] for __ in range(m)]

# custos de troca entre linhas
transfer[0][1] = [1, 1, 2]  # da linha 1 → 2
transfer[1][0] = [1, 2, 1]  # da linha 2 → 1


# ==============================
# EXECUÇÃO
# ==============================

f, tempo_minimo, caminho = assembly_dp(times, transfer)

print("\nTABELA f (tempos mínimos):")
for i in range(m):
    print(f"Linha {i+1}:", f[i])

print("\nTempo mínimo de produção:", tempo_minimo)
print("Trajetória ótima (linhas por etapa):", [x+1 for x in caminho])

trocas = sum(1 for j in range(1, n) if caminho[j] != caminho[j-1])
print("Número de transferências:", trocas)
