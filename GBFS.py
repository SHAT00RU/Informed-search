import pygame
import sys
import random
import heapq
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Collecting Pellets")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

ROWS = len(maze)
COLS = len(maze[0])

start = (7, 0)
goal = (7, 19) 
pacman_pos = start

pellets = [(r, c) for r in range(ROWS) for c in range(COLS) if maze[r][c] == 0 and (r, c) != start]
pellets_eaten = 0

pacman_image = pygame.image.load(r'C:\Users\lenov\OneDrive\Documents\Kuliah\SMT 3\KKA\pacman.png')
pacman_image = pygame.transform.scale(pacman_image, (CELL_SIZE, CELL_SIZE))

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = BLUE if maze[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for pellet in pellets:
        pygame.draw.circle(screen, WHITE, (pellet[1] * CELL_SIZE + CELL_SIZE // 2, pellet[0] * CELL_SIZE + CELL_SIZE // 2), 5)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def greedy_best_first_search(start, goals):
    queue = []
    heapq.heappush(queue, (0, start))
    came_from = {}
    came_from[start] = None

    while queue:
        _, current = heapq.heappop(queue)

        if current in goals:
            goals.remove(current)
            if not goals:
                break

        neighbors = [(current[0] + 1, current[1]), (current[0] - 1, current[1]), 
                     (current[0], current[1] + 1), (current[0], current[1] - 1)]

        for next in neighbors:
            if 0 <= next[0] < ROWS and 0 <= next[1] < COLS and maze[next[0]][next[1]] == 0 and next not in came_from:
                priority = heuristic(goal, next)
                heapq.heappush(queue, (priority, next))
                came_from[next] = current

    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path

def draw_pacman(pos):
    screen.blit(pacman_image, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE))

def draw_turn_count(turn_count):
    font = pygame.font.SysFont(None, 36)
    turn_text = font.render(f'Turns: {turn_count}', True, WHITE)
    screen.blit(turn_text, (10, 10))

def draw_time(elapsed_time):
    font = pygame.font.SysFont(None, 36)
    time_text = font.render(f'Time: {int(elapsed_time)} s', True, WHITE)
    screen.blit(time_text, (WIDTH - 150, 10))

def main():
    global pacman_pos, pellets_eaten
    clock = pygame.time.Clock()
    
    start_time = time.time()
    direction = None 
    turn_count = 0
    total_score = 0

    while pellets: 
        path = greedy_best_first_search(pacman_pos, pellets[:]) 
        path_index = 0

        while path_index < len(path):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)
            draw_grid()

            pacman_pos = path[path_index]
            
            if path_index > 0:
                previous_pos = path[path_index - 1]
                current_direction = (pacman_pos[0] - previous_pos[0], pacman_pos[1] - previous_pos[1])

                if direction is not None:
                    if current_direction != direction:
                        turn_count += 1

                direction = current_direction

            if pacman_pos in pellets:
                pellets.remove(pacman_pos)
                pellets_eaten += 1
                total_score += len(path) - path_index  # Skor bertambah sesuai dengan langkah yang tersisa
                pygame.draw.circle(screen, GRAY, (pacman_pos[1] * CELL_SIZE + CELL_SIZE // 2, pacman_pos[0] * CELL_SIZE + CELL_SIZE // 2), 5)

            path_index += 1

            draw_pacman(pacman_pos)
            draw_turn_count(turn_count)

            elapsed_time = time.time() - start_time
            draw_time(elapsed_time)

            pygame.display.flip()
            clock.tick(5)

    pacman_pos = goal
    elapsed_time = time.time() - start_time
    font = pygame.font.SysFont(None, 72)
    score_text = font.render(f'Score: {total_score}', True, WHITE)
    time_text = font.render(f'Time: {int(elapsed_time)} seconds', True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 + score_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
