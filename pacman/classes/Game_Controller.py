import sys
import os
from enum import Enum, auto
import random
import pygame
import time

def get_base_path():
    if getattr(sys, 'frozen', False): # executable
        return sys._MEIPASS
    else:
        return os.path.dirname(__file__)
base_path = get_base_path()

sys.path.append(os.path.join(base_path,'Game'))
sys.path.append(os.path.join(base_path,'Progress'))
sys.path.append(os.path.join(base_path,'User_Interface'))
sys.path.append(os.path.join(base_path,'Error'))
sys.path.append(os.path.join(base_path,'Database'))


import Entity
import Level_Manager
import Object
import Error
import Progress

# smart screen allignment issue

class Game_State(Enum):
    START = auto()
    MENU= auto()
    NEW_USER= auto()
    DELETE_USER= auto()
    GAME_START= auto()
    GAME = auto()
    GAME_OVER = auto()
    WIN = auto()
    LOSE = auto()
    STOP= auto()
    GAME_END = auto()
    
class Utility:
    @staticmethod
    def load_image(file_name):
        return pygame.image.load(os.path.join(base_path,'..','resources','sprite', file_name)).convert_alpha()

    @staticmethod
    def scale_logo(image, new_width):
            width, height = image.get_size()
            aspect_ratio = height / width
            new_height = int(new_width * aspect_ratio)
            return pygame.transform.scale(image, (new_width, new_height))
    
class Start_Menu(Utility):
    def __init__(self, screen, TILES_X=27, TILES_Y=27):
        self.screen = screen
        self.state = Game_State.START
        
        self.font_path = os.path.join(base_path,'..','resources','font','Minecraft.ttf')

        self.logo_image = self.scale_logo(Utility.load_image('logo.gif'), 400)
        self.font = pygame.font.Font(self.font_path, 28)
        self.font1 = pygame.font.Font(self.font_path, 26)
        self.font2 = pygame.font.Font(self.font_path, 22)
        self.font3 = pygame.font.Font(self.font_path, 19)
        self.font3 = pygame.font.Font(self.font_path, 14)
        
        self.username=""
        self.user_selection=0
        self.user_options = None
        
        #background
        self.ghost_background = []
        self.grid_background=[[" " for x in range(TILES_X)] for y in range(TILES_Y)]
        self.graph_background = Level_Manager.Graph().connect_maze(self.grid_background)
            
        for i in range(random.randint(10,25)):
            self.ghost_background.append(Entity.Dumb_Ghost(self.screen))
            self.ghost_background[i].set_maze(self.grid_background, self.graph_background)
            self.ghost_background[i].set_graph(Level_Manager.Graph())
            self.ghost_background[i].set_pos()
    
    def background(self):
        current_time=time.time()
        for setan in self.ghost_background:
            setan.control(current_time)
        
    def start_menu(self, score_list):        
        self.screen.fill((0, 0, 0))
        self.background()
        
        logo_rect = self.logo_image.get_rect(center=(self.screen.get_width() // 2, 180))
        text = '< Press any key to Play >'
        outline_color = (255, 0, 0)
        text_color = (255, 255, 255)
        
        # Create the outline by rendering the text multiple times with slight offsets
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in offsets:
            outline_surface = self.font2.render(text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(self.screen.get_width() // 2 + dx, 280 + dy))
            self.screen.blit(outline_surface, outline_rect)
        
        # Render the main text
        text_surface = self.font2.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 280))
        self.screen.blit(text_surface, text_rect)
        
        header_text = 'Scoreboard'
        outline_color = (0, 0, 255) 
        text_color = (255, 255, 255) 

        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in offsets:
            outline_surface = self.font1.render(header_text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(self.screen.get_width() // 2 + dx, 335 + dy))
            self.screen.blit(outline_surface, outline_rect)

        header_surface = self.font1.render(header_text, True, text_color)
        header_rect = header_surface.get_rect(center=(self.screen.get_width() // 2, 335))
        self.screen.blit(header_surface, header_rect)
        
        # Render the scores
        start_y = 365
        for i, (data) in enumerate(score_list):
            score_text = f'{data[0]}    Level {data[1]}    Score {data[2]}'
            score_surface = self.font3.render(score_text, True, text_color)
            score_rect = score_surface.get_rect(center=(self.screen.get_width() // 2, start_y + i * 20))
            self.screen.blit(score_surface, score_rect)
        
        self.screen.blit(self.logo_image, logo_rect)
        pygame.display.flip()
    
    def user_menu(self, user_list=None):	
        self.user_options = [str(i) for i in user_list.keys()]
        if len(self.user_options) < 5:
            self.user_options.append('Create New User')
        # print(self.user_options)
        self.screen.fill((0, 0, 0))
        self.background()
        
        title_text = 'Choose Save Data:'
        title_outline_color = (255, 0, 0)
        title_color = (255, 255, 255)
        title_surface = self.font.render(title_text, True, title_outline_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 210))
        
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in offsets:
            outline_surface = self.font.render(title_text, True, title_outline_color)
            outline_rect = outline_surface.get_rect(center=(self.screen.get_width() // 2 + dx, 210 + dy))
            self.screen.blit(outline_surface, outline_rect)
        title_surface = self.font.render(title_text, True, title_color)
        self.screen.blit(title_surface, title_rect)
        
        start_y = 250
        for i, user in enumerate(self.user_options):
            if i == self.user_selection:
                outline_color = (0, 0, 255)  # Blue outline for selected user
                text_color = (255, 0, 0)  # Red text for selected user
            else:
                outline_color = (255, 255, 0)  # White outline for non-selected users
                text_color = (255, 255, 255)  # Yellow text for non-selected users
            
            user_text = f"{str(user)} level {user_list[user]['level']}  {user_list[user]['difficulty']}" if user in user_list else user
            for dx, dy in offsets:
                outline_surface = self.font2.render(user_text, True, outline_color)
                outline_rect = outline_surface.get_rect(center=(self.screen.get_width() // 2 + dx, start_y + i * 30 + dy))
                self.screen.blit(outline_surface, outline_rect)
            user_surface = self.font2.render(user_text, True, text_color)
            user_rect = user_surface.get_rect(center=(self.screen.get_width() // 2, start_y + i * 30))
            self.screen.blit(user_surface, user_rect)
        
        pygame.display.flip()
    
    def handle_user_registration(self):
        self.screen.fill((0, 0, 0))
        self.background()
        
        title_text = 'Username:'
        title_outline_color = (255, 0, 0)
        title_color = (255, 255, 255)
        title_surface = self.font.render(title_text, True, title_outline_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 210))
        
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in offsets:
            outline_surface = self.font.render(title_text, True, title_outline_color)
            outline_rect = outline_surface.get_rect(center=(self.screen.get_width() // 2 + dx, 210 + dy))
            self.screen.blit(outline_surface, outline_rect)
        title_surface = self.font.render(title_text, True, title_color)
        self.screen.blit(title_surface, title_rect)
        
        input_box = pygame.Rect(self.screen.get_width() // 2 - 100, 250, 200, 40)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = True
        text = ''
        done = False
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                        color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = Game_State.MENU
                        done = True
                    if active:
                        if event.key == pygame.K_RETURN:
                            self.username = text
                            self.state = Game_State.MENU
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            
            self.screen.fill((0, 0, 0))
            self.background()
            self.screen.blit(title_surface, title_rect)
            
            txt_surface = self.font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)
            
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
    
    def get_user(self):
        return self.username
        
    def handle_event(self, event):
        
        if event.type == pygame.KEYDOWN:
            if self.state == Game_State.START:
                self.state = Game_State.MENU
                time.sleep(0.1)
                
            elif self.state == Game_State.MENU:
                time.sleep(0.05)
                if event.key == pygame.K_UP:
                    self.user_selection = (self.user_selection - 1) % len(self.user_options)
                elif event.key == pygame.K_DOWN:
                    self.user_selection = (self.user_selection + 1) % len(self.user_options)
                elif event.key == pygame.K_ESCAPE:
                    self.state = Game_State.START
                    time.sleep(0.25)
                elif event.key == pygame.K_RETURN:
                    self.selection = self.user_options[self.user_selection]
                    if self.selection == 'Create New User':
                        self.state = Game_State.NEW_USER
                    else:
                        self.state = Game_State.GAME_START
                        self.username = self.selection
                        print(self.username)
                elif event.key == pygame.K_DELETE:
                    if self.user_options[self.user_selection] != 'Create New User':
                        self.username = self.user_options[self.user_selection]
                        self.state = Game_State.DELETE_USER
                        time.sleep(0.1)
            elif self.state == Game_State.NEW_USER:
                self.state = Game_State.NEW_USER

class Game:
    def __init__(self, screen, user=None, tile_size=20):
        self.screen = screen
        self.state = Game_State.START
        self.user=user
        self.score=0
        self.life=3
        self.level = 0
        
        self.running = True
        
        self.tile_size = tile_size
        self.maze_layout = None
        self.maze_graph = None
        self.maze_path = None
        self.maze_width = None
        self.maze_height = None
        self.difficulty = None
        
        self.Player=None
        self.Ghost=[]
        self.Food_Pellets=[]
        self.Fruit=[]
        
        self.game_score=[Game_State.STOP, self.user, self.score, self.level]
        
        self.font_path = os.path.join(base_path,'..','resources','font','Minecraft.ttf')
        self.font = pygame.font.Font(self.font_path, 22)
        
        self.start_image = Utility.load_image('start.gif')
        self.ready_image = Utility.load_image('ready.gif')
        self.game_over_image = Utility.load_image('gameover.gif')
        self.life_image = Utility.load_image('life.gif')
        
        self.wall_nub = Utility.load_image('wall-nub.gif')
        self.wall_corner_ll = Utility.load_image('wall-corner-ll.gif')
        self.wall_corner_lr = Utility.load_image('wall-corner-lr.gif')
        self.wall_corner_ul = Utility.load_image('wall-corner-ul.gif')
        self.wall_corner_ur = Utility.load_image('wall-corner-ur.gif')
        self.wall_end_b = Utility.load_image('wall-end-b.gif')
        self.wall_end_l = Utility.load_image('wall-end-l.gif')
        self.wall_end_r = Utility.load_image('wall-end-r.gif')
        self.wall_end_t = Utility.load_image('wall-end-t.gif')
        self.wall_straight_horiz = Utility.load_image('wall-straight-horiz.gif')
        self.wall_straight_vert = Utility.load_image('wall-straight-vert.gif')
        self.wall_t_left = Utility.load_image('wall-t-left.gif')
        self.wall_t_right = Utility.load_image('wall-t-right.gif')
        self.wall_t_up = Utility.load_image('wall-t-top.gif')
        self.wall_t_bottom = Utility.load_image('wall-t-bottom.gif')
        self.wall_x = Utility.load_image('wall-x.gif')
        
    def set_user(self, user):
        self.user = user
        
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        
    def initialize_game(self, level_data=None, Player=None):
        self.maze_width=level_data['size'][0]*self.tile_size
        self.maze_height=level_data['size'][1]*self.tile_size
        self.maze_layout=level_data['maze']
        self.maze_graph=level_data['graph']
        self.maze_path=level_data['path']
        difficulty=Level_Manager.Difficulty(level_data['difficulty'])
        
        self.level=level_data['level']
        self.difficulty=Level_Manager.Difficulty(level_data['difficulty']).name
        
        
        #...................................................
        self.Player = Player
        self.Player.set_maze(self.maze_layout, self.maze_graph)
        self.Player.set_pos()
        if difficulty == Level_Manager.Difficulty.EASY:
            for i in range(4):
                self.Ghost.append(Entity.Dumb_Ghost(self.screen))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level_Manager.Graph())
                self.Ghost[i].set_pos()
        elif difficulty == Level_Manager.Difficulty.MEDIUM:
            for i in range(5):
                self.Ghost.append(random.choice([Entity.Dumb_Ghost(self.screen),Entity.Hunter1_Ghost(self.screen),Entity.Hunter2_Ghost(self.screen), Entity.Wanderer_Ghost(self.screen)]))
                # self.Ghost.append(Entity.Dumb_Ghost(self.screen))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level_Manager.Graph())
                self.Ghost[i].set_pos()
        elif difficulty == Level_Manager.Difficulty.HARD:
            for i in range(6):
                self.Ghost.append(random.choice([Entity.Dumb_Ghost(self.screen),Entity.Hunter1_Ghost(self.screen),Entity.Hunter2_Ghost(self.screen), Entity.Wanderer_Ghost(self.screen)]))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level_Manager.Graph())
                self.Ghost[i].set_pos()
        elif difficulty == Level_Manager.Difficulty.SUPER_HARD:
            for i in range(8):
                self.Ghost.append(random.choice([Entity.Dumb_Ghost(self.screen), Entity.Wanderer_Ghost(self.screen)]))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level_Manager.Graph())
                self.Ghost[i].set_pos()
        
        for vertex in self.maze_path:
            x,y=vertex.split(',')
            self.Food_Pellets.append(Object.Pellet_Food(self.screen, int(y), int(x)))
        
    def draw_hud(self):
        # Draw life images in the bottom left corner
        life_x = 10
        life_y = self.screen.get_height() - self.life_image.get_height() - 10
        for i in range(self.life):
            self.screen.blit(self.life_image, (life_x, life_y))
            life_x += self.life_image.get_width() + 5  # Add some spacing between life images

        # Draw score next to the life images with a red outline
        score_text = f'Score: {self.score}'
        score_surface = self.font.render(score_text, True, (255, 255, 255))
        score_outline_surface = self.font.render(score_text, True, (255, 0, 0))
        score_rect = score_surface.get_rect(bottomleft=(life_x + 5, self.screen.get_height() -5))
        score_outline_rect = score_outline_surface.get_rect(bottomleft=(life_x + 5, self.screen.get_height() - 5))

        # Draw the outline by rendering the text multiple times with slight offsets
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in offsets:
            self.screen.blit(score_outline_surface, score_outline_rect.move(dx, dy))
        self.screen.blit(score_surface, score_rect)
        
    def draw_maze(self):
        for y, row in enumerate(self.maze_layout):
            for x, tile in enumerate(row):
                if tile == '#':
                    self.screen.blit(self.wall_nub, (x * self.tile_size, y * self.tile_size))

                
    def game_begin(self):
        self.screen.fill((0, 0, 0))
        for setan in self.Ghost:
            if isinstance(setan,Entity.Dumb_Ghost):
                setan.control(0)
            else:
                setan.control(0, self.Player)
                
        for food in self.Food_Pellets:
            food.draw()
                
        self.draw_maze()
        self.draw_hud()        
        self.Player.draw(0,0)
        
        ready_rect = self.ready_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(self.ready_image, ready_rect)
        self.state = Game_State.GAME
        pygame.display.flip()
        time.sleep(2)
    
    def game_restart(self):
        self.Player.set_pos()
        for setan in self.Ghost:
            setan.set_pos()
        self.game_begin()
            
    def game_over(self):
        # self.Player=None
        self.Ghost.clear()
        self.Food_Pellets.clear()
        self.score=0
        self.life=3
        # self.maze_layout = None
        # self.maze_graph = None
        # self.maze_path = None
        # self.maze_width = None
        # self.maze_height = None   
        
        self.screen.blit(self.game_over_image, (self.screen.get_width() // 2 - self.game_over_image.get_width() // 2, self.screen.get_height() // 2 - self.game_over_image.get_height() // 2))
        pygame.display.flip()
        # time.sleep(2)
    def game_ended(self, state):
        self.game_score=[state ,self.user, self.score, self.level]
        
    def game_result(self):
        return self.game_score

    def update_offsets(self):
        # Calculate the offsets to center the maze
        maze_width = len(self.maze_layout[0]) * self.tile_size
        maze_height = len(self.maze_layout) * self.tile_size

        # Calculate the offsets to center the maze on the screen
        self.offset_x = 0#(SCREEN_WIDTH - maze_width) // 2
        self.offset_y = 0#(SCREEN_HEIGHT - maze_height) // 2

    
    def update_screen(self, keys=None):
        BLACK = (0, 0, 0)
        keys=pygame.key.get_pressed()
        current_time=time.time()
        random.seed(current_time)
        if self.state ==Game_State.GAME_START:
            self.game_begin()
        
        elif self.state == Game_State.GAME:
            self.update_offsets()
            self.screen.fill(BLACK)
            self.draw_maze()
            self.draw_hud()
            for setan in self.Ghost:
                if isinstance(setan,Entity.Dumb_Ghost):
                    setan.control(current_time)
                else:
                    setan.control(current_time, self.Player)
                
                if setan.check_collision(self.Player):
                    self.life -= 1
                    if self.life == 0:
                        self.state = Game_State.GAME_OVER
                        self.game_ended(Game_State.LOSE)
                    else:
                        self.game_restart()
                
            for food in self.Food_Pellets:
                food.draw()
                if food.check_collision(self.Player):
                    self.score += food.get_score()
                    self.Food_Pellets.remove(food)
                    
            if not self.Food_Pellets:
                self.state = Game_State.GAME_OVER
                self.game_ended(Game_State.WIN)
                # self.game_over()
                    
            self.Player.move(keys, self.offset_x, self.offset_y)
            self.Player.draw(self.offset_x, self.offset_y)
            pygame.display.flip()
            
        elif self.state == Game_State.GAME_OVER:
            # self.game_()
            self.game_over()
            time.sleep(0.1)
            # print("Game Over")
            if keys[pygame.K_RETURN] or keys[pygame.K_ESCAPE]:
                print("End")
                self.running = False
        
    def run(self):
        # self.running = True
        print(self.state)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or self.state == Game_State.GAME_END:
                    # print("End")
                    self.state = Game_State.GAME_OVER
                    # self.running = False
                    # return self.game_over()
            self.update_screen()
            pygame.time.Clock().tick(30)
        self.running = True

class Game_Controller:
    def __init__(self, screen, tile_size=20, tiles_x=27, tiles_y=27, screen_width=540, screen_height=540):
        self.screen = screen
        self.state=Game_State.START
        
        self.tile_size = tile_size
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        #OPEN CLOSE VIOLATION
        self.start_menu= None
        self.game=None
        self.level=None
        self.account=None
        self.scoreboard=None
        self.achievement=None
        
        self.running = True
    
    def set_start_menu(self, start_menu):
        self.start_menu = start_menu
    def set_game(self, game):
        self.game = game
    def set_level(self, level):
        self.level = level
    def set_account(self, account):
        self.account = account
    def set_scoreboard(self, scoreboard):
        self.scoreboard = scoreboard
    def set_achievement(self, achievement):
        self.achievement = achievement
    
    def setup(self):
        Start_Menu_Manager = Start_Menu(self.screen, self.tiles_x, self.tiles_y)
        Game_Manager = Game(self.screen, 'user', tile_size=self.tile_size)
        Level = Level_Manager.Level()
        Account = Progress.Account()
        Scoreboard = Progress.Scoreboard()
        Achievement = Progress.Achievement()
        
        self.set_start_menu(Start_Menu_Manager)
        self.set_game(Game_Manager)
        self.set_level(Level)
        self.set_account(Account)
        self.set_scoreboard(Scoreboard)
        self.set_achievement(Achievement)
        
        self.account.load_data(self.account)
        self.scoreboard.load_data(self.scoreboard)
        self.achievement.load_data(self.achievement)
      
    def end(self):
        self.account.save_data(self.account)
        self.scoreboard.save_data(self.scoreboard)
        self.achievement.save_data(self.achievement)
    
    def renew(self):
        self.state=Game_State.START
        
    def run(self):
        # running = True
        while self.running:
            current_time=time.time()
            # random.seed(current_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
                    self.running = False
            
            if self.state == Game_State.START:
                self.start_menu.start_menu(self.scoreboard.get_scoreboard())
                self.state = self.start_menu.get_state()
                
            elif self.state == Game_State.MENU:
                self.start_menu.user_menu(self.account.get_account_data())
                self.state = self.start_menu.get_state()
                
            elif self.state == Game_State.NEW_USER:
                self.start_menu.handle_user_registration()
                username=self.start_menu.get_user()
                if username != "":	
                    self.level.generate_level()
                    level_data=self.level.get_level_data()
                    self.account.register(username, level_data['level'], Level_Manager.Difficulty(level_data['difficulty']).name, level_data)
                
                self.state = Game_State.MENU
                self.start_menu.set_state(self.state)
                
            elif self.state == Game_State.DELETE_USER:
                username=self.start_menu.get_user()
                if username != "":
                    self.account.delete(username)
                    
                self.state = Game_State.MENU
                self.start_menu.set_state(self.state)
                
            elif self.state == Game_State.GAME_START:
                print('Game Start')
                self.game.set_state(Game_State.GAME_START)
                self.game.set_user(self.start_menu.get_user())
                user_level=self.account.load(self.start_menu.get_user())['current_level_data']
                self.game.initialize_game(user_level, Entity.Player(self.screen))
                self.game.run()
                result=self.game.game_result()
                print(result)
                
                if result[0] == Game_State.WIN:
                    self.scoreboard.insert_score(result[1], result[2], result[3])
                    self.level.advance_level(result[3])
                    new_level_data=self.level.get_level_data()
                    self.account.update(result[1], result[2],new_level_data['level'],Level_Manager.Difficulty(new_level_data['difficulty']).name, new_level_data)
                elif result[0] == Game_State.LOSE:
                    self.scoreboard.insert_score(result[1], result[2], result[3])
                    self.account.delete(result[1])
                elif result[0] == Game_State.STOP:
                    pass
                
                self.state=Game_State.START
                self.start_menu.set_state(self.state)
                time.sleep(0.2)
                #     self.level.reset_level()
                
            # elif self.start_menu.get_state() == Game_State.GAME:
            #     # print(self.start_menu.get_difficulty())
            #     self.start_menu.set_state(Game_State.START)
            #     self.game.run()
            #     self.level.reset_level()
                
            self.start_menu.handle_event(event)
            pygame.time.Clock().tick(30)

if __name__== '__main__':
    # game_controller = Game_Controller(screen)
    # game_controller.setup()
    # game_controller.run()
    # game_controller.end()
    # print("End")
    pass