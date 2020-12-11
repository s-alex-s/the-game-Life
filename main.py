import pygame
from copy import deepcopy


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_board = [[0] * width for _ in range(height)]
        self.next_board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 1
        self.cell_size = 20
        self.board_coords = []
        left2 = self.left
        top2 = self.top
        for i in range(self.height):
            self.board_coords.append([])
            for j in range(self.width):
                self.board_coords[i].append((left2, top2))
                left2 += self.cell_size
            top2 += self.cell_size
            left2 = self.left

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.board_coords = []
        left2 = self.left
        top2 = self.top
        for i in range(self.height):
            self.board_coords.append([])
            for j in range(self.width):
                self.board_coords[i].append((left2, top2))
                left2 += self.cell_size
            top2 += self.cell_size
            left2 = self.left

    def render(self, screen):
        left2 = self.left
        top2 = self.top
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255), (left2, top2, self.cell_size, self.cell_size), 1)
                if self.current_board[i][j]:
                    pygame.draw.rect(screen, (0, 255, 0), (left2 + 1, top2 + 1, self.cell_size - 2,
                                                           self.cell_size - 2), 0)
                if not pause:
                    self.next_board[i][j] = Life.next_move(self, self.current_board, i, j)
                left2 += self.cell_size
            top2 += self.cell_size
            left2 = self.left
        if not pause:
            self.current_board = deepcopy(self.next_board)

    def get_cell(self, mouse_pos):
        ii = 0
        jj = 0
        check = ()
        for i in self.board_coords:
            for j in i:
                if j[0] <= mouse_pos[0] <= j[0] + self.cell_size and j[1] <= mouse_pos[1] <= j[1] + self.cell_size:
                    check = (ii, jj)
                jj += 1
            ii += 1
            jj = 0
        if check:
            return check
        else:
            return None

    def on_click(self, cell_coords):
        if self.current_board[cell_coords[0]][cell_coords[1]] == 0:
            self.current_board[cell_coords[0]][cell_coords[1]] = 1
        else:
            self.current_board[cell_coords[0]][cell_coords[1]] = 0

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell and pause:
            self.on_click(cell)


class Life(Board):
    def __init__(self):
        super().__init__()

    def next_move(self, current_field, y, x):
        count = 0
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if current_field[i % self.height][j % self.width]:
                    count += 1
        if current_field[y][x]:
            count -= 1
            if count == 2 or count == 3:
                return 1
            return 0
        else:
            if count == 3:
                return 1
            return 0


if __name__ == '__main__':
    pygame.init()
    size = width, height = 940, 841
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Жизнь на Торе')
    clock = pygame.time.Clock()
    board = Board(47, 42)
    fps = 10
    fps_pause = 60
    pause = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
                elif event.button == 3:
                    if pause:
                        pause = False
                    else:
                        pause = True
                elif event.button == 4:
                    if fps <= 300:
                        fps += 1
                elif event.button == 5:
                    if fps > 1:
                        fps -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if pause:
                        pause = False
                    else:
                        pause = True
        screen.fill((0, 0, 0))
        board.render(screen)
        if pause:
            clock.tick(fps_pause)
        else:
            clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
