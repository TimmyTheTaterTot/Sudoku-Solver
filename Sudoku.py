import pygame
import time
import random as rand
import threading
from Space import Space

colors = {
    'white': (255, 255, 255),
    'off white': (220, 220, 220),
    'black': (0, 0, 0),
    'baby blue': (37, 150, 190),
    'light blue': (116, 185, 255),
    'red': (255, 55, 41)
}

class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.active = True
        self.running = True
        self.help_menu_active = False

        self.grid = [[Space(j, i) for i in range(9)] for j in range(9)]
        self.window_width = 690
        self.window_height = 690
        self.rect_width = 70
        self.rect_height = 70

        self.selected_space = None

        self.font = pygame.font.SysFont('Comic Sans', 60)
        self.helpfont = pygame.font.SysFont('Comic Sans', 20)
        self.clock = pygame.time.Clock()

        self.init_window()
        self.gameloop()


    def init_window(self):
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.window.fill(colors['off white'])
        pygame.display.set_caption("Sudoku Solver! Press h for help")

        self.init_board_squares()
        self.update_board()


    def init_board_squares(self):
        for i in range(9):
            for j in range(9):
                Game.init_rect(self.grid[j][i], self.rect_width, self.rect_height)


    def update_board(self):
        for i in range(9):
            for j in range(9):
                Game.update_rect(self.grid[j][i], self.window, self.font)
                

    @staticmethod
    def init_rect(space:Space, width:int, height:int):
        x = (space.x * (width + 5)) + ((space.x // 3) * 5) + 5
        y = (space.y * (height + 5)) + ((space.y // 3) * 5) + 5
        space.width = width
        space.height = height
        space.rectx = x
        space.recty = y
        space.rect = pygame.Rect(x, y, width, height)

    @staticmethod
    def update_rect(space:Space, window:pygame.display, font:pygame.font):
        pygame.draw.rect(window, space.color, space.rect, border_radius=5)
        font_w, font_h = font.size(str(space.val))
        if space.val != 0:
            window.blit(font.render(str(space.val), 1, colors['black']), (space.rectx + space.width/2 - font_w/2, space.recty + space.height/2 - font_h/2))

    
    def generate_puzzle(self):
        for space in range(81):
            self.grid[space//9][space%9].val = 0

        base  = 3
        side  = base*base

        # pattern for a baseline valid solution
        def pattern(r,c):
            return (base*(r%base)+r//base+c)%side

        # randomize rows, columns and numbers (of valid base pattern)
        def shuffle(s):
            return rand.sample(s,len(s)) 
        
        rBase = range(base) 
        rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
        cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
        nums  = shuffle(range(1,base*base+1))

        # produce board using randomized baseline pattern
        board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

        # place a certain ratio of the numbers onto the board to create the puzzle
        for space in rand.sample(range(81), 81 * 1//4):
            self.grid[space//9][space%9].val = board[space//9][space%9]

    
    def solve_puzzle(self):
        x = 0
        y = 0
        solved_squares = []
        self.active = False
        while y != 9 and self.running:
            time.sleep(0)
            space = self.grid[x][y]
            if space.val == 0: # if it is a blank square, solve it
                for i in range(1, 10):
                    if i not in space.failed_values and self.check_move(space, i):
                        space.val = i
                        solved_squares.append(space)
                        break
                if space.val == 0: # if it is still a blank square, we need to backtrack
                    space.failed_values = []
                    prev_space = solved_squares[-1]
                    try:
                        x = prev_space.x
                        y = prev_space.y
                        prev_space.failed_values.append(prev_space.val)
                        prev_space.val = 0
                    except IndexError:
                        raise ValueError("Unsolvable sudoku board")
                    solved_squares = solved_squares[0:-1]
                    continue

            if x < 8:
                x += 1
            else:
                y += 1
                x = 0

        self.active = True

    
    def check_move(self, space:Space, value:int):
        selx = space.x
        sely = space.y
        error_spaces = []

        # check row
        for x in range(9):
            if x != selx:
                if self.grid[x][sely].val == value:
                    error_spaces.append(self.grid[x][sely])

        # check column
        for y in range(9):
            if y != sely:
                if self.grid[selx][y].val == value:
                    error_spaces.append(self.grid[selx][y])

        #check 3x3 block
        blockx = 3 * (selx // 3)
        blocky = 3 * (sely // 3)
        for x in range(blockx, blockx+3):
            for y in range(blocky, blocky+3):
                if self.grid[x][y].val == value:
                    error_spaces.append(self.grid[x][y])

        if len(error_spaces) == 0:
            return True 
        elif self.active:
            threading.Thread(target=Game.flash_spaces, args = [error_spaces]).start()
    

    @staticmethod
    def flash_spaces(spaces:list | tuple):
        for i in range(len(spaces)):
            spaces[i].color = colors['red']
        time.sleep(0.5)
        for i in range(len(spaces)):
            spaces[i].color = colors['white']


    def help_menu(self):
        # text_y = 0
        # help_rect = pygame.draw.rect(self.window, colors['red'], pygame.Rect(0, 0, 400, 400), border_radius=3)
        # helptext = ["Welcome to Sudoku Solver!",
        #             "Here you can play or watch the computer solve a Sudoku puzzle",
        #             "To fill in a square, click on it (it will turn blue), then type the number (1-9) that you want to input",
        #             "To generate a new Sudoku puzzle, press 'g'",
        #             "To solve the current Sudoku puzzle, press 's'",
        #             "To reopen this help page, press 'h'"]
        
        # def rhf(text):
        #     text_surface = (self.helpfont.render(text, 1, colors['black']), (0, text_y))
        #     text_y += self.helpfont.size(text)[1]
        #     return text_surface

        # self.window.blits([rhf(line, text_y) for line in helptext])

    
    def input_handler(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # mouse button 1 (left click)
                if self.help_menu_active:
                    self.help_menu_active = False
                    self.window.fill(colors['off white'])
                
                if self.selected_space is not None:
                    self.selected_space.color = colors['white']

                posx, posy = event.pos
                x = int((posx - (posx // 225)*5 - 3) / (self.rect_width + 5))
                y = int((posy - (posy // 225)*5 - 3) / (self.rect_height + 5))
                self.selected_space = self.grid[x][y]
                self.selected_space.color = colors['light blue']
        
        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key-48 in [1,2,3,4,5,6,7,8,9]:
                if self.selected_space is not None:
                    if self.check_move(self.selected_space, event.key-48):
                        self.selected_space.val = event.key-48
            elif event.key == 103: # g key
                threading.Thread(target=self.generate_puzzle).start()
            elif event.key == 115: # s key
                threading.Thread(target=self.solve_puzzle).start()
            elif event.key == 104: # h key
                self.help_menu_active = True
            

    def gameloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.input_handler(event)

            self.update_board()

            if self.help_menu_active: 
                self.help_menu()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    sudoku = Game()