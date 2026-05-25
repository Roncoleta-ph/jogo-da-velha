import os
import sys
import pygame

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from jogo_da_velha import criar_board, faz_movimento, get_input_valido, \
    print_board, verifica_ganhador, verica_movimento

from minimax import movimento_ia, movimentoIA_facil, movimentoIA_medio

pygame.mixer.init()
try:
    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.play(-1) 
except:
    print("Aviso: Arquivo musica.mp3 não encontrado ou falhou ao carregar.")

pygame.font.init()

BG_COLOR = (28, 28, 28)
LINE_COLOR = (0, 255, 255)
TEXT_COLOR = (148, 0, 211)

def draw_board(win, board):
    height = 600
    width = 600
    tamanho = 200 
    
    for i in range(1, 3):
        pygame.draw.line(win, LINE_COLOR, (0, i * tamanho), (width, i * tamanho), 3)
        pygame.draw.line(win, LINE_COLOR, (i * tamanho, 0), (i * tamanho, height), 3)
        
    font = pygame.font.SysFont('comicsans', 100)
    for i in range(3):
        for j in range(3):
            x = j * tamanho
            y = i * tamanho

            if board[i][j] != " ":
                text = font.render(board[i][j], 1, TEXT_COLOR)
                win.blit(text, ((x + 65), (y + 40)))

def redraw_window(win, board, dificuldade):
    win.fill(BG_COLOR)
    draw_board(win, board)
    
   #font_diff = pygame.font.SysFont('comicsans', 25)
   #text_diff = font_diff.render(f"Dificuldade: {dificuldade}", 1, (148, 0, 211)) 
   #win.blit(text_diff, (15, 570))

def main():
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Jogo da Velha - IA")

    dificuldade = None
    escolhendo = True
    font_menu = pygame.font.SysFont('comicsans', 40)

    while escolhendo:
        win.fill(BG_COLOR)
        text1 = font_menu.render("Escolha a Dificuldade:", 1, TEXT_COLOR)
        text2 = font_menu.render("1 - Facil", 1, TEXT_COLOR)
        text3 = font_menu.render("2 - Medio", 1, TEXT_COLOR)
        text4 = font_menu.render("3 - Dificils", 1, TEXT_COLOR)
        
        win.blit(text1, (100, 150))
        win.blit(text2, (120, 240))
        win.blit(text3, (120, 300))
        win.blit(text4, (120, 360))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    dificuldade = "Facil"
                    escolhendo = False
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    dificuldade = "Medio"
                    escolhendo = False
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    dificuldade = "Dificil"
                    escolhendo = False

    board = criar_board()
    redraw_window(win, board, dificuldade)
    pygame.display.update()

    jogador = 0
    ganhador = verifica_ganhador(board)

    while(not ganhador):
        i = None
        j = None
        print_board(board)

        if jogador == 0:
            jogou = False

            while(not jogou):
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        pygame.quit()
                        sys.exit()
                    elif (event.type == pygame.MOUSEBUTTONUP):
                        pos = pygame.mouse.get_pos()
                        i = int(pos[1]/200)
                        j = int(pos[0]/200)
                        jogou = True
        else:
            if dificuldade == "Facil":
                i, j = movimentoIA_facil(board, jogador)
            elif dificuldade == "Medio":
                i, j = movimentoIA_medio(board, jogador)
            else:
                i, j = movimento_ia(board, jogador)

        if verica_movimento(board, i, j):
            faz_movimento(board, i, j, jogador)
            jogador = (jogador + 1) % 2

        ganhador = verifica_ganhador(board)
        redraw_window(win, board, dificuldade)
        pygame.display.update()

    font_final = pygame.font.SysFont('comicsans', 50)
    if ganhador == "EMPATE":
        resultado_txt = "O Jogo Empatou!"
    else:
        resultado_txt = f"Vencedor: {ganhador}"
        
    text_final = font_final.render(resultado_txt, 1, (255,255,0))
    win.blit(text_final, (160, 260))
    pygame.display.update()

    while(True):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()