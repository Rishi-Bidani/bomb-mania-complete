import pygame
import random
import math
import pickle
import os
from os import path

pygame.mixer.init()
pygame.font.init()
save_data = {}
# upgrade data = {}

if path.exists('savegame'):
    # print("reached1")
    with open("savegame", "rb") as f:
        save_data = pickle.load(f)

if not path.exists('savegame'):
    # print("reached")
    with open("savegame", "wb") as f:
        save_data = {"cash": 0, "bestkills": 0, "upgrades_landmine": False}
        pickle.dump(save_data, f)



width = 900
height = 600

screen = pygame.display.set_mode([width, height])

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]

walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

char = pygame.image.load('standing.png')
bomb_pic = pygame.transform.scale(pygame.image.load('bomb.png'), (20, 20))
bomb_explosion = pygame.transform.scale(pygame.image.load('explosion1.png'), (40, 40))
landmine_upgrade = pygame.transform.scale(pygame.image.load("landmine.png"), (100,100))
landmine_drop = pygame.transform.scale(pygame.image.load("landmine.png"), (20, 20))

pics = [bomb_pic, bomb_explosion]
shop = pygame.transform.scale(pygame.image.load("shop.png"), (60, 60))
# boss = pygame.image.load("enemyboss.png")

player = [walkLeft, walkRight, char]

# enemy_Left = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
#               pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
#               pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png')]
enemy_pic = pygame.image.load('L1E.png')

# boss = pygame.image.load('pixel_monster.png')
cannon = pygame.image.load('tank_cannon.png')
bullet = pygame.image.load('bullet.png')

position = [60, 60]
x = 50  # same as position
y = 50  # same as position
width = 40
height = 60
vel = 5
isJump = False
jumpCount = 10
left = False
right = False
down = False
up = False
walkCount = 0
run_once = False

enemy_list = []
num_enemies = 5

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font('freesansbold.ttf', 32)
font_large = pygame.font.Font('freesansbold.ttf', 45)
items_font = pygame.font.Font('freesansbold.ttf', 16)
font_small = pygame.font.Font('freesansbold.ttf', 18)
font_tiny = pygame.font.Font('freesansbold.ttf', 13)
font_verytiny =pygame.font.Font('freesansbold.ttf', 9)
normal_txt = pygame.font.SysFont('comicsans', 40)
normal_txt_small = pygame.font.SysFont('comicsans', 24)

bombs = []
explosions = []

bag = {'bomb': 0, 'heal': 0, 'cannon': 1    , 'money': 500, 'landmine': 0}

health = 100
base_health = 150
normal_enemies = []
kills = 0
cannon_list = []
bullet_list = []
landmine_list = []

cash_pic = pygame.image.load("pixel_money.png")
num_check = 0


class Fonts():
    def __init__(self, font, antialias, text, color, x, y ):
        self.font = font
        self.antialias = antialias
        self.text = text
        self.color = color
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(self.font.render(self.text, self.antialias, (self.color)), (self.x, self.y))


class DrawRectangles():
    def __init__(self, win, color, width, height, x, y):
        self.win = win
        self. color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(self.win, (self.color), (self.x, self.y, self.width, self.height))

    def healthBarRed(self, width_new, height_new):
        self.width_new = width_new
        self.height_new = height_new
        pygame.draw.rect(self.win, (220, 0, 0), (self.x, self.y, self.width_new, self.height_new))

    def healthBarGreen(self, change_green_width = 1, change_green_height = 1):
        self.change_green_width = change_green_width
        self.change_green_height = change_green_height
        pygame.draw.rect(self.win, (0, 220, 0), (self.x, self.y, self.width * self.change_green_width, self.height * change_green_height))


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):

        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))



def shop_run():
    bright_green = (0, 255, 0)
    green = (0, 200, 0)

    shop_bomb = Button((0, 200, 0), 810, 150, 70, 20, text="Bomb_b")
    shop_bomb.draw(screen)

    shop_heal = Button((0, 200, 0), 810, 210, 70, 20, text="Heal_h")
    shop_heal.draw(screen)

    shop_cannon = Button((0, 200, 0), 810, 180, 70, 20, text="Cannon_c")
    shop_cannon.draw(screen)

    if save_data['upgrades_landmine']:
        shop_mine = Button(green, 810, 240, 70, 20, text = "Mine_m")
        shop_mine.draw(screen)


def walk():
    global walkCount
    global walkcount

    if walkCount + 1 >= 27:
        walkCount = 0

    if left:
        screen.blit(player[0][walkCount // 3], (x, y))
        walkCount += 1

    elif right:
        screen.blit(player[1][walkCount // 3], (x, y))
        walkCount += 1

    elif down:
        screen.blit(player[2], (x, y))
        walkcount = 0

    elif up:
        screen.blit(player[2], (x, y))
        walkcount = 0

    else:
        screen.blit(player[2], (x, y))
        walkCount = 0


def enemy_spawn(number_of_enemies):
    global normal_enemies
    global health
    global base_health
    global kills
    global bag
    global landmine
    global num_check

    # for random_velocity in range(number_of_enemies):
    player_rect = pygame.Rect(x+20, y+20, 20, 20)
    for ne in range(number_of_enemies):
        random_velocity = random.uniform(0.3, 1.3)
        random_enemy_location_y = random.randrange(170, 470)
        random_enemy_location_x = random.randrange(800, 1000)
        normal_enemies.append([random_enemy_location_x, random_enemy_location_y, random_velocity])
        # print(normal_enemies[ne][0], normal_enemies[ne][1], normal_enemies[ne][2])


    for e in range(number_of_enemies):
        ex, ey, evel = normal_enemies[e]
        screen.blit(enemy_pic, (ex, ey))
        if ex > 75:
            normal_enemies[e][0] -= evel
        else:
            base_health -= 0.02

        normal_enemy_rect = pygame.Rect(ex, ey, 50, 50)

        if player_rect.colliderect(normal_enemy_rect):
            health -= 0.2

        for j in reversed(range(len(explosions))):
            pos, end_time_2, hurt = explosions[j]
            explosion_rect = pygame.Rect(pos[0], pos[1], 20, 20)
            if explosion_rect.colliderect(normal_enemy_rect):
                normal_enemies.pop(e)
                kills += 1
                num_check += 1
                bag['money'] += 15

        for l in reversed(range(len(landmine_list))):
            landmine_rect = pygame.Rect(landmine_list[l][0], landmine_list[l][1], 18, 18)
            if landmine_rect.colliderect(normal_enemy_rect):
                normal_enemies.pop(e)
                landmine_list.pop(l)
                kills += 1
                num_check += 1
                bag["money"] += 10

def redrawGameWindow():
    global walkCount
    global font
    global font_small
    global font_tiny
    global font_verytiny
    global bag
    global items_font
    global enemy_list
    global pics
    global position
    global health
    global base_health
    global run_once
    global explosions
    global bullet_list
    global normal_enemies
    global kills
    global counter
    global num_enemies
    global num_check

    current_time = pygame.time.get_ticks()
    dx = []
    dy = []
    dist = []
    screen.fill([166, 166, 166])

    # pygame.draw.rect(screen, (220, 0, 0), (700, 500, 100, 100))
    # for five_enemies in range(5):
    #     random_enemy_location_y = random.randrange(170, 470)
    #     random_enemy_location_x = random.randrange(700, 840)
    #     enemy_list.append([random_enemy_location_x, random_enemy_location_y])

    # for enemies in range(5):
    #     screen.blit(enemy_Left[enemies], enemy_list[enemies])
    #     dx.append(position[0] - enemy_list[enemies][0])
    #     dy.append(position[1] - enemy_list[enemies][1])
    #     dist.append(math.hypot(dx[enemies], dy[enemies]))
    #     dx[enemies], dy[enemies] = dx[enemies] / dist[enemies], dy[enemies] / dist[enemies]

    #     enemy_list[enemies][0] += dx[enemies] * 2
    #     enemy_list[enemies][1] += dy[enemies] * 2

    #------------------main base------------------------------
    main_base = DrawRectangles(screen, (70, 0, 220), 100, 400, 0, 120)
    main_base.draw()

    baseHealthBar = DrawRectangles(screen, (0,0,0), 5, -base_health,  50, 470)
    baseHealthBar.healthBarRed(5, -300)
    baseHealthBar.healthBarGreen(1, 2)
    #------------------------end main base ----------------------

    if num_check == 20: # increases the number of enemies by 1 after every 20 kills
        num_enemies += 1
        num_check = 0

    enemy_spawn(num_enemies)

    side_panel = DrawRectangles(screen, (0, 0, 0), 100, 600, 800, 0)
    side_panel.draw()

    if x + char.get_width() < 60 and y + char.get_height() < 60:
        shop_run()

    screen.blit(shop, (0, 0))

    #---------------------my health bar -----------------------------------
    myHealthBar = DrawRectangles(screen, (0,0,0), health, 5, position[0] - 3, position[1] )
    myHealthBar.healthBarRed(50, 5)
    myHealthBar.healthBarGreen((1/2), 1)
    #----------------------end my health bar ------------------------------------
    money_bg = DrawRectangles(screen, (179, 179, 0), 100, 40, 800, 560)
    money_bg.draw()
    #-----------------  Fonts -----------------------------------
    white = (255, 255, 255)

    shop_font = Fonts(font_small, True, "Shop", (0, 0, 0), 5, 5 )
    shop_font.draw(screen)

    base_B_font = Fonts(font, True, "B", (0, 0, 0), 10, 200 + 40 )
    base_B_font.draw(screen)

    base_A_font = Fonts(font, True, "A", (0, 0, 0), 10, 230 + 40 )
    base_A_font.draw(screen)

    base_S_font = Fonts(font, True, "S", (0, 0, 0), 10, 270 + 40 )
    base_S_font.draw(screen)

    base_E_font = Fonts(font, True, "E", (0, 0, 0), 10, 305 + 40 )
    base_E_font.draw(screen)

    menu_font = Fonts(font, True, "Menu", (255, 255, 255), 805, 10 )
    menu_font.draw(screen)

    bomb_font = Fonts(items_font, True, "Bombs: " + str(bag["bomb"]),(white), 805, 520)
    bomb_font.draw(screen)

    heal_font = Fonts(items_font, True, "Heal: " + str(bag["heal"]),(white), 805, 540)
    heal_font.draw(screen)

    cannon_font = Fonts(items_font, True, "Cannon: " + str(bag["cannon"]),(white), 805, 500)
    cannon_font.draw(screen)

    landmine_font = Fonts(items_font, True, "Mines:" + str(bag["landmine"]), (white), 805, 480)
    landmine_font.draw(screen)

    myHealth_font = Fonts(font_tiny, True, "Health: " + str("{:.2f}".format(health)),(white), 805, 60)
    myHealth_font.draw(screen)

    myMoney_font = Fonts(items_font, True, "$" + str(bag['money']), (white), 805, 570 )
    myMoney_font.draw(screen)

    baseHealth_font = Fonts(font_verytiny, True, "Base Health: " + str("{:.2f}".format(base_health)), (255, 255, 255), 805, 90)
    baseHealth_font.draw(screen)

    kills_font = Fonts(font_tiny, True, "Kills: " + str(kills), (255, 255, 255), 805, 115)
    kills_font.draw(screen)
    #------------------------end Fonts ----------------------------------------------

    walk()

    for i in reversed(range(len(bombs))):
        pos, end_time = bombs[i]
        if current_time > end_time:
            end_time_2 = end_time + 5000
            pos2 = (pos[0] - 10, pos[1] - 20)
            explosions.append((pos2, end_time_2, False))
            bombs.pop(i)
        else:
            screen.blit(pics[0], pos)

    for j in reversed(range(len(explosions))):
        pos, end_time_2, hurt = explosions[j]
        if current_time > end_time_2:
            explosions.pop(j)
        else:
            screen.blit(pics[1], pos)
            # crash_sound = pygame.mixer.Sound("bomb_sound_wav.wav")
            # pygame.mixer.Sound.play(crash_sound)

            if not hurt:
                explosion_rect = pygame.Rect(pos[0], pos[1], 20, 20)
                player_rect = pygame.Rect(x+20, y+20, 20, 20)
                if player_rect.colliderect(explosion_rect):
                    explosions[j] = (pos, end_time_2, True)
                    health -= 5

    #------------------cannon spawns cannon, bullets---- moves bullets --- resets bullets-----
    for j in reversed(range(len(bullet_list))):
        bx, by, track, oldx, endtime = bullet_list[j]
        if current_time > endtime:
            bullet_list.pop(j)
        #---------------------bullets disappear after 15 seconds --------------------------
        else:
            screen.blit(bullet, ((bullet_list[j][0]+20), (bullet_list[j][1]+30)))
            if bullet_list[j][2] <= 180:
                bullet_list[j][0] += 3
                bullet_list[j][2] += 3
            if bullet_list[j][2] >= 180:
                bullet_list[j][0] = bullet_list[j][3]
                bullet_list[j][2] = 0
        #------------------end bullet disappear after 15 seconds -----------------------

        bullet_rect = pygame.Rect((bx+20), (by+30), 8, 3)
        #------ getting enemy rect element--------------------
        number_of_enemies1 = 5
        for e in range(number_of_enemies1):
            ex, ey, evel = normal_enemies[e]
            normal_enemy_rect = pygame.Rect(ex, ey, 50, 50)
        #-------------------end get enemy rect element--------
            if bullet_rect.colliderect(normal_enemy_rect):
                normal_enemies.pop(e)
                kills += 1
                num_check += 1
                bag['money'] += 10


    #-----------------cannon disappear after 15 seconds -----------------------
    for i in reversed(range(len(cannon_list))):
        cx, cy, endtimecannon = cannon_list[i]
        if current_time > endtimecannon:
            cannon_list.pop(i)
        else:
            screen.blit(cannon, (cx, cy))
    #------------------------end cannons disppear after 15 seconds--------------
    #-----------------------------------------ended cannon and bullets -------------------------
    #----------------------lanmine dropping------------------------
    for l in landmine_list:
        screen.blit(landmine_drop, l)


    pygame.display.update()


def main():
    run = True
    pygame.display.set_caption("bomb-mania")

    global x
    global y
    global width
    global height
    global vel

    global left
    global right
    global down
    global up

    global walkCount

    global bomb_pic

    global font
    global bombs
    global explosions
    global position
    global health

    global kills
    global cannon_list
    global bullet_list

    global cash
    global save_data

    global num_check

    while run:
        current_time = pygame.time.get_ticks()
        redrawGameWindow()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                run = False


            shop_rect = pygame.Rect(0, 0, 40, 40)
            player_rect = pygame.Rect(x+20, y+20, 20, 20)

            if player_rect.colliderect(shop_rect):
                buy = pygame.key.get_pressed()
                if buy[pygame.K_b] and bag["money"] >= 10:
                    bag["bomb"] += 1
                    bag['money'] -= 10
                    # print(bag["bomb"])
                if buy[pygame.K_h] and bag["money"] >= 20:
                    bag["heal"] += 1
                    bag["money"] -= 20

                if buy[pygame.K_c] and kills > 3 and bag["money"] >= 30:
                    kills -= 3
                    bag["cannon"] += 1
                    bag["money"] -= 30
                    # print(bag["cannon"])
                if buy[pygame.K_m] and bag['money'] >= 25 and save_data['upgrades_landmine'] == True:
                    bag["landmine"] += 1
                    bag["money"] -= 25

            if event.type == pygame.KEYDOWN and not player_rect.colliderect(shop_rect):
                if (event.key == pygame.K_SPACE or event.key == pygame.K_b) and bag["bomb"] >= 1:
                    current_time_2 = pygame.time.get_ticks()
                    pos = x + char.get_width() / 2, y + char.get_height() - 20
                    pos2 = ((x + char.get_width() / 2) - 10), (y + char.get_height() - 30)
                    end_time = current_time + 3000  # 3000 milliseconds = 3 seconds
                    bombs.append((pos, end_time))
                    bag["bomb"] -= 1

                if event.key == pygame.K_h and not player_rect.colliderect(shop_rect) and health < 90 and bag["heal"] >= 1:
                    health += 10
                    bag["heal"] -= 1

                if event.key == pygame.K_c and not player_rect.colliderect(shop_rect) and bag["cannon"] >= 1:
                    # cannon_time = pygame.time.get_ticks()
                    cannon_end_time = current_time + 15000
                    cannon_list.append([x,y, cannon_end_time])
                    bullet_list.append([x,y,0, x, cannon_end_time])
                    bag["cannon"] -= 1

                if event.key == pygame.K_m and not player_rect.colliderect(shop_rect) and bag["landmine"] >= 1:
                    pos = x + char.get_width() / 2, y + char.get_height() - 20
                    landmine_list.append((pos))
                    bag["landmine"] -= 1

        if health <= 0 or base_health <= 0:
            save_data['cash'] += kills
            for j in reversed(range(len(bullet_list))):
                bullet_list.pop(j)
            save()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and x > vel - 15:
            x -= vel
            position[0] -= vel
            left = True
            right = False
            down = False
            up = False
            # print(position)

        elif keys[pygame.K_RIGHT] and x < 800 - vel - width:
            x += vel
            position[0] += vel
            left = False
            right = True
            down = False
            up = False
            # print(position)

        elif keys[pygame.K_DOWN] and y < 600 - height:
            y += vel
            position[1] += vel
            left = False
            right = False
            down = True
            up = False
            # print(position)

        elif keys[pygame.K_UP] and y > vel - 15:
            y -= vel
            position[1] -= vel
            left = False
            right = False
            down = False
            up = True
            # print(position)

        else:
            left = False
            right = False
            down = False
            up = False
            walkCount = 0

        clock.tick(FPS)
        pygame.display.flip()


def setDefaults():
    global health
    global base_health
    global bag
    global position
    global x
    global y
    global left
    global right
    global down
    global up
    global walkCount
    global normal_enemies
    global explosions
    global bombs
    global enemy_list
    global kills
    global cannon_list

    cannon_list =[]
    enemy_list = []
    normal_enemies = []
    bombs = []
    explosions = []
    position = [60, 60]
    x = 50  # same as position
    y = 50  # same as position
    left = False
    right = False
    down = False
    up = False
    walkCount = 0
    enemy_vel = 2
    enemy_list = []
    bag["bomb"] = 0
    bag["heal"] =0
    bag['money'] = 500
    bag['cannon'] = 1
    bag['landmine'] = 0
    health = 100
    base_health = 150



def upgrades():
    global save_data

    pygame.display.set_caption("Upgrades")
    run = True
    bright_green = (0, 255, 0)
    green = (0, 200, 0)
    screen.fill((163, 163, 194))
    while run:
        mousex, mousey = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                run = False
            #--------------------buttons---------------------------------back
            if 60 + 100 > mousex > 60 and 520 + 50 > mousey > 520:
                pygame.draw.rect(screen, bright_green, (60, 520, 100, 50))
                back = Fonts(normal_txt, True, "Back", (0, 0, 0), 76, 532)
                back.draw(screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_menu()
            else:
                pygame.draw.rect(screen, green, (60, 520, 100, 50))
                back = Fonts(normal_txt, True, "Back", (0, 0, 0), 76, 532)
                back.draw(screen)
            #--------------------------------------------------------------buy landmine
            if 100 + 110 > mousex > 100 and 120 + 40 > mousey > 120 and save_data['cash'] >= 200 and not save_data["upgrades_landmine"]:
                pygame.draw.rect(screen, bright_green, (100, 120, 110, 40))
                buy = Fonts(normal_txt, True, "Buy", (0, 0, 220), 125, 125)
                buy.draw(screen)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    save_data['upgrades_landmine'] = True
                    save_data['cash'] -= 200
                    with open("savegame", "wb") as f:
                        pickle.dump(save_data, f)

            elif save_data['cash'] < 200 and not save_data["upgrades_landmine"]:
                pygame.draw.rect(screen, (137, 138, 154), (100, 120, 110, 40))
                lock = Fonts(normal_txt, True, "Locked", (220, 0, 0), 105, 125)
                lock.draw(screen)

            elif save_data["upgrades_landmine"] == True:
                pygame.draw.rect(screen, (137, 138, 154), (100, 120, 110, 40))
                bought = Fonts(normal_txt, True, "Bought", (0, 0, 220), 105, 125)
                bought.draw(screen)

            else:
                pygame.draw.rect(screen, green, (100, 120, 110, 40))
                buy = Fonts(normal_txt, True, "Buy", (0, 0, 220), 125, 125)
                buy.draw(screen)
            #------------------------------------------------------------------

        screen.blit(landmine_upgrade, (100, 200))
        screen.blit(cash_pic, (70, 320))

        if not save_data["upgrades_landmine"]:
            landmine_price_unbought = Fonts(normal_txt, True, "200", (220, 0, 0), 160, 320)
            landmine_price_unbought.draw(screen)
        if save_data["upgrades_landmine"]:
            landmine_price_bought = Fonts(normal_txt, True, "200", (0, 220, 0), 160, 320)
            landmine_price_bought.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

def save():
    global save_data
    global kills

    if save_data['bestkills'] >= kills:
        pass
    else:
        save_data['bestkills'] = kills


    with open("savegame", "wb") as f:
        pickle.dump(save_data, f)
    # print(save_data)
    main_menu()

def main_menu():
    global kills
    global save_data
    new_kills = kills
    setDefaults()

    # print(save_data)
    pygame.display.set_caption("Main Menu")
    run = True
    bright_green = (0, 255, 0)
    green = (0, 200, 0)
    screen.fill((163, 163, 194))
    # pygame.mixer.music.load('background_music_wav.wav')
    # pygame.mixer.music.play(-1)

    while run:

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                run = False
        #------------------------------buttons----------------------------------------play
            if 360 + 175 > mouse[0] > 360 and 325 + 50 > mouse[1] > 325:
                pygame.draw.rect(screen, bright_green, (360, 325, 175, 50))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    kills = 0
                    main()
            else:
                pygame.draw.rect(screen, green, (360, 325, 175, 50))

            #-----------------------------------------------------------------upgrades
            if 600 + 175 > mouse[0] > 600 and 325 + 50 > mouse[1] > 325:
                pygame.draw.rect(screen, bright_green, (600, 325, 175, 50))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    upgrades()
            else:
                pygame.draw.rect(screen, green, (600, 325, 175, 50))

            #-----------------------------------------------------------------rules
            if 125 + 175 > mouse[0] > 125 and 325 + 50 > mouse[1] > 325:
                pygame.draw.rect(screen, bright_green, (125, 325, 175, 50))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()
            else:
                pygame.draw.rect(screen, green, (125, 325, 175, 50))
        #-----------------------------end buttons----------------------------------------
            screen.blit(cash_pic, (325, 125))
            screen.blit(normal_txt.render(str(save_data['cash']), True, (0, 0, 0)), (450, 125))
            screen.blit(font_large.render("Bomb-Mania", True, (255, 255, 255)), (325, 50))
            screen.blit(font.render("Play", True, (0, 0, 0)), (417, 335))
            screen.blit(font.render("Upgrades", True, (0, 0, 0)), (613, 335))
            screen.blit(font.render("Rules", True, (0, 0, 0)), (165, 335))
            screen.blit(normal_txt.render("Kills", True, (0, 0, 0)), (325, 175))
            screen.blit(normal_txt.render(str(new_kills), True, (0, 0, 0)), (450, 175))
            screen.blit(normal_txt.render("Best", True, (0, 0, 0)), (325, 225))
            screen.blit(normal_txt.render(str(save_data["bestkills"]), True, (0, 0, 0)), (450, 225))
            screen.blit(normal_txt.render("Made By: Rishi Bidani".rjust(4), True, (0, 0, 0)), (5, 5))

        pygame.display.flip()
        clock.tick(FPS)

main_menu()
