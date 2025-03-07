import pygame

pygame.init()

width, height = 700, 700
screen = pygame.display.set_mode((width, height))

WHITE = (255, 255, 255)

snake_posx = width // 2 - 25
snake_posy = height // 2 - 25

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill((30, 30, 30))  
    pygame.draw.rect(screen, WHITE, (snake_posx, snake_posy, 50, 50) )

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        snake_posy -= 5
    if keys[pygame.K_s]:
        snake_posy += 5
    if keys[pygame.K_a]:
        snake_posx -= 5
    if keys[pygame.K_d]:
        snake_posx += 5
    
    pygame.display.flip()

    


pygame.quit()