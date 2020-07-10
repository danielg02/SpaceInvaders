import pygame
import random
import math
from pygame import mixer

# Initialize pygame module
pygame.init()
clock = pygame.time.Clock()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Game Loading
load_font = pygame.font.Font(None, 40)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

enemy_startY = [0, 64, 128, 192]

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(enemy_startY[random.randint(0, 3)])
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - Can't see bullet on screen
# Fire - Bullet is in motion
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Game Over Text
over_font = pygame.font.Font('game_over.ttf', 200)

# Score
score_value = 0
font = pygame.font.Font('SPACE.ttf', 32)

textX = 15
textY = 550

# Text
# Game
over_font = pygame.font.Font('game_over.ttf', 200)
font = pygame.font.Font('SPACE.ttf', 32)
# Menu
titleFont = pygame.font.Font('game_over.ttf', 200)
titleText = titleFont.render("Space Invaders", True, (0, 255, 0))
titleText_rect = titleText.get_rect(center=(400, 250))
startFont = pygame.font.SysFont("Open Sans", 30, True)
startText = startFont.render("Start Game", True, (255, 255, 255))
startText_rect = startText.get_rect(center=(263, 430))
settingsFont = pygame.font.SysFont("Open Sans", 30, True)
settingsText = settingsFont.render("Settings", True, (255, 255, 255))
settingsText_rect = settingsText.get_rect(center=(538, 430))
# Settings
backFont = pygame.font.SysFont("Open Sans", 20, True)
backText = backFont.render("Back To Menu", True, (250, 250, 250))
backText_rect = backText.get_rect(center=(80, 560))

def reset_variables():
    global playerX, playerY, playerX_change, enemyX, enemyY, enemyX_change, enemyY_change
    global bulletX, bulletY, bullet_state, score_value
    # Player
    playerX = 370
    playerY = 480
    playerX_change = 0

    # Enemy
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []

    for i in range(num_of_enemies):
        enemyX.append(random.randint(0, 735))
        enemyY.append(enemy_startY[random.randint(0, 3)])
        enemyX_change.append(4)
        enemyY_change.append(40)

    # Bullet

    # Ready - Can't see bullet on screen
    # Fire - Bullet is in motion
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    score_value = 0

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def settings():
    running = True
    while running:
        screen.fill((230, 230, 230))
        pygame.draw.rect(screen, (0, 0, 0), (20, 540, 120, 40))
        screen.blit(backText, backText_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if (x < 140) and (x > 20) and (y < 580) and (y > 540):
                    running = False
                    break
        pygame.display.update()

def game_menu():
    running = True
    while running:
        screen.fill((255, 250, 250))
        pygame.draw.rect(screen, (255, 0, 0), (175, 400, 175, 60))
        pygame.draw.rect(screen, (0, 0, 250), (450, 400, 175, 60))
        screen.blit(titleText, titleText_rect)
        screen.blit(startText, startText_rect)
        screen.blit(settingsText, settingsText_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if (x < 350) and (x > 175) and (y < 460) and (y > 400):
                    game()
                    while restart:
                        reset_variables()
                        game_load()
                        game()
                    else:
                        running = False
                        break
                if (x < 625) and (x > 450) and (y < 460) and (y > 400):
                    settings()

        pygame.display.update()


def game_load():
    timer = 3
    dt = 0
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        timer -= dt
        if timer < 0:
            break
        screen.blit(background, (0, 0))
        time_txt = load_font.render(str(round(timer, 2)), True, (255, 255, 255))
        time_txt_rect = time_txt.get_rect(center=(400, 300))
        screen.blit(time_txt, time_txt_rect)
        pygame.display.update()
        dt = clock.tick(30) / 1000  # / 1000 to convert to seconds.

def game():
    global bullet_state
    global score_value
    global playerX
    global playerX_change
    global bulletX
    global bulletY

    game_load()

    # Game Loop
    running = True
    while running:

        # RGB - Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # if keystroke is pressed check whether it's right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        bullet_state = "fire"
                        screen.blit(bulletImg, (bulletX + 16, bulletY + 10))
                        bullet_Sound = mixer.Sound('laser.wav')
                        bullet_Sound.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):
            # Game Over
            if enemyY[i] > 416:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                over_text = over_font.render("GAME OVER", True, (255, 255, 255))
                text_rect = over_text.get_rect(center=(400, 200))
                screen.blit(over_text, text_rect)

                pygame.draw.rect(screen, (0, 255, 0), (175, 300, 175, 60))
                pygame.draw.rect(screen, (255, 0, 0), (450, 300, 175, 60))

                restartFont = pygame.font.SysFont("Open Sans", 30, True)
                restartText = restartFont.render("Restart Game", True, (255, 255, 255))
                restartText_rect = restartText.get_rect(center=(263, 330))
                screen.blit(restartText, restartText_rect)

                stopFont = pygame.font.SysFont("Open Sans", 30, True)
                stopText = stopFont.render("End Game", True, (255, 255, 255))
                stopText_rect = stopText.get_rect(center=(538, 330))
                screen.blit(stopText, stopText_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        if (x < 350) and (x > 175) and (y < 360) and (y > 300):
                            global restart
                            restart = True
                            running = False
                            break
                        if (x < 625) and (x > 450) and (y < 360) and (y > 300):
                            restart = False
                            running = False
                            break


            enemyX[i] += enemyX_change[i]

            if enemyX[i] <= 0:
                enemyX_change[i] =4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = enemy_startY[random.randint(0, 2)]

            screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            bullet_state = "fire"
            screen.blit(bulletImg, (bulletX + 16, bulletY + 10))
            bulletY -= bulletY_change



        screen.blit(playerImg, (playerX, playerY))
        score = font.render("Score: " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (20, 550))
        pygame.display.update()

game_menu()