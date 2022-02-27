import pygame
import random

pygame.init()
# managing fps
clock = pygame.time.Clock()
fps = 60

# game window
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Battle System')

current_Player = 1
total_Players = 3
action_cooldown = 0
action_wait_time = 90
attack = False
clicked = False
game_over = 0

# fonts
font = pygame.font.SysFont('Times New Roman', 26)

#colours
red = (255, 0, 0)
green= (0, 255, 0)

background = pygame.image.load('Final boss.PNG')
panel = pygame.image.load('panel.png')
sword = pygame.image.load('sword.png')


# printing images
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.blit(background, (0, 0))

def draw_panel():
    # panel rectangle
    screen.blit(panel, (0, 345))
    # stats for the knight and enemies
    draw_text(f'{Knight.name} HP: {Knight.hp}', font, red, 100, 345)
    draw_text(f'{Monsters1.name} HP: {Monsters1.hp}', font, red, 430, 349)
    draw_text(f'{Monsters2.name} HP: {Monsters2.hp}', font, red, 430, 410)


# player
class Player():
    def __init__(self, x, y, name, max_hp, strength):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # 0 is idle, 1 is attack.
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(6):
            Image = pygame.image.load(f'Images/{self.name}/Animations/PNG/idle {i}.png')
            Image = pygame.transform.scale(Image, (Image.get_width() * 3, Image.get_height() * 3))
            temp_list.append(Image)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(6):
            Image = pygame.image.load(f'Images/{self.name}/Animations/attack/Attack {i}.png')
            Image = pygame.transform.scale(Image, (Image.get_width() * 3, Image.get_height() * 3))
            temp_list.append(Image)
        self.animation_list.append(temp_list)
        self.Image = self.animation_list[self.action][self.frame_index]
        self.rect = self.Image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        animation_cooldown = 140
        # updating the image and handle animation
        self.Image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # animation resets back to the start if the animation runs out
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()



    def draw(self):
        screen.blit(self.Image, self.rect)


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # update with new health
        self.hp = hp
        # calculating the health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

Knight = Player(200, 260, 'Player', 100, 10)
Monsters1 = Player(550, 230, 'Capra Demon', 50, 10)
Monsters2 = Player(700, 240, 'Lost Soul', 20, 5)

Monsters_list = []
Monsters_list.append(Monsters1)
Monsters_list.append(Monsters2)

Knight_health_bar = HealthBar(100, 380, Knight.hp, Knight.max_hp)
Monsters1_health_bar = HealthBar(430, 380, Monsters1.hp, Monsters1.max_hp)
Monsters2_health_bar = HealthBar(430, 440, Monsters2.hp, Monsters2.max_hp)


# while loop
run = True
while run:

    clock.tick(fps)

    # drawing images
    draw_bg()
    draw_panel()

    #healthbar
    Knight_health_bar.draw(Knight.hp)
    Monsters1_health_bar.draw(Monsters1.hp)
    Monsters2_health_bar.draw(Monsters2.hp)


    Knight.update()
    Knight.draw()
    for Monsters in Monsters_list:
        Monsters.update()
        Monsters.draw()


    # controlling the player actions
    attack = False
    target = None
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, Monsters in enumerate(Monsters_list):
        if Monsters.rect.collidepoint(pos):
            #hide the mouse
            pygame.mouse.set_visible(False)
            #show the sword in place of mouse cursor
            screen.blit(sword, pos)
            if clicked == True:
                attack = True
                target = Monsters_list[count]


     # Player
    if Knight.alive == True:
        if current_Player == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                  if attack == True and target != None:
                    Knight.attack(target)
                    current_Player += 1
                    action_cooldown = 0

    # Monsters
        for count, Monsters in enumerate(Monsters_list):
            if current_Player == 2 + count:
                if Monsters.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        Monsters.attack(Knight)
                        current_Player += 1
                        action_cooldown = 0
                else:
                     current_Player += 1

        if current_Player > total_Players:
            current_Player = 1

     #checking if all Monsters are dead

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
         clicked = False



    pygame.display.update()