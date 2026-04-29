import pygame
import sys
import random

# ── Màu sắc ─────────────────────────────────────────
BLACK      = (0, 0, 0)
WHITE      = (255, 255, 255)
DARK_GRAY  = (80, 80, 80)
X_COLOR    = (220, 50, 50)
O_COLOR    = (30, 100, 200)

# ── Cấu hình ─────────────────────────────────────────
WIDTH   = 28
HEIGHT  = 28
MARGIN  = 2
ROWNUM  = 33
COLNUM  = 64
WIN_LEN = 5
FPS     = 60

WINDOW_W = (WIDTH + MARGIN) * COLNUM + MARGIN
WINDOW_H = (HEIGHT + MARGIN) * ROWNUM + MARGIN

# ── Grid ────────────────────────────────────────────
def make_grid(rows, cols):
    return [[0]*cols for _ in range(rows)]

# ── Draw X ──────────────────────────────────────────
def draw_x(surface, x, y):
    pad = WIDTH // 5
    pygame.draw.line(surface, X_COLOR, (x+pad, y+pad), (x+WIDTH-pad, y+HEIGHT-pad), 3)
    pygame.draw.line(surface, X_COLOR, (x+WIDTH-pad, y+pad), (x+pad, y+HEIGHT-pad), 3)

# ── Draw O ──────────────────────────────────────────
def draw_o(surface, x, y):
    pygame.draw.circle(surface, O_COLOR, (x+WIDTH//2, y+HEIGHT//2), WIDTH//2-5, 3)

# ── Check win ───────────────────────────────────────
def check_win(board):
    for piece in ['x','o']:
        for r in range(ROWNUM):
            for c in range(COLNUM):
                if board[r][c] != piece:
                    continue
                for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
                    try:
                        if all(board[r+i*dr][c+i*dc]==piece for i in range(WIN_LEN)):
                            return piece
                    except:
                        pass
    return None

# ── AI ENGINE ───────────────────────────────────────

def get_neighbors(grid, dist=2):
    moves = set()
    for r in range(ROWNUM):
        for c in range(COLNUM):
            if grid[r][c] != 0:
                for dr in range(-dist, dist+1):
                    for dc in range(-dist, dist+1):
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < ROWNUM and 0 <= nc < COLNUM:
                            if grid[nr][nc] == 0:
                                moves.add((nr,nc))
    return list(moves) if moves else [(ROWNUM//2, COLNUM//2)]

def evaluate_direction(grid, r, c, dr, dc, player):
    count = 0
    for i in range(1,5):
        nr, nc = r+dr*i, c+dc*i
        if 0 <= nr < ROWNUM and 0 <= nc < COLNUM:
            if grid[nr][nc] == player:
                count += 1
            elif grid[nr][nc] != 0:
                break
        else:
            break

    if count == 4: return 10000
    if count == 3: return 1000
    if count == 2: return 100
    if count == 1: return 10
    return 1

def evaluate_cell(grid, r, c):
    score = 0
    directions = [(1,0),(0,1),(1,1),(1,-1)]

    for dr,dc in directions:
        score += evaluate_direction(grid,r,c,dr,dc,'o')

    for dr,dc in directions:
        score += evaluate_direction(grid,r,c,dr,dc,'x') * 1.2

    return score

def ai_move(grid):
    moves = get_neighbors(grid)

    best_score = -1
    best_move = None

    for r,c in moves:
        score = evaluate_cell(grid,r,c)
        if score > best_score:
            best_score = score
            best_move = (r,c)

    return best_move

# ── Draw board ──────────────────────────────────────
def draw_board(screen, grid):
    screen.fill(DARK_GRAY)
    for r in range(ROWNUM):
        for c in range(COLNUM):
            x = (WIDTH+MARGIN)*c + MARGIN
            y = (HEIGHT+MARGIN)*r + MARGIN

            pygame.draw.rect(screen, WHITE, (x,y,WIDTH,HEIGHT))

            if grid[r][c]=='x':
                draw_x(screen,x,y)
            elif grid[r][c]=='o':
                draw_o(screen,x,y)

# ── MAIN ────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Caro AI")
    clock = pygame.time.Clock()

    grid = make_grid(ROWNUM, COLNUM)
    xo = 'x'
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and xo == 'x':
                mx, my = pygame.mouse.get_pos()
                c = mx // (WIDTH+MARGIN)
                r = my // (HEIGHT+MARGIN)

                if grid[r][c] == 0:
                    grid[r][c] = 'x'
                    xo = 'o'

        # AI TURN
        if xo == 'o':
            move = ai_move(grid)
            if move:
                r,c = move
                grid[r][c] = 'o'
                xo = 'x'

        winner = check_win(grid)
        if winner:
            print("Winner:", winner)
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

        draw_board(screen, grid)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()