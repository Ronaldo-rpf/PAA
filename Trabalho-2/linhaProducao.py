def linhaDeProducao(tempos_processamento, transporte_mesma_linha, transporte_troca, tempo_entrada, tempo_saida):
    # tempos_processamento[linha][estacao]
    # transporte_mesma_linha[linha][j] é o tempo da estacao j para j+1            
    # transporte_troca[linha_origem][linha_destino][j] é o tempo da linha_origem estacao j para linha_destino estacao j+1, na diagonal
    # tempo_entrada: Tempo para entrar na linha 
    # tempo_saida: Tempo para sair da linha 
    
    n_estacoes = len(tempos_processamento[0])# numero de coluna, igual uma matriz em c, porque uma matriz e um ponteiro de ponteiros, um vetor de varios ponteiros
    n_linhas = len(tempos_processamento) # numero de linhas
    
    # Matrizes para Programação Dinâmica
    # T: Tempo acumulado mínimo até o fim do processamento da estação j (tempo minimo de cada estacao)
    T = [[0] * n_estacoes for _ in range(n_linhas)]
    
    # Caminho: Para reconstruir a rota (0 = veio da mesma linha, 1 = veio da outra)
    # caminho[i][j] = qual linha a peça estava antes de chegar na linha i, estação j
    caminho = [[0] * n_estacoes for _ in range(n_linhas)]  # Cria uma lista com 'n_estacoes' de 0's e repete isso 'n_linhas' vezes. '_' não vai usar a variável dentro do loop, descartável. 

    # --- 1. CASO BASE (Primeira Estação) ---
    # O tempo é apenas Entrada + Processamento da primeira máquina
    T[0][0] = tempo_entrada[0] + tempos_processamento[0][0]
    T[1][0] = tempo_entrada[1] + tempos_processamento[1][0]
    T[2][0] = tempo_entrada[2] + tempos_processamento[2][0]
    
    # --- 2. ITERAÇÃO (Da estação 2 até o fim) ---
    for j in range(1, n_estacoes): #nunca chega no range
        
        # --- CÁLCULOS PARA A LINHA 0 (1) ---
        # Opção 1: Vir da Linha 1 (mesma) -> Esteira -> processar o nó
        from_line_0 = T[0][j-1] + transporte_mesma_linha[0][j-1] + tempos_processamento[0][j]
        # Opção 2: Vir da Linha 2 -> Troca -> processar
        from_line_1 = T[1][j-1] + transporte_troca[1][0][j-1] + tempos_processamento[0][j]
        # Opção 3: Vir da Linha 3 -> Troca -> processar
        from_line_2 = T[2][j-1] + transporte_troca[2][0][j-1] + tempos_processamento[0][j]
        
        if from_line_0 <= from_line_1 and from_line_0 <= from_line_2:
            T[0][j] = from_line_0
            caminho[0][j] = 0
        elif from_line_1 <= from_line_2:
            T[0][j] = from_line_1
            caminho[0][j] = 1
        else:
            T[0][j] = from_line_2
            caminho[0][j] = 2

        # --- CÁLCULOS PARA A LINHA 1 (2)---
        # Opção 1: Vir da Linha 1 -> Troca -> processar
        from_line_0 = T[0][j-1] + transporte_troca[0][1][j-1] + tempos_processamento[1][j]
        # Opção 2: Vir da Linha 2 (mesma) -> Esteira -> processar
        from_line_1 = T[1][j-1] + transporte_mesma_linha[1][j-1] + tempos_processamento[1][j]
        # Opção 3: Vir da Linha 3 -> Troca -> processar
        from_line_2 = T[2][j-1] + transporte_troca[2][1][j-1] + tempos_processamento[1][j]
        
        if from_line_0 <= from_line_1 and from_line_0 <= from_line_2:
            T[1][j] = from_line_0
            caminho[1][j] = 0
        elif from_line_1 <= from_line_2:
            T[1][j] = from_line_1
            caminho[1][j] = 1
        else:
            T[1][j] = from_line_2
            caminho[1][j] = 2

        # --- CÁLCULOS PARA A LINHA 2 ---
        # Opção 1: Vir da Linha 1 -> Troca -> processar
        from_line_0 = T[0][j-1] + transporte_troca[0][2][j-1] + tempos_processamento[2][j]
        # Opção 2: Vir da Linha 2 -> Troca -> processar
        from_line_1 = T[1][j-1] + transporte_troca[1][2][j-1] + tempos_processamento[2][j]
        # Opção 3: Vir da Linha 3 (mesma) -> Esteira -> processar
        from_line_2 = T[2][j-1] + transporte_mesma_linha[2][j-1] + tempos_processamento[2][j]
        
        if from_line_0 <= from_line_1 and from_line_0 <= from_line_2:
            T[2][j] = from_line_0
            caminho[2][j] = 0
        elif from_line_1 <= from_line_2:
            T[2][j] = from_line_1
            caminho[2][j] = 1
        else:
            T[2][j] = from_line_2
            caminho[2][j] = 2

    # --- 3. FINALIZAÇÃO ---
    total_final_0 = T[0][n_estacoes-1] + tempo_saida[0]
    total_final_1 = T[1][n_estacoes-1] + tempo_saida[1]
    total_final_2 = T[2][n_estacoes-1] + tempo_saida[2]

    if total_final_0 <= total_final_1 and total_final_0 <= total_final_2:
        tempo_otimo = total_final_0
        linha_fim = 0
    elif total_final_1 <= total_final_2:
        tempo_otimo = total_final_1
        linha_fim = 1
    else:
        tempo_otimo = total_final_2
        linha_fim = 2

    # --- 4. RECONSTRUÇÃO DO CAMINHO COMPLETO ---
    trajeto = [None] * n_estacoes # e se for 0 ---------------------------------------------------------------------------------------------------------------------
    curr_line = linha_fim
    
    for j in range(n_estacoes-1, -1, -1): # passa por todas as estacoes pra refazer o melhor caminho final.
        trajeto[j] = curr_line
        if j > 0:
            curr_line = caminho[curr_line][j]
    
    return T, tempo_otimo, trajeto # T - matriz dos melhores tempos de cada nó, tempo_otimo - o melhor tempo de todos, trajeto - vetor do historico de caminhos pro melhor tempo.



# ==========================================
# ÁREA DE DADOS - INSIRA OS VALORES AQUI
# ==========================================

# 1. Tempo que a MÁQUINA fica parada processando a peça
tempos_processamento = [
    [1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2],  # Linha 1
    [2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1],  # Linha 2
    [3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2],  # Linha 3
]

# 2. Tempo de transporte NA MESMA LINHA (da estacao j para j+1)
# Note: Se tem 4 estações, tem 3 transportes entre elas
transporte_mesma_linha = [
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],  # Linha 1
    [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],  # Linha 2
    [1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1],  # Linha 3
]

# 3. Tempo de transporte TROCANDO DE LINHA
# Matriz 3D: transporte_troca[origem][destino][estacao]
transporte_troca = [
    [None, [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2], [3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3]],
    [[2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2], None, [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]],
    [[
3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3], [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2], None]
]

# 4. Tempos de Entrada e Saída
tempo_entrada = [4, 3, 5]  
tempo_saida = [3, 4, 2]  

# --- Execução ---
T, tempo_minimo, trajeto = linhaDeProducao(tempos_processamento, transporte_mesma_linha, transporte_troca, tempo_entrada, tempo_saida)

n_linhas = len(tempos_processamento) # numero de linhas
n_estacoes = len(tempos_processamento[0]) # numero de coluna, igual uma matriz em c, porque uma matriz e um ponteiro de ponteiros, um vetor de varios ponteiros








print("TABELA de tempos mínimos:")
for i in range(n_linhas):
    print(f"Linha {i+1}:", T[i]) # imprime a matriz dos melhores tempos 

print("\nTempo mínimo de produção:", tempo_minimo) # o melhor tempo possivel calculado
print("Trajetória ótima (linhas por etapa):", [x+1 for x in trajeto]) # cria uma nova lista com todos os valores de 'trajeto' + 1.

print("\n--- Detalhes do Processo ---")

# INÍCIO
linha_inicio = trajeto[0]
print(f"INÍCIO: Entrou na Linha {linha_inicio + 1} (Setup: {tempo_entrada[linha_inicio]}, Maq 1: {tempos_processamento[linha_inicio][0]})")

# PERCORRER AS ESTAÇÕES (da 2 em diante)
for j in range(1, n_estacoes): #nao chega no valor final do range.
    linha_atual = trajeto[j]
    linha_anterior = trajeto[j-1]
    
    if linha_atual == linha_anterior:
        # Mesma linha
        tipo_transp = "Esteira (mesma linha)"
        tempo_transp = transporte_mesma_linha[linha_anterior][j-1]
    else:
        # Troca de linha
        tipo_transp = "Troca (cruzamento)"
        tempo_transp = transporte_troca[linha_anterior][linha_atual][j-1]
    
    print(f"Estação {j+1}: Processou na Linha {linha_atual+1} (Tempo maq: {tempos_processamento[linha_atual][j]}). "
          f"Veio da Linha {linha_anterior+1} via {tipo_transp} (Tempo: {tempo_transp})")

# FIM
linha_fim = trajeto[n_estacoes-1] # se nao sai do range dos index.
print(f"FIM: Saída da Linha {linha_fim + 1}")

