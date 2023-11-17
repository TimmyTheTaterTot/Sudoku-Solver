import pygame
from Space import Space

colors = {
    'white': (255, 255, 255),
    'off white': (220, 220, 220),
    'black': (0, 0, 0)
}

class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.grid = [[Space(j, i) for i in range(9)] for j in range(9)]
        self.window_width = 695
        self.window_height = 695
        self.rect_width = 70
        self.rect_height = 70

        self.font = pygame.font.SysFont('Comic Sans', 60)

        self.init_window()
        self.gameloop()


    def init_window(self):
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        window = self.window
        window.fill(colors['off white'])
        pygame.display.set_caption("Sudoku Solver")

        self.draw_board()


    def draw_board(self):
        for i in range(9):
            for j in range(9):
                self.create_rect(self.grid[j][i], self.window, self.font)
                

    @staticmethod
    def create_rect(space: Space, window: pygame.display, font:pygame.font.Font, width:int=70, height:int=70):
        x = (space.x * (width + 5)) + (int(space.x * 0.34) * 5) + 5
        y = (space.y * (height + 5)) + (int(space.y * 0.34) * 5) + 5
        font_w, font_h = font.size(str(space.val))
        space.rect = pygame.draw.rect(window, colors['white'], pygame.Rect(x, y, width, height), border_radius=5)
        if space.val != 0:
            window.blit(font.render(str(space.val), 1, colors['black']), (x + width/2 - font_w/2, y + height/2 - font_h/2))


    def gameloop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()


    def setval(self, x, y, val):
        self.grid[y][x].val = val


    def getval(self, x, y):
        return self.grid[y][x].val

if __name__ == "__main__":
    sudoku = Game()
    print(sudoku.grid)