def otimizacao_fabrica_detalhada(processamento, trans_mesma, trans_troca, entrada, saida):
    """
  
    processamento[linha][estacao]
          
    transporte_mesma: Matriz de tempos de TRANSPORTE NA MESMA LINHA (esteira)
                 trans_mesma[linha][j] é o tempo da estacao j para j+1
                 
    transporte_troca: Matriz de tempos de TRANSPORTE DE TROCA (robô transferidor)
                 transporte_troca[linha][j] é o tempo da linha 'linha' estacao j para a outra linha estacao j+1
                 
    entrada: Tempo para entrar na linha (setup inicial)
    saida: Tempo para sair da linha (finalização/expedição)
    """
    
    n_estacoes = len(processamento[0])
    n_linhas = len(processamento)
    
    # Matrizes para Programação Dinâmica
    # T: Tempo acumulado mínimo até o fim do processamento da estação j
    T = [[0] * n_estacoes for _ in range(n_linhas)]
    
    # Caminho: Para reconstruir a rota (0 = veio da mesma linha, 1 = veio da outra)
    # Vamos usar um identificador de linha de origem para ficar mais claro
    #caminho[i][j] = qual linha a peça estava antes de chegar na linha i, estação j
    #Exemplo: caminho[0][2] = 1 significa: "Para estar na Linha 0, Estação 2, a peça veio da Linha 1"
    caminho = [[0] * n_estacoes for _ in range(n_linhas)] # '_' não vai usar a variável dentro do loop, descartável

    # --- 1. CASO BASE (Primeira Estação) ---
    # O tempo é apenas Entrada + Processamento da primeira máquina
    T[0][0] = entrada[0] + processamento[0][0]
    T[1][0] = entrada[1] + processamento[1][0]
    
    # --- 2. ITERAÇÃO (Da estação 2 até o fim) ---
    for j in range(1, n_estacoes): #nunca chega no range
        
        # --- CÁLCULOS PARA A LINHA 0 (Digamos, Linha A) ---
        
        # Opção 1: Vir da Linha 0 (Anterior) -> Transporte Esteira 0 -> processar na 0
        from_line_0 = T[0][j-1] + trans_mesma[0][j-1] + processamento[0][j]
        
        # Opção 2: Vir da Linha 1 (Anterior) -> Transporte Troca -> processar na 0
        from_line_1 = T[1][j-1] + trans_troca[1][j-1] + processamento[0][j]

        if from_line_0 <= from_line_1:
            T[0][j] = from_line_0
            caminho[0][j] = 0 # Veio da linha 0
        else:
            T[0][j] = from_line_1
            caminho[0][j] = 1 # Veio da linha 1

        # --- CÁLCULOS PARA A LINHA 1 (Digamos, Linha B) ---
        
        # Opção 1: Vir da Linha 1 (Anterior) -> Transporte Esteira 1 -> processar na 1
        from_line_1_same = T[1][j-1] + trans_mesma[1][j-1] + processamento[1][j]
        
        # Opção 2: Vir da Linha 0 (Anterior) -> Transporte Troca -> processar na 1
        from_line_0_cross = T[0][j-1] + trans_troca[0][j-1] + processamento[1][j]

        if from_line_1_same <= from_line_0_cross:
            T[1][j] = from_line_1_same
            caminho[1][j] = 1 # Veio da linha 1
        else:
            T[1][j] = from_line_0_cross
            caminho[1][j] = 0 # Veio da linha 0

    # --- 3. FINALIZAÇÃO ---
    total_final_0 = T[0][n_estacoes-1] + saida[0]
    total_final_1 = T[1][n_estacoes-1] + saida[1]

    if total_final_0 <= total_final_1:
        tempo_otimo = total_final_0
        linha_fim = 0
    else:
        tempo_otimo = total_final_1
        linha_fim = 1

    # --- 4. RECONSTRUÇÃO DO CAMINHO COMPLETO ---
    trajeto = [None] * n_estacoes
    curr_line = linha_fim
    
    for j in range(n_estacoes-1, -1, -1):
        trajeto[j] = curr_line
        if j > 0:
            curr_line = caminho[curr_line][j]
    
    return T, tempo_otimo, trajeto


# ==========================================
# ÁREA DE DADOS - INSIRA SEUS VALORES AQUI
# ==========================================

# 1. Tempo que a MÁQUINA fica parada processando a peça
# Exemplo: 4 estações
tempos_processamento = [
    [7, 5, 4, 8],  # Linha 1
    [5, 5, 9, 3]   # Linha 2
]

# 2. Tempo de transporte NA MESMA LINHA (da estacao j para j+1)
# Note: Se tem 4 estações, tem 3 transportes entre elas
transporte_mesma_linha = [
    [1, 2, 1], # Linha 1 (Esteira rápida)
    [1, 2, 2]  # Linha 2 (Esteira lenta)
]

# 3. Tempo de transporte TROCANDO DE LINHA (da linha i para a outra)
transporte_troca = [
    [1, 1, 2], # De Linha 1 -> Linha 2 (Demorado)
    [1, 2, 1]  # De Linha 2 -> Linha 1
]

# 4. Tempos de Entrada e Saída
t_entrada = [3, 4]
t_saida = [4, 3]

# --- Execução ---
T, tempo_minimo, trajeto = otimizacao_fabrica_detalhada(
    tempos_processamento, 
    transporte_mesma_linha, 
    transporte_troca, 
    t_entrada, 
    t_saida
)

n_linhas = len(tempos_processamento)
n_estacoes = len(tempos_processamento[0])

print("TABELA f (tempos mínimos):")
for i in range(n_linhas):
    print(f"Linha {i+1}:", T[i])

print("\nTempo mínimo de produção:", tempo_minimo)
print("Trajetória ótima (linhas por etapa):", [x+1 for x in trajeto])

trocas = sum(1 for j in range(1, n_estacoes) if trajeto[j] != trajeto[j-1])
print("Número de transferências:", trocas)

print("\n--- Detalhes do Processo ---")

# INÍCIO
linha_inicio = trajeto[0]
print(f"INÍCIO: Entrou na Linha {linha_inicio + 1} (Setup: {t_entrada[linha_inicio]}, Maq 1: {tempos_processamento[linha_inicio][0]})")

# PERCORRER AS ESTAÇÕES (da 2 em diante)
for j in range(1, n_estacoes):
    linha_atual = trajeto[j]
    linha_anterior = trajeto[j-1]
    
    if linha_atual == linha_anterior:
        # Mesma linha
        tipo_transp = "Esteira (mesma linha)"
        tempo_transp = transporte_mesma_linha[linha_anterior][j-1]
    else:
        # Troca de linha
        tipo_transp = "Troca (cruzamento)"
        tempo_transp = transporte_troca[linha_anterior][j-1]
    
    print(f"Estação {j+1}: Processou na L{linha_atual+1} (Tempo maq: {tempos_processamento[linha_atual][j]}). "
          f"Veio da L{linha_anterior+1} via {tipo_transp} (Tempo: {tempo_transp})")

# FIM
linha_fim = trajeto[-1]
print(f"FIM: Saída da Linha {linha_fim + 1}")