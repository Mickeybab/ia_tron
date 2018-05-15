import sys
import math

MAX_Y = 20
MAX_X = 30

tab = [[False] * MAX_X for i in range(MAX_Y)]
tab_temp = [[False] * MAX_X for i in range(MAX_Y)]
head_ennemy = [0, 0]
last_ennemy = [0, 0]
x, y, x_depart, y_depart = 0, 0, 0, 0
direction = 3
max_val = 0
# direction 0: UP  1: DOWN  2: RIGHT  3: LEFT  4: UP

# Fonction
def detect_dir(direction):
    return {
        0 : "RIGHT",
        1 : "DOWN",
        2 : "LEFT",
        3 : "UP",
    }[direction]

def detect_direction_ennemy():
    if last_ennemy[0] == head_ennemy[0] - 1:
        return 1
    if last_ennemy[0] == head_ennemy[0] + 1:
        return 3
    if last_ennemy[1] == head_ennemy[1] - 1:
        return 0
    if last_ennemy[1] == head_ennemy[1] + 1:
        return 2

def recursive_traking(my_y, my_x, val):
    global tab, tab_temp, is_here, head_ennemy
    if my_y == head_ennemy[0] and my_x == head_ennemy[1]:
        is_here = 1
    if my_y < 0 or my_x < 0 or my_y >= MAX_Y or my_x >= MAX_X:
        return val
    if tab[my_y][my_x] == True or tab_temp[my_y][my_x] == True:
        return val
    tab_temp[my_y][my_x] = True
    for i in range(4):
        if i == 0:
            val = recursive_traking(my_y, my_x - 1, val + 1)
        if i == 1:
            val = recursive_traking(my_y - 1, my_x, val + 1)
        if i == 2:
            val = recursive_traking(my_y, my_x + 1, val + 1)
        if i == 3:
            val = recursive_traking(my_y + 1, my_x, val + 1)
    return val

def count_possibility(y_plus, x_plus):
    global tab, x, y, tab_temp, is_here
    is_here = 0
    direction_ennemy = detect_direction_ennemy()
    print("Debug console", direction_ennemy, file=sys.stderr)
    tab_temp = [[False] * MAX_X for i in range(MAX_Y)]
    if direction_ennemy == 0:
        x_temp = head_ennemy[1]
        while x_temp < x:
            tab_temp[head_ennemy[0]][x_temp] = True
            x_temp += 1
    elif direction_ennemy == 1:
        y_temp = head_ennemy[0]
        while y_temp < y:
            tab_temp[y_temp][head_ennemy[1]] = True
            y_temp += 1
    elif direction_ennemy == 2:
        x_temp = head_ennemy[1]
        while x_temp > x:
            tab_temp[head_ennemy[0]][x_temp] = True
            x_temp -= 1
    elif direction_ennemy == 3:
        y_temp = head_ennemy[0]
        while y_temp > y:
            tab_temp[y_temp][head_ennemy[1]] = True
            y_temp -= 1
    val = recursive_traking(int(y + y_plus), int(x + x_plus), 0)
    if is_here == 0:
        return val
    else:
        return (val / 2)

def check_all():
    global direction, tab, x, y
    if direction == 0:
        one = count_possibility(-1, 0)
        two = count_possibility(0, 1)
        tree = count_possibility(1, 0)
        if one > two and one > tree:
            direction = 3
        if tree > one and tree > two:
            direction = 1
    elif direction == 1:
        one = count_possibility(0, 1)
        two = count_possibility(1, 0)
        tree = count_possibility(0, -1)
        if one > two and one > tree:
            direction = 0
        if tree > one and tree > two:
            direction = 2
    elif direction == 2:
        one = count_possibility(-1, 0)
        two = count_possibility(0, -1)
        tree = count_possibility(1, 0)
        if one > two and one > tree:
            direction = 3
        if tree > one and tree > two:
            direction = 1
    elif direction == 3:
        one = count_possibility(0, 1)
        two = count_possibility(-1, 0)
        tree = count_possibility(0, -1)
        if one > two and one > tree:
            direction = 0
        if tree > one and tree > two:
            direction = 2

def check_left_or_right():
    global direction, tab, x, y
    if direction == 0 or direction == 2:
        weight = count_possibility(-1, 0)
        weight2 = count_possibility(1, 0)
        if weight > weight2 and tab[y - 1][x] == False:
            direction = 3
        elif tab[y + 1][x] == False:
            direction = 1
        else:
            direction = 3
    elif direction == 1 or direction == 3:
        weight = count_possibility(0, -1)
        weight2 = count_possibility(0, 1)
        if weight > weight2 and tab[y][x - 1] == False:
            direction = 2
        elif tab[y][x + 1] == False:
            direction = 0
        else:
            direction = 2

def check_hitbox():
    global direction, tab, x, y
    if direction == 0 and (x >= MAX_X - 1 or tab[y][x + 1] == True):
        check_left_or_right()
    elif direction == 1 and (y >= MAX_Y - 1 or tab[y + 1][x] == True):
        check_left_or_right()
    elif direction == 2 and (x <= 0 or tab[y][x - 1] == True):
        check_left_or_right()
    elif direction == 3 and (y <= 0 or tab[y - 1][x] == True):
        check_left_or_right()
    else:
        check_all()

# game loop
while True:
    # n: total number of players (2 to 4).
    # p: your player number (0 to 3).
    # Recuperation des infos
    n, p = [int(i) for i in input().split()]
    for i in range(n):
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        if i == p:
            x, y, x_depart, y_depart = int(x1), int(y1), int(x0), int(y0)
        else:
            last_ennemy[0], last_ennemy[1] = head_ennemy[0], head_ennemy[1]
            head_ennemy[0] = y1
            head_ennemy[1] = x1
        tab[y1][x1] = True
        tab[y0][x0] = True

    # Algo
    check_hitbox()
    print(detect_dir(direction))
