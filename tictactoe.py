import pygame as pg
import sys
from pygame.color import THECOLORS

from players import TEAMS, check_player

pg.init()
pg.font.init()

#окно
screen = pg.display.set_mode((1200, 900))
pg.display.set_caption("Football x TicTacToe ")
clock = pg.time.Clock()

#шрифт
font = pg.font.SysFont('helvetica', 60)
def make_font(size):
    return pg.font.SysFont('helvetica', size)
mid_font = make_font(44)
small_font = make_font(36)

#цвета
purple = (177, 144, 217)
red = (224, 62, 62)
blue = (62, 148, 224)
bg = (247, 247, 204)


#переменные
X0 = -1 # -1 - крестик, 1 - нолик
move = None #ячейка
winner = None
draw = False
used_players = set()
message = ''
message_until = 0

#значения в полях
TTT = [0,0,0,
       0,0,0,
       0,0,0]


#координаты, куда вставлять крестик/нолик
positions = {
    0: (335, 235),
    1: (502, 235),
    2: (669, 235),

    3: (335, 402),
    4: (502, 402),
    5: (669, 402),

    6: (335, 569),
    7: (502, 569),
    8: (669, 569)
    }

def get_nickname(number):
    nickname = ''
    entering = True
    while entering:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if nickname != '':
                        entering = False
                elif event.key == pg.K_BACKSPACE:
                    nickname = nickname[:-1]
                elif event.unicode.isprintable() and len(nickname) < 12:
                    nickname += event.unicode
        screen.fill(bg)
        if number == 1:
            text = font.render('Enter player 1 nickname', True, THECOLORS['black'])
        else:
            text = font.render('Enter player 2 nickname', True, THECOLORS['black'])
        screen.blit(text, (250, 300))

        name_text = font.render(nickname, True, purple)
        screen.blit(name_text, (250, 400))
        pg.display.flip()
        clock.tick(60)
    return nickname   

 
def draw_field():
    screen.fill(bg)

    x = font.render(f'X: ', True, red)
    player1_text = font.render(player1, True, THECOLORS['black'])
    o = font.render(f'0: ', True, blue)
    player2_text = font.render(player2, True, THECOLORS['black'])
    screen.blit(x, (315, 70))
    screen.blit(player1_text, (378, 70))
    screen.blit(o, (615, 70))
    screen.blit(player2_text, (678, 70))

    #столбцы
    barca = pg.image.load("fcb.png").convert_alpha()
    barca = pg.transform.scale(barca, (50, 50))
    screen.blit(barca, (367, 140))
    rm = pg.image.load("Real_Madrid.png").convert_alpha()
    rm = pg.transform.scale(rm, (60, 60))
    screen.blit(rm, (532, 130))
    mu = pg.image.load("Manchester_United.png").convert_alpha()
    mu = pg.transform.scale(mu, (50, 50))
    screen.blit(mu, (700, 140))

    #строки
    ch = pg.image.load("Chelsea_FC.png").convert_alpha()
    ch = pg.transform.scale(ch, (50, 50))
    screen.blit(ch, (240, 265))
    psg = pg.image.load("Paris_Saint-Germain.png").convert_alpha()
    psg = pg.transform.scale(psg, (50, 50))
    screen.blit(psg, (240, 420))
    ju = pg.image.load("ju.png").convert_alpha()
    ju = pg.transform.scale(ju, (50, 50))
    screen.blit(ju, (240, 586))


    #поле
    field = pg.Rect(300, 200, 500, 500)
    pg.draw.rect(screen, THECOLORS['black'], field, 4)
    points_str1 = [(300, 367), (800, 367)]
    points_row1 = [(467, 200), (467, 700)]
    points_str2 = [(300, 534), (800, 534)]
    points_row2 = [(634, 200), (634, 700)]
    pg.draw.lines(screen, THECOLORS['black'], True, points_str1, 3)
    pg.draw.lines(screen, THECOLORS['black'], True, points_row1, 3)
    pg.draw.lines(screen, THECOLORS['black'], True, points_str2, 3)
    pg.draw.lines(screen, THECOLORS['black'], True, points_row2, 3)

    #draw_legend()
    draw_turn()

"""def draw_legend():
    title = small_font.render('Teams:', True, THECOLORS['black'])
    screen.blit(title, (860, 200))
    for num, name in TEAMS.items():
        text = small_font.render(f'{num} - {name}', True, purple)
        screen.blit(text, (860, 250 + (num - 1) * 50))"""

def draw_turn():
    if winner is not None or draw:
        return
    name = player1 if X0 == -1 else player2
    color = red if X0 == -1 else blue
    text = small_font.render(f'Turn: {name}', True, color)
    screen.blit(text, (300, 730))

    if pg.time.get_ticks() < message_until:
        msg = small_font.render(message, True, THECOLORS['black'])
        screen.blit(msg, (300, 780))


def user_click():
    global move
    move = None
    #по координатам
    x, y = pg.mouse.get_pos()
    #первая строка
    if (199 < y < 368) and (299 < x < 468):
        move = 0
    elif (199 < y < 368) and (467 < x < 635):
        move = 1
    elif (199 < y < 368) and (634 < x < 801):
        move = 2

    #вторая строка
    elif (367 < y < 535) and (299 < x < 468):
        move = 3
    elif (367 < y < 535) and (467 < x < 635):
        move = 4
    elif (367 < y < 535) and (634 < x < 801):
        move = 5
        
    #третья строка
    elif (534 < y < 701) and (299 < x < 468):
        move = 6
    elif (534 < y < 701) and (467 < x < 635):
        move = 7
    elif (534 < y < 701) and (634 < x < 801):
        move = 8

    return move

def ask_player(team_a, team_b):
    text = ''
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if text.strip() != '':
                        return text
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                elif event.unicode.isprintable() and len(text) < 24:
                    text += event.unicode
        draw_field()
        draw_moves()

        ans_window = pg.Surface((800, 300))
        ans_window.fill(THECOLORS['white'])
        ans_window = add_border_to_surface(ans_window, THECOLORS['black'], 4)
        screen.blit(ans_window, (150, 300))

        title = mid_font.render(f'{team_a} x {team_b}', True, purple)
        screen.blit(title, title.get_rect(center=(550, 360)))
        hint = small_font.render('Write a name and surname', True, THECOLORS['black'])
        screen.blit(hint, hint.get_rect(center=(550, 415)))

        input_rect = pg.Rect(200, 470, 700, 70)
        pg.draw.rect(screen, THECOLORS['black'], input_rect, 3)
        typed = mid_font.render(text, True, THECOLORS['black'])
        screen.blit(typed, (input_rect.x + 15, input_rect.y + 15))

        pg.display.flip()
        clock.tick(60)

def try_move(move):
    global X0, message, message_until
    col, row = move % 3, move // 3
    team_a, team_b = col + 1, row + 4

    answer = ask_player(TEAMS[team_a], TEAMS[team_b])
    if answer is None:
        return
    status, name = check_player(answer, team_a, team_b, used_players)
    if status == 'ok':
        used_players.add(name)
        make_move(move)
        check_win()
    else:
        message = 'Already used :(' if status == 'used' else 'Wrong !'
        message_until = pg.time.get_ticks() + 1800
        X0 = -1 * X0

def make_move(move): 
    global TTT, X0

    TTT[move] = X0
    
    #смена игрока
    X0 = -1 * X0

def draw_moves():
    global X0, move, positions

    for i in range(9):
        if TTT[i] != 0:
            posx, posy = positions[i]
            if TTT[i] == -1:
                pg.draw.line(screen, red, (posx, posy), (posx + 100, posy + 100), 8)
                pg.draw.line(screen, red, (posx + 100, posy), (posx, posy + 100), 8)
            else:
                pg.draw.circle(screen, blue, (posx + 50, posy + 50), 50, 6)
    

def check_win():
    global winner, draw
    combinations = [
            #по строкам 
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),

            #по столбцам
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),

            #по диагонали
            (0, 4, 8),
            (2, 4, 6)

    ]
    for a, b, c in combinations:
        if TTT[a] == TTT[b] == TTT[c] and TTT[a] != 0:
            winner = TTT[a] #-1 или 1
            return

    if 0 not in TTT:
        draw = True

def restart_game():
    global TTT, X0, move, winner, draw, used_players, message_until
    TTT = [0, 0, 0,
           0, 0, 0,
           0, 0, 0]
    X0 = -1
    move = None
    winner = None
    draw = False
    used_players = set()
    message_until = 0

#обводка
def add_border_to_surface(surface, border_color, border_width):
  w, h = surface.get_size()
  
  new_surf = pg.Surface(
      (w + border_width * 2, h + border_width * 2), pg.SRCALPHA
  )
  
  pg.draw.rect(
      new_surf, border_color, (0, 0, w + border_width * 2, h + border_width * 2), border_width
  ) 
  new_surf.blit(surface, (border_width, border_width))
  return new_surf

def draw_window():
    global winner
    #окно в конце
    res_surf = pg.Surface((800, 300))
    res_surf.fill(THECOLORS['white'])
    res_surf = add_border_to_surface(res_surf, THECOLORS['black'], 4)   
    line1 = font.render('press ENTER for new game', True, THECOLORS['black'])
    line2 = font.render('or ESC to exit', True, THECOLORS['black'])

    
    screen.blit(res_surf, (146, 300))
    if winner != None:
        res = f'winner is {player1} !' if winner == -1 else f'winner is {player2} !'
        res = font.render(res, True, THECOLORS['black'])
        res_rect = res.get_rect(center=(550, 400))
        screen.blit(res, res_rect)
        restart_rect = line1.get_rect(center=(550, 500))
        screen.blit(line1, restart_rect)
        exit_rect = line2.get_rect(center=(550, 550))
        screen.blit(line2, exit_rect)

    else:
        res = font.render('draw !', True, THECOLORS['black'])
        res_rect = res.get_rect(center=(550, 400))
        screen.blit(res, res_rect)  
        restart_rect = line1.get_rect(center=(550, 500))                
        screen.blit(line1, restart_rect)
        exit_rect = line2.get_rect(center=(550, 550))
        screen.blit(line2, exit_rect)

player1 = get_nickname(1)
player2 = get_nickname(2)
draw_field()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            if winner is None and not draw:
                move = user_click()
                if TTT[move] == 0:
                    try_move(move)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.key == pg.K_RETURN:
                if winner is not None or draw:
                    restart_game()
    
    draw_field()
    draw_moves()
    if winner is not None or draw:
        draw_window()
    pg.display.flip()
    clock.tick(60)

