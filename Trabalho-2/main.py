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
    caminho = [[0] * n_estacoes for _ in range(n_linhas)]

    # --- 1. CASO BASE (Primeira Estação) ---
    # O tempo é apenas Entrada + Processamento da primeira máquina
    T[0][0] = entrada[0] + processamento[0][0]
    T[1][0] = entrada[1] + processamento[1][0]
    
    # --- 2. ITERAÇÃO (Da estação 2 até o fim) ---
    for j in range(1, n_estacoes):
        
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
        
        # Opção 1: Vir da Linha 1 (Anterior) -> Transporte Esteira 1 -> processamentoessar na 1
        from_line_1_same = T[1][j-1] + trans_mesma[1][j-1] + processamento[1][j]
        
        # Opção 2: Vir da Linha 0 (Anterior) -> Transporte Troca -> processamentoessar na 1
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

    # --- 4. RELATÓRIO DE ROTA (Backtracking) ---
    rota_passos = []
    curr_line = linha_fim
    
    rota_passos.append(f"FIM: Saída da Linha {curr_line + 1}")
    
    for j in range(n_estacoes-1, 0, -1):
        prev_line = caminho[curr_line][j]
        
        # Recuperar qual foi o custo de transporte usado
        if prev_line == curr_line:
            tipo_transp = "Esteira (mesma linha)"
            tempo_transp = trans_mesma[prev_line][j-1]
        else:
            tipo_transp = "Troca (cruzamento)"
            tempo_transp = trans_troca[prev_line][j-1]
            
        desc = (f"Estação {j+1}: Processou na L{curr_line+1} "
                f"(Tempo maq: {processamento[curr_line][j]}). "
                f"Veio da L{prev_line+1} via {tipo_transp} (Tempo: {tempo_transp})")
        
        rota_passos.append(desc)
        curr_line = prev_line # volta para o anterior

    rota_passos.append(f"INÍCIO: Entrou na Linha {curr_line + 1} "
                       f"(Setup: {entrada[curr_line]}, Maq 1: {processamento[curr_line][0]})")

    return tempo_otimo, rota_passos[::-1]

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
tempo, relatorio = otimizacao_fabrica_detalhada(
    tempos_processamento, 
    transporte_mesma_linha, 
    transporte_troca, 
    t_entrada, 
    t_saida
)

print(f"=== OTIMIZAÇÃO DE CHÃO DE FÁBRICA ===")
print(f"Tempo Total Mínimo: {tempo} unidades de tempo")
print("\n--- Detalhes do Processo ---")
for r in relatorio:
    print(r)
