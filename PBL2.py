#Autor: Tairone de Jesus Lima
#Componente curricular: MI algoritmos 1
#Concluído em: 00/00/2024
#Eu declaro que este código foi elaborado por mim de forma individual e não contém nenhum
#trecho de código de outro colega ou de outro autor, tais como provindos de livros e
#apostilas, e páginas ou documentos eletrônicos da internet. Qualquer trecho de código
#de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
#do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.

#Bibliotecas
import os
import time
import random
import curses

#Função para criar o tabuleiro:
def criar_tabuleiro():
    tabuleiro = []
    for i in range(20):
        linha = []  
        for j in range(10):
            linha.append("⬛") 
        tabuleiro.append(linha)
    return tabuleiro

tabuleiro = criar_tabuleiro()

#Função para exibir o tabuleiro:
def exibir_tabuleiro(win, tabuleiro):
    win.clear() #Função para limpar o terminal
    for i, linha in enumerate(tabuleiro):
        win.addstr(i, 0, ''.join(linha))
    win.refresh()


#Definindo as peças:
I = [['🟩', '🟩', '🟩', '🟩']]

O = [['🟩', '🟩'],['🟩', '🟩']]

T = [['🟩', '🟩', '🟩'],['⬛', '🟩', '⬛']]

S = [['⬛', '🟩', '🟩',],['🟩', '🟩', '⬛']]

Z = [['🟩', '🟩', '⬛'],['⬛', '🟩', '🟩']]

J = [['🟩', '⬛', '⬛'],['🟩', '🟩', '🟩']]

L = [['⬛', '⬛', '🟩'],['🟩', '🟩', '🟩']]

BOMBA = [['🟦']]

#Variável para armazenar as peças:
pecas = [I,O,T,S,Z,J,L,BOMBA]

#Função para escolher uma peça aleatória:
def escolha():
    return random.choice(pecas)
peca = escolha()

#Função para verificar se a peça cabe e se a peça não ultrapassará o limite do tabuleiro:
def verificar_colisao(tabuleiro, peca, posicao):
    # Verifica se a peça está dentro dos limites do tabuleiro
    if posicao[0] < 0 or posicao[1] < 0 or posicao[0] + len(peca) > len(tabuleiro) or posicao[1] + len(peca[0]) > len(tabuleiro[0]):
        return False

    for i in range(len(peca)):
        for j in range(len(peca[i])):
            if peca[i][j] != "⬛":
                if (posicao[0] + i >= len(tabuleiro) or
                        posicao[1] + j >= len(tabuleiro[0]) or
                        tabuleiro[posicao[0] + i][posicao[1] + j] != "⬛"):
                    return False
    return True


# Função para colocar a peça:
def colocar_peca(tabuleiro, peca, posicao):
    if verificar_colisao(tabuleiro, peca, posicao):
        for i in range(len(peca)):
            for j in range(len(peca[i])):
                if peca[i][j] != '⬛':
                    tabuleiro[posicao[0] + i][posicao[1] + j] = peca[i][j]
                

#Função para remover a peça do tabuleiro:
def remover_peca(tabuleiro, peca, posicao):
    for i in range(len(peca)):
        for j in range(len(peca[i])):
            if (posicao[0] + i >= 0 and posicao[0] + i < len(tabuleiro) and
                posicao[1] + j >= 0 and posicao[1] + j < len(tabuleiro[0])):
                if tabuleiro[posicao[0] + i][posicao[1] + j] == peca[i][j]:
                    tabuleiro[posicao[0] + i][posicao[1] + j] = "⬛"

# Função para rotacionar as peças:
def rotacionar_pecas(tabuleiro, peca, posicao):
    rot_peca = [list(row) for row in zip(*peca[::-1])]  # Rotaciona a peça
    if verificar_colisao(tabuleiro, rot_peca, posicao):  # Verifica colisão
        return rot_peca  # Retorna a nova peça rotacionada se não houver colisão
    return peca  # Retorna a peça original se houver colisão


#Função para limpar a linha, descer as linhas acima e calcular a pontuação:
def limpar_linha(tabuleiro):
    linhas_ocupadas = 0
    novas_linhas = []
    #Verificação para ver se tem alguma linha completa:
    for linha in (tabuleiro):
        if all(celula == "🟩" for celula in linha):
            linhas_ocupadas += 1
        else:
            novas_linhas.append(linha)

    #Código para descer a linha e adicionar:
    for _ in range(linhas_ocupadas):
        novas_linhas.insert(0, ["⬛"] * len(tabuleiro[0]))

    for i in range(len(novas_linhas)):
        tabuleiro[i] = novas_linhas[i]

    #Sistema de Pontuação:
    return linhas_ocupadas * (linhas_ocupadas * 100)

def detonar_bomba(tabuleiro, posicao):
    for i in range(-2,1):
        for j in range(-1,2):
            area1 = i + posicao[0]
            area2 = j + posicao[1]
            if 0 <= area1 < len(tabuleiro) and 0 <= area2 < len(tabuleiro[0]):
                tabuleiro[area1][area2] = '⬛'
    return tabuleiro

#Função de Game Over caso a peça ultrapasse o limite:
def game_over(tabuleiro, peca, posicao):
    for i in range(len(tabuleiro[0])):
        if tabuleiro[0][i] != "⬛":
            return True
    return False

def jogo(win):
    jogo_ativo = True
    curses.curs_set(0)  #Oculta o cursor
    win.nodelay(1)      #Não espera por uma tecla
    coluna = random.randint(0, 9)
    peca = escolha()
    posicao = [0, coluna]
    pontuacao = 0
    pontuacaofinal = 0
    
    while jogo_ativo:
        #Código para rotacionar a peça e mover:
        tecla = win.getch()
        nova_posicao = posicao.copy()

        #Código para rotacionar e mover as peças:
        if tecla == 32:  #Código ASCII para a tecla de espaço
            nova_peca = rotacionar_pecas(tabuleiro, peca, posicao)
            if nova_peca != peca:
                peca = nova_peca
                remover_peca(tabuleiro, peca, posicao)

        elif tecla == curses.KEY_LEFT:
            nova_posicao[1] -= 1
            if verificar_colisao(tabuleiro, peca, nova_posicao):
                remover_peca(tabuleiro, peca, posicao)
                posicao[1] = nova_posicao[1] 

        elif tecla == curses.KEY_RIGHT:
            nova_posicao[1] += 1
            if verificar_colisao(tabuleiro, peca, nova_posicao):
                remover_peca(tabuleiro, peca, posicao)
                posicao[1] = nova_posicao[1]

        elif tecla == curses.KEY_DOWN:
            nova_posicao[0] += 1
            if verificar_colisao(tabuleiro, peca, nova_posicao):
                remover_peca(tabuleiro, peca, posicao)
                posicao[0] = nova_posicao[0]
        exibir_tabuleiro(win, tabuleiro)
    
        #Código para fazer a peça cair:
        if verificar_colisao(tabuleiro, peca, posicao):
            colocar_peca(tabuleiro, peca, posicao)
            exibir_tabuleiro(win,tabuleiro)
            time.sleep(0.4)
            remover_peca(tabuleiro, peca, posicao)
            posicao[0] += 1
        else:
            #Código para explodir a peça bomba caso tenha:
            if peca == BOMBA and len(peca) <= len(tabuleiro) or peca == BOMBA and tabuleiro[posicao[0]][posicao[1]] != "⬛":
                detonar_bomba(tabuleiro, posicao)
                peca = "⬛"

            #Código para fixar a peça caso tenha uma peça na posição abaixo ou estiver no fundo do tabuleiro:    
            posicao[0] -= 1
            colocar_peca(tabuleiro, peca, posicao)
            exibir_tabuleiro(win,tabuleiro)

            coluna = random.randint(0, 9)
            peca = escolha()
            posicao = [0, coluna]

            if game_over(tabuleiro, peca, posicao):
                print("GAME OVER")
                jogo_ativo = False
        #Calcular e exibir pontuação:
        pontuacao = limpar_linha(tabuleiro)
        pontuacaofinal += pontuacao
        win.addstr(21, 0, f'SUA PONTUAÇÂO: {pontuacaofinal}')
        win.refresh()
       
curses.wrapper(jogo)