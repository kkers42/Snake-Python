import pygame, sys, random

WIDTH, HEIGHT = 600, 600
CELL = 20
FPS = 12

BG = (18,18,18)
HEAD = (46, 204, 113)
BODY = (39, 174, 96)
FOOD = (231, 76, 60)
GRID = (30, 30, 30)
TEXT = (240, 240, 240)

def rand_food():
    return (random.randrange(0, WIDTH//CELL) * CELL,
            random.randrange(0, HEIGHT//CELL) * CELL)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake (pygame)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    snake = [(WIDTH//2, HEIGHT//2)]
    direction = (0, 0)
    food = rand_food()
    score = 0
    alive = True

    def draw():
        screen.fill(BG)
        # grid
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, GRID, (x,0), (x,HEIGHT), 1)
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, GRID, (0,y), (WIDTH,y), 1)

        # food
        pygame.draw.rect(screen, FOOD, (*food, CELL, CELL))

        # snake
        for i,(x,y) in enumerate(snake):
            pygame.draw.rect(screen, HEAD if i==0 else BODY, (x,y,CELL,CELL))

        # score
        label = font.render(f"Score: {score}", True, TEXT)
        screen.blit(label, (8, HEIGHT-28))
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_LEFT and direction != (CELL,0):
                    direction = (-CELL, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL,0):
                    direction = (CELL, 0)
                elif event.key == pygame.K_UP and direction != (0,CELL):
                    direction = (0, -CELL)
                elif event.key == pygame.K_DOWN and direction != (0,-CELL):
                    direction = (0, CELL)
                elif event.key == pygame.K_r and not alive:
                    snake[:] = [(WIDTH//2, HEIGHT//2)]
                    direction = (0, 0)
                    alive = True

        if alive and direction != (0,0):
            hx, hy = snake[0]
            nx, ny = hx + direction[0], hy + direction[1]

            # collisions
            if nx < 0 or ny < 0 or nx >= WIDTH or ny >= HEIGHT or (nx, ny) in snake:
                alive = False
            else:
                snake.insert(0, (nx, ny))
                if (nx, ny) == food:
                    score += 1
                    food = rand_food()
                else:
                    snake.pop()

        draw()

        if not alive:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(overlay, (0,0))
            big = pygame.font.SysFont(None, 40).render("Game Over", True, (255,255,255))
            small = font.render("Press R to restart — ESC to quit", True, (255,255,255))
            screen.blit(big, big.get_rect(center=(WIDTH//2, HEIGHT//2 - 10)))
            screen.blit(small, small.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
            pygame.display.flip()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
