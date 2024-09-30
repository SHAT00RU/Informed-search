import pygame
import sys
import random
import heapq

# Inisialisasi pygame
pygame.init()

# Konfigurasi layar
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man A*")

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)

# Maze grid (1 adalah dinding, 0 adalah jalan)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

ROWS = len(maze)
COLS = len(maze[0])

# Posisi Pac-Man dan tujuan
start = (4, 0)  # Pojok kiri tengah
goal = (4, 17)  # Pojok kanan tengah
pacman_pos = start

# Ghosts (gerak acak)
ghosts = [(1, 16), (8, 1)]

# Poin (Pellets)
pellets = [(r, c) for r in range(ROWS) for c in range(COLS) if maze[r][c] == 0 and (r, c) != start]
pellets_eaten = 0  # Variabel untuk menghitung pellet yang dimakan

# Load gambar Pac-Man dan Ghost
pacman_image = pygame.image.load(r'C:\Users\lenov\OneDrive\Documents\Kuliah\SMT 3\KKA\pacman.png')
ghost_image = pygame.image.load(r'C:\Users\lenov\OneDrive\Documents\Kuliah\SMT 3\KKA\ghost.png')
pacman_image = pygame.transform.scale(pacman_image, (CELL_SIZE, CELL_SIZE))
ghost_image = pygame.transform.scale(ghost_image, (CELL_SIZE, CELL_SIZE))

# Fungsi untuk menggambar grid
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = BLUE if maze[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Menggambar pellets
    for pellet in pellets:
        pygame.draw.circle(screen, WHITE, (pellet[1] * CELL_SIZE + CELL_SIZE // 2, pellet[0] * CELL_SIZE + CELL_SIZE // 2), 5)

# Fungsi Heuristic untuk A* (menghitung jarak Manhattan)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Fungsi untuk mencari jalur dengan A*
def astar(start, goal):
    queue = []
    heapq.heappush(queue, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while queue:
        _, current = heapq.heappop(queue)

        if current == goal:
            break

        neighbors = [(current[0] + 1, current[1]), (current[0] - 1, current[1]), 
                     (current[0], current[1] + 1), (current[0], current[1] - 1)]

        for next in neighbors:
            if 0 <= next[0] < ROWS and 0 <= next[1] < COLS and maze[next[0]][next[1]] == 0:
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    heapq.heappush(queue, (priority, next))
                    came_from[next] = current

    # Rekonstruksi jalur dari goal ke start
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# Fungsi untuk menggambar Pac-Man di layar
def draw_pacman(pos):
    screen.blit(pacman_image, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE))

# Fungsi untuk menggambar Ghost di layar
def draw_ghost(pos):
    screen.blit(ghost_image, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE))

# Fungsi untuk menggerakkan Ghost secara acak
def move_ghost(pos):
    neighbors = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), 
                 (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
    random.shuffle(neighbors)
    for next in neighbors:
        if 0 <= next[0] < ROWS and 0 <= next[1] < COLS and maze[next[0]][next[1]] == 0:
            return next
    return pos

# Fungsi utama
def main():
    global pacman_pos, pellets_eaten
    clock = pygame.time.Clock()
    path = astar(start, goal)
    path_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_grid()

        # Gerakan Pac-Man berdasarkan jalur A*
        if path_index < len(path):
            pacman_pos = path[path_index]
            # Jika pacman melewati pellet, hapus dari daftar dan ubah warna jadi abu-abu
            if pacman_pos in pellets:
                pellets.remove(pacman_pos)
                pellets_eaten += 1  # Tambahkan ke skor
                pygame.draw.circle(screen, GRAY, (pacman_pos[1] * CELL_SIZE + CELL_SIZE // 2, pacman_pos[0] * CELL_SIZE + CELL_SIZE // 2), 5)
            path_index += 1

        # Menggerakkan Ghost
        for i in range(len(ghosts)):
            ghosts[i] = move_ghost(ghosts[i])

        # Gambar Pac-Man, Ghost, dan Poin
        draw_pacman(pacman_pos)
        for ghost in ghosts:
            draw_ghost(ghost)

        # Tampilkan skor di pojok kanan bawah
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Pellets eaten: {pellets_eaten}', True, WHITE)
        screen.blit(score_text, (WIDTH - 250, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(5)

# Jalankan permainan
if _name_ == "_main_":
    main()
