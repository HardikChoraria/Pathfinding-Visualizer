import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* pathfinding algorithm")

# Define colors
RED = (255, 0, 0)
GREEN = (254, 250, 224)
BLUE = (188, 108, 37)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (51, 51, 49)
PURPLE = (83, 166, 124)
ORANGE = (44, 115, 109)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
LAV = (230, 230, 250)
OLIVEGREEN = (87, 187, 188)




class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == BLUE

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        start_color = WHITE  # Initial color
        end_color = BLUE  # Closed color
        duration = 5  # Number of frames for the gradient effect

    # Calculate the color components difference
        r_diff = (end_color[0] - start_color[0]) / duration
        g_diff = (end_color[1] - start_color[1]) / duration
        b_diff = (end_color[2] - start_color[2]) / duration

    # Gradually change the color
        for i in range(duration):
        # Calculate the new color based on the current frame
            r = start_color[0] + int(r_diff * i)
            g = start_color[1] + int(g_diff * i)
            b = start_color[2] + int(b_diff * i)

        # Update the color of the spot
            self.color = (r, g, b)

        # Delay a bit to visualize the gradient effect
            pygame.time.delay(10)

        # BLUEraw the spot
            pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.width))
            pygame.display.update()


    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = OLIVEGREEN

    def make_start(self):
        self.color = ORANGE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


class PathfindingAlgorithm:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("A* pathfinding algorithm")

    def run(self):
        grid = self.make_grid(20, WIDTH)
        start = None
        end = None
        run = True

        while run:
            self.draw(grid)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos, 20, WIDTH)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    elif spot != end and spot != start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos, 20, WIDTH)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    if spot == end:
                        end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        self.algorithm(grid, start, end)

                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = self.make_grid(20, WIDTH)

        pygame.quit()

    def make_grid(self, rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                grid[i].append(spot)
        return grid

    def draw_grid(self, rows, width):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(self.win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(self.win, GREY, (j * gap, 0), (j * gap, width))

    def draw(self, grid):
        self.win.fill(WHITE)
        for row in grid:
            for spot in row:
                spot.draw(self.win)
        self.draw_grid(len(grid), WIDTH)
        pygame.display.update()


    def get_clicked_pos(self, pos, rows, width):
        gap = width // rows
        y, x = pos
        row = y // gap
        col = x // gap
        return row, col

    def reconstruct_path(self, came_from, current,grid):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            self.draw(grid)

    def algorithm(self, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[start] = self.h(start.get_pos(), end.get_pos())
        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                self.reconstruct_path(came_from, end,grid)
                end.make_end()
                start.make_start()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            self.draw(grid)

            if current != start:
                current.make_closed()

        return False

    @staticmethod
    def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)


pathfinding_algorithm = PathfindingAlgorithm()
pathfinding_algorithm.run()
