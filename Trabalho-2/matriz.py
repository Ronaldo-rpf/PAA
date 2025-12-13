import time

# ======= CONFIGURAÇÕES GLOBAIS =======
TAMANHO_MATRIZ = 10
TAMANHO_QUADRANTE = 5
VALOR_MINIMO = 1
VALOR_MAXIMO = 10
MAX_OCORRENCIAS_NUMERO_DIAGONAL = 2
MAX_NUMEROS_REPETIDOS_DIAGONAL = 2

solucoes_encontradas = []
contador_tentativas = 0


def criar_matriz_vazia():
    #Cria matriz 10x10 zerada
    return [[0] * TAMANHO_MATRIZ for _ in range(TAMANHO_MATRIZ)]


def verificar_vizinhanca(matriz, linha, coluna, valor):
    # Verifica se valor não repete nas 8 posições adjacentes. Retorna True se válido.
    for delta_linha in [-1, 0, 1]:
        for delta_coluna in [-1, 0, 1]:
            if delta_linha == 0 and delta_coluna == 0: # Propria posicao do numero, o meio.
                continue
            
            linha_vizinha = linha + delta_linha #a linha do numero vizinho
            coluna_vizinha = coluna + delta_coluna #a coluna do numero vizinho
            
            if 0 <= linha_vizinha < TAMANHO_MATRIZ and 0 <= coluna_vizinha < TAMANHO_MATRIZ: #verifica se está dentro da matriz.
                if matriz[linha_vizinha][coluna_vizinha] == valor: # se for igual ao numero do meio, esta errado.
                    return False
    return True


def verificar_diagonal(matriz, linha, coluna, direcao):
    #Verifica UMA diagonal específica.
    #direcao: 0 = diagonal principal, 1 = diagonal secundaria.
    
    #Regras:
    #1. Nenhum número pode aparecer mais de 2 vezes.
    #2. No máximo 2 números diferentes podem repetir.
    
    contagem = [0] * (VALOR_MAXIMO + 1) #vetor de contagem das repeticoes
    
    # Encontra início da diagonal
    linha_inicio = linha
    coluna_inicio = coluna
    
    if direcao == 0:  # Diagonal principal
        while linha_inicio > 0 and coluna_inicio > 0: #quer achar o primeiro valor da diagonal, quando um dos dois chegar a 0
            linha_inicio -= 1
            coluna_inicio -= 1
    else:  # Diagonal secundaria
        while linha_inicio > 0 and coluna_inicio < TAMANHO_MATRIZ - 1:
            linha_inicio -= 1
            coluna_inicio += 1
    
    # Percorre a diagonal contando valores
    linha_atual = linha_inicio
    coluna_atual = coluna_inicio
    
    while (0 <= linha_atual < TAMANHO_MATRIZ and 0 <= coluna_atual < TAMANHO_MATRIZ):
        valor = matriz[linha_atual][coluna_atual]
        
        if valor != 0:
            if valor < VALOR_MINIMO or valor > VALOR_MAXIMO:
                return False
            
            contagem[valor] += 1
            
            # REGRA 1: Nenhum número pode aparecer mais de 2 vezes
            if contagem[valor] > MAX_OCORRENCIAS_NUMERO_DIAGONAL:
                return False
        
        # Move para próxima posição da diagonal para verificar
        if direcao == 0:
            linha_atual += 1
            coluna_atual += 1
        else:
            linha_atual += 1
            coluna_atual -= 1
    
    # REGRA 2: Conta quantos números diferentes repetem (aparecem 2+ vezes)
    numeros_que_repetem = 0
    for quantidade in contagem: #percore o vetor contagem verificando se existem repeticoes 
        if quantidade > 1:
            numeros_que_repetem += 1
    
    if numeros_que_repetem > MAX_NUMEROS_REPETIDOS_DIAGONAL:
        return False
    
    return True


def verificar_todas_diagonais(matriz, linha, coluna):
    #Verifica ambas as direções de diagonal passando por (linha, coluna)
    if not verificar_diagonal(matriz, linha, coluna, 0): # principal, se for False, inverte e entra no if.
        return False
    if not verificar_diagonal(matriz, linha, coluna, 1): # secundaria
        return False
    return True


def calcular_somas_quadrantes(matriz):
    #Retorna lista com somas dos 4 quadrantes [Q1, Q2, Q3, Q4]
    somas = [0, 0, 0, 0]
    
    for linha in range(TAMANHO_MATRIZ): #vai passar por toda a matriz
        for coluna in range(TAMANHO_MATRIZ):
            valor = matriz[linha][coluna]
            
            # Determina qual quadrante
            if linha < TAMANHO_QUADRANTE and coluna < TAMANHO_QUADRANTE:
                somas[0] += valor  # Q1: Superior-Esquerdo
            elif linha < TAMANHO_QUADRANTE and coluna >= TAMANHO_QUADRANTE:
                somas[1] += valor  # Q2: Superior-Direito
            elif linha >= TAMANHO_QUADRANTE and coluna < TAMANHO_QUADRANTE:
                somas[2] += valor  # Q3: Inferior-Esquerdo
            else:
                somas[3] += valor  # Q4: Inferior-Direito
    
    return somas


def verificar_balanceamento(matriz, parametro_k):
    #Verifica se |Si - Sj| / St < k para todos os pares de quadrantes.
    #Retorna True se válido.
    
    somas_quadrantes = calcular_somas_quadrantes(matriz)
    soma_total = sum(somas_quadrantes) #St
    
    if soma_total == 0:
        return False
    
    # Verifica todos os pares de quadrantes
    for i in range(4):
        for j in range(i + 1, 4):
            diferenca = abs(somas_quadrantes[i] - somas_quadrantes[j]) #modulo
            razao = diferenca / soma_total
            
            if razao >= parametro_k:
                return False
    
    return True


def backtracking(matriz, linha, coluna, parametro_k, max_solucoes):
    #Algoritmo de backtracking.
    #Retorna True se deve parar a busca (atingiu max_solucoes).
    
    global contador_tentativas # chama a variavel global pra modificar ela, e nao criar outra LOCAL
    contador_tentativas += 1
    
    # Chegou ao final da matriz
    if linha == TAMANHO_MATRIZ:
        if verificar_balanceamento(matriz, parametro_k): #so verifico o K ao final dos preenchimentos.
            # Copia solução
            solucao = [linha[:] for linha in matriz]
            solucoes_encontradas.append(solucao) #coloca a matriz solucao no vetor de matrizes de solucao
            return len(solucoes_encontradas) >= max_solucoes # Ja encontrou quantas solucoes o usuario deseja, se nao, tenta outra
        return False # tenta outra tambem
    
    # Calcula próxima posição
    proxima_coluna = coluna + 1
    proxima_linha = linha
    if proxima_coluna == TAMANHO_MATRIZ:
        proxima_coluna = 0
        proxima_linha += 1
    
    # Tenta cada valor possível
    for valor in range(VALOR_MINIMO, VALOR_MAXIMO + 1): # pra entrar no intervalo de valores
        matriz[linha][coluna] = valor
        
        if not verificar_vizinhanca(matriz, linha, coluna, valor):
            matriz[linha][coluna] = 0 #se der False, tenta outro valor.
            continue
        
        if not verificar_todas_diagonais(matriz, linha, coluna):
            matriz[linha][coluna] = 0
            continue
        
        # Recursão
        if backtracking(matriz, proxima_linha, proxima_coluna, parametro_k, max_solucoes):
            matriz[linha][coluna] = 0 # mesmo que tenha encontrado uma solução zera a matriz.
            return True  # Atingiu max_solucoes
        
        matriz[linha][coluna] = 0 # se for False o backtracking, tenta outro valor, e sempre precisa limpa o anterior (precisa limpar pra noa atrapalhar a verificacao de numeros vizinhos).
    
    return False # se nao encontrar nenhuma solucao valida


def imprimir_matriz(matriz, numero_solucao):
    #Imprime matriz formatada
    print(f"\n{'='*60}")
    print(f"SOLUÇÃO {numero_solucao}")
    print('='*60)
    
    for linha in range(TAMANHO_MATRIZ):
        if linha == TAMANHO_QUADRANTE:
            print('-' * 33)
        
        linha_str = ""
        for coluna in range(TAMANHO_MATRIZ):
            if coluna == TAMANHO_QUADRANTE:
                linha_str += " | "
            linha_str += f"{matriz[linha][coluna]:2} " #reserva dois caracteres pra printar
        print(linha_str)


def imprimir_relatorio_quadrantes(matriz, parametro_k):
    #Imprime relatório de verificação dos quadrantes 
    somas = calcular_somas_quadrantes(matriz)
    soma_total = sum(somas)
    
    print(f"\n*** VERIFICAÇÃO DOS QUADRANTES ***")
    print(f"Q1 (Superior-Esquerdo):  {somas[0]:.0f}")
    print(f"Q2 (Superior-Direito):   {somas[1]:.0f}")
    print(f"Q3 (Inferior-Esquerdo):  {somas[2]:.0f}")
    print(f"Q4 (Inferior-Direito):   {somas[3]:.0f}")
    print(f"Soma Total (St):         {soma_total:.0f}")
    
    print(f"\nVerificação da condição |Si - Sj| / St < {parametro_k}:")
    print('-' * 60)
        
    for i in range(4):
        for j in range(i + 1, 4):
            soma_q_a = somas[i]
            soma_q_b = somas[j]
            
            diferenca = abs(soma_q_a - soma_q_b)
            razao = 0.0
            if soma_total > 0:
                razao = diferenca / soma_total
                
            eh_valido = razao < parametro_k
            status = "✓ VÁLIDO" if eh_valido else "✗ INVÁLIDO"
            
            print(f"Q{i+1} vs Q{j+1}: |{soma_q_a:.0f} - {soma_q_b:.0f}| / {soma_total:.0f} = {razao:.4f} {status}")


def resolver(parametro_k, quantidade_solucoes):
    #Função principal para resolver o problema.
    #Retorna lista de soluções encontradas.
    
    global solucoes_encontradas, contador_tentativas # chama a variavel global pra modificar ela, e nao criar outra LOCAL
    solucoes_encontradas = []
    contador_tentativas = 0
    
    #imprime um menu pras solucoes
    print("="*60)
    print(f"Parâmetro k: {parametro_k}")
    print(f"Valores possíveis: {VALOR_MINIMO} a {VALOR_MAXIMO}")
    print(f"Soluções desejadas: {quantidade_solucoes}")
    print(f"\nRegras:")
    print(f"1. Nenhum valor repete na vizinhança (8 adjacentes)")
    print(f"2. Em cada diagonal: máximo {MAX_OCORRENCIAS_NUMERO_DIAGONAL} ocorrências por número")
    print(f"3. Em cada diagonal: máximo {MAX_NUMEROS_REPETIDOS_DIAGONAL} números diferentes podem repetir")
    print(f"4. Balanceamento: |Si - Sj| / St < {parametro_k}")
    print("="*60)
    print("\nBuscando soluções...")
    
    tempo_inicio = time.time()
    
    matriz = criar_matriz_vazia() #com 0's
    backtracking(matriz, 0, 0, parametro_k, quantidade_solucoes)
    
    tempo_decorrido = time.time() - tempo_inicio
    
    # Imprime resultados
    print(f"\n{'='*60}")
    print("RESULTADOS")
    print("="*60)
    print(f"Tempo de execução: {tempo_decorrido:.2f} segundos")
    print(f"Tentativas realizadas: {contador_tentativas}")
    print(f"Soluções encontradas: {len(solucoes_encontradas)} / {quantidade_solucoes}")
    
    if len(solucoes_encontradas) == 0:
        print("\nNenhuma solução encontrada!")
        print("Sugestões:")
        print("  - Aumentar o valor de k")
        print("  - Reduzir o número de soluções desejadas")
    
    # Imprime cada solução
    for idx, solucao in enumerate(solucoes_encontradas, 1): # gera um par da solucao com o numero correspondente dela, para imprimir melhor
        imprimir_matriz(solucao, idx)
        imprimir_relatorio_quadrantes(solucao, parametro_k)
    
    return solucoes_encontradas


if __name__ == "__main__":
    # Parâmetros
    K = 0.2
    N_SOLUCOES = 2
    
    solucoes = resolver(K, N_SOLUCOES)

