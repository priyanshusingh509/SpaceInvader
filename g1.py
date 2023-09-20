# Importing reqired libraries
import pygame
from random import randint

# Initialization
game = "start"
pygame.init()
screen = pygame.display.set_mode((800,600))     # Resolution
pygame.display.set_caption("Space Invaders")    # Title/Caption
icon = pygame.image.load("assets/g1_logo.png")  # Logo
pygame.display.set_icon(icon)
bg = pygame.image.load("assets/Background.png") # Background
end = pygame.image.load("assets/End.png")

# Shooter
shooter = pygame.image.load("assets/space_shooter.png")    # Shooter_Icon
shooter_x = 370
shooter_y = 500
shooter_change = 0

# Enemy
enemy = []
enemy_x = []
enemy_y = []
enemy_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemy.append(pygame.image.load("assets/enemy.png"))
    enemy_x.append(randint(0,736))
    enemy_y.append(10)
    enemy_change.append(0.1)

# Bullet
bullet = pygame.image.load("assets/bullet.png")
bullet_x = shooter_x
bullet_y = 500
bullet_change = 2
bullet_state = "Ready"

#Score
score_value = 0
font = pygame.font.Font("ka1.ttf",10)
fontx = 10
fonty = 10
# Logic

# Player Logic
def shoot(x,y):
    screen.blit(shooter,(x,y))

#Enemy Logic
def enemy_func(x,y,i):
    screen.blit(enemy[i], (x,y))

# Bullet Logic
def fire(x,y):
    global bullet_state
    bullet_state = "Fired"
    screen.blit(bullet, (x + 16, y - 20))

# Score
def show_score(x,y):
    score = font.render("Score: "+str(score_value), True, (255,255,255) )
    screen.blit(score, (x,y))

def game_over():
    font2 = pygame.font.Font("ka1.ttf",30)
    val = score_value
    text1 = font2.render("Game Over  Score: "+str(val),True,("white"))
    screen.blit(text1,(250,200))

# Game
running = True
while running:
    for event in pygame.event.get():

        # Close Game
        if event.type == pygame.QUIT:
            running = False

        #Key Press
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                ec = enemy_change.copy()
                sc = shooter_change
                bc = bullet_change
                enemy_change = [0,0,0,0,0,0]
                shooter_change = 0
                bullet_change = 0
            
            if event.key == pygame.K_KP_ENTER:
                enemy_change = ec
                shooter_change = sc
                bullet_change = bc
            
            #Player Movement
            if event.key == pygame.K_LEFT:
                shooter_change = -0.9
            
            if event.key == pygame.K_RIGHT:
                shooter_change = 0.9

            # Bullet Movement
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    bullet_x = shooter_x
                    fire(bullet_x,bullet_y)
                

        # Player Stop
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                shooter_change = 0

    #Screen Design
    screen.fill("black")
    screen.blit(bg, (0,0))

    # Shooter Movement and Boundaries
    shoot(shooter_x,shooter_y)
    shooter_x += shooter_change
    if shooter_x > 800:
        shooter_x =- 64
    
    if shooter_x < -64:
        shooter_x = 800

    # Enemy Movement
    for i in range(num_of_enemies):
        enemy_func(enemy_x[i],enemy_y[i],i)
        enemy_y[i] += enemy_change[i]
        
        if (bullet_x - enemy_x[i] < 40 and  bullet_x - enemy_x[i] > -40) or (enemy_x[i] - bullet_x < 40 and enemy_x[i] - bullet_x > -40):
            if (bullet_y - enemy_y[i] < 40 and  bullet_y - enemy_y[i] > -40) or (enemy_y[i] - bullet_y < 40 and enemy_y[i] - bullet_y > -40):
                enemy_x[i] = randint(0,736)
                enemy_y[i] = -50
                bullet_y = 500
                bullet_state = "Ready" 
                score_value += 1
        
        if enemy_y[i] > 450:
            enemy_change[i] = 0
            game = "end"
    
    # Bullet Movement
    if bullet_state == "Fired":
        fire(bullet_x, bullet_y)
        bullet_y -= bullet_change
    if bullet_y == 0:
        bullet_state = "Ready"
        bullet_x = 0
        bullet_y = 500

    show_score(fontx,fonty)

    if game == "end":
        screen.fill("black")
        game_over()
    
    pygame.display.update()