# import pygame
# import os
# import time
# import random
# from collections import deque
# from scenes.Dialog import DialogBox
# from scenes.maze_gen import generate_maze

# # Cấu hình game
# SCREEN_WIDTH = 1200
# SCREEN_HEIGHT = 800
# TILE_SIZE = 25
# MAZE_SIZE = 30

# # Màu sắc
# COLORS = {
#     '#': (0, 0, 0),
#     '.': (230, 230, 230),
#     'S': (0, 150, 255),
#     'T': (0, 200, 100)
# }, vbhjinmjk

# class Player:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.size = TILE_SIZE - 2
#         base_dir = os.path.dirname(__file__)
#         self.assets_dir = os.path.abspath(os.path.join(base_dir, "..", "assets"))
#         self.sprite = self.load_sprite("player.png")

#     def load_sprite(self, filename):
#         path = os.path.join(self.assets_dir, filename)
#         try:
#             sprite = pygame.image.load(path).convert_alpha()
#             return pygame.transform.scale(sprite, (self.size, self.size))
#         except:
#             surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
#             pygame.draw.rect(surface, (255, 0, 0), (0, 0, self.size, self.size))
#             return surface

#     def draw(self, screen, offset_x, offset_y):
#         pos_x = offset_x + self.x * TILE_SIZE + (TILE_SIZE - self.size) // 2
#         pos_y = offset_y + self.y * TILE_SIZE + (TILE_SIZE - self.size) // 2
#         screen.blit(self.sprite, (pos_x, pos_y))

#     def move(self, dx, dy, maze):
#         nx, ny = self.x + dx, self.y + dy
#         if 0 <= nx < MAZE_SIZE and 0 <= ny < MAZE_SIZE and maze[ny][nx] != '#':
#             self.x, self.y = nx, ny
#             return True
#         return False

# def compute_distance_to_target(maze):
#     dis = [[-1 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
#     for y in range(MAZE_SIZE):
#         for x in range(MAZE_SIZE):
#             if maze[y][x] == 'T':
#                 dis[y][x] = 0
#                 queue = deque([(x, y)])
#                 dx, dy = [0, 0, 1, -1], [1, -1, 0, 0]
#                 while queue:
#                     cx, cy = queue.popleft()
#                     for d in range(4):
#                         nx, ny = cx + dx[d], cy + dy[d]
#                         if 0 <= nx < MAZE_SIZE and 0 <= ny < MAZE_SIZE and maze[ny][nx] != '#' and dis[ny][nx] == -1:
#                             dis[ny][nx] = dis[cy][cx] + 1
#                             queue.append((nx, ny))
#                 return dis
#     raise ValueError("No target 'T' found")

# # Khởi tạo Pygame
# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Maze Game")
# clock = pygame.time.Clock()

# base_dir = os.path.dirname(__file__)
# assets_dir = os.path.abspath(os.path.join(base_dir, "..", "assets"))
# font = pygame.font.Font(os.path.join(assets_dir, "Pixel Emulator.otf"), 32)
# dialog = DialogBox(SCREEN_WIDTH, SCREEN_HEIGHT, font)
# dialog.text_speed = 5

# # Tạo mê cung
# generate_maze(MAZE_SIZE, "maze.txt")
# maze = [list(line.strip()) for line in open("maze.txt")][:MAZE_SIZE]
# dis = compute_distance_to_target(maze)
# initial_distance = dis[1][1]
# seen = [[False]*MAZE_SIZE for _ in range(MAZE_SIZE)]
# offset_x = (SCREEN_WIDTH - MAZE_SIZE*TILE_SIZE) // 2
# offset_y = (SCREEN_HEIGHT - MAZE_SIZE*TILE_SIZE) // 2
# player = Player(1, 1)

# # Tầng thoại
# dialog_tiers = [
#     ["Je ne peux pas dormir. Il y a quelqu’un ?", "Pourquoi est-ce que je ressens ça tout le temps ?", "C’est trop silencieux... mais aussi trop bruyant dans ma tête."],
#     ["Je suis bloqué. Je ne peux pas sortir.", "Personne ne comprend ce que je vis.", "Est-ce que je vais rester comme ça pour toujours ?"],
#     ["J’ai besoin de quelqu’un à mes côtés.", "Besoin de quelqu’un qui écoute… vraiment.", "Peut-être… que je ne suis pas seul."],
#     ["Je crois que je peux m’en sortir. Pas à pas."]
# ]

# DIALOG_COLORS = [ (20, 20, 20, 220), (50, 50, 50, 220), (90, 90, 90, 220), (130, 130, 130, 220) ]
# thresholds = [1.0, 0.85, 0.4, 0.2]
# dialog_shown = [False]*4
# dialog_queue = []
# dialog_index = 0
# dialog_timer = 0
# current_tier = -1
# switch_interval = 10
# time_delay = 0
# running = True
# while running:
#     screen.fill((0, 0, 0))
#     LEFT_font = pygame.font.SysFont(None, 30)
#     text = LEFT_font.render("Trouvez la sortie dans votre esprit", True, (255, 255, 0))
#     dist = LEFT_font.render("distance: " + str(dis[player.y][player.x]),True,(255, 255, 0))
#     screen.blit(text, (1, 1))
#     screen.blit(dist, (1, 20))
#     dt = clock.tick(60) / 1000

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if time_delay:
#                 time.sleep(time_delay)
#             if event.key == pygame.K_UP: player.move(0, -1, maze)
#             if event.key == pygame.K_DOWN: player.move(0, 1, maze)
#             if event.key == pygame.K_LEFT: player.move(-1, 0, maze)
#             if event.key == pygame.K_RIGHT: player.move(1, 0, maze)

#     # Vẽ mê cung
#     for y in range(MAZE_SIZE):
#         for x in range(MAZE_SIZE):
#             pygame.draw.rect(screen, COLORS.get(maze[y][x], (0, 0, 0)),
#                              (offset_x + x*TILE_SIZE, offset_y + y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

#     player.draw(screen, offset_x, offset_y)

#     # Cập nhật vùng đã thấy
#     for dx in range(-2, 3):
#         for dy in range(-2, 3):
#             nx, ny = player.x + dx, player.y + dy
#             if 0 <= nx < MAZE_SIZE and 0 <= ny < MAZE_SIZE:
#                 if abs(dx)+abs(dy) <= 2:
#                     seen[ny][nx] = True

#     fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
#     for y in range(MAZE_SIZE):
#         for x in range(MAZE_SIZE):
#             if not seen[y][x]:
#                 pygame.draw.rect(fog, (0, 0, 0, 250), (offset_x + x*TILE_SIZE, offset_y + y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
#     screen.blit(fog, (0, 0))

#     # Tiến trình và thoại
#     current_dis = dis[player.y][player.x]
#     progress = current_dis / initial_distance if initial_distance else 1

#     # Hiển thị thoại theo tầng tiến độ
#     for i, threshold in enumerate(thresholds):
#         if progress <= threshold and not dialog_shown[i]:
#             dialog_shown[i] = True
#             current_tier = i
#             dialog_queue = random.sample(dialog_tiers[i], len(dialog_tiers[i]))
#             dialog_index = 0
#             dialog_timer = 0
#             dialog.set_text(dialog_queue[dialog_index])
#             dialog.bg_color = DIALOG_COLORS[i]
#             break

#     # Cập nhật thời gian và đổi thoại nếu đã hiển thị xong câu trước
#     if 0 <= current_tier <= 2 and len(dialog_queue) > 1:
#         dialog_timer += dt
#         time_delay = 0.09
#         if dialog.finished and dialog_timer >= switch_interval:
#             dialog_timer = 0
#             dialog_index = (dialog_index + 1) % len(dialog_queue)
#             dialog.set_text(dialog_queue[dialog_index])

#     elif current_tier == 3:
#         dialog_timer += dt
#         time_delay = 0.15
#         if dialog.finished and dialog_timer >= switch_interval:
#             dialog_timer = 0
#             dialog.set_text(dialog_tiers[3][0])

#     # Victory
#     if maze[player.y][player.x] == 'T':
#         screen.fill((250, 248, 238))
#         victory_font = pygame.font.SysFont(None, 150)
#         text = victory_font.render("Victory!", True, (255, 255, 0))
#         screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
#         dialog.set_text("Toute souffrance a une fin, je peux marcher\nJe peux y aller")
#         dialog.draw(screen)
#         time.sleep(2)
#         pygame.display.flip()
#         break

#     dialog.update(dt)
#     dialog.draw(screen)
#     pygame.display.flip()

# pygame.quit()
# map_scene.py + point-and-click scene combined
import pygame
import sys
import os
from scenes.scene import Scene
from scenes.Dialog import DialogBox
from scenes.maze_gen import generate_maze
from collections import deque
import random
import time
 
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TILE_SIZE = 25
MAZE_SIZE = 30
COLORS = {'#': (0, 0, 0), '.': (255, 192, 203), 'S': (0, 150, 255), 'T': (0, 200, 100)}
 
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = TILE_SIZE - 2
        base_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.abspath(os.path.join(base_dir, "..", "assets"))
        self.sprite = self.load_sprite("player.png")
 
    def load_sprite(self, filename):
        path = os.path.join(self.assets_dir, filename)
        try:
            sprite = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(sprite, (self.size, self.size))
        except:
            surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(surface, (255, 0, 0), (0, 0, self.size, self.size))
            return surface
 
    def draw(self, screen, offset_x, offset_y):
        pos_x = offset_x + self.x * TILE_SIZE + (TILE_SIZE - self.size) // 2
        pos_y = offset_y + self.y * TILE_SIZE + (TILE_SIZE - self.size) // 2
        screen.blit(self.sprite, (pos_x, pos_y))
 
    def move(self, dx, dy, maze):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < MAZE_SIZE and 0 <= ny < MAZE_SIZE and maze[ny][nx] != '#':
            self.x, self.y = nx, ny
            return True
        return False
 
def compute_distance_to_target(maze):
    dis = [[-1 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
    for y in range(MAZE_SIZE):
        for x in range(MAZE_SIZE):
            if maze[y][x] == 'T':
                dis[y][x] = 0
                queue = deque([(x, y)])
                dx, dy = [0, 0, 1, -1], [1, -1, 0, 0]
                while queue:
                    cx, cy = queue.popleft()
                    for d in range(4):
                        nx, ny = cx + dx[d], cy + dy[d]
                        if 0 <= nx < MAZE_SIZE and 0 <= ny < MAZE_SIZE and maze[ny][nx] != '#' and dis[ny][nx] == -1:
                            dis[ny][nx] = dis[cy][cx] + 1
                            queue.append((nx, ny))
                return dis
    raise ValueError("No target 'T' found")
 
class MazeScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
 
    def run(self):
        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.abspath(os.path.join(base_dir, "..", "assets"))
 
        font = pygame.font.Font(os.path.join(assets_dir, "Pixel Emulator.otf"), 32)
        dialog = DialogBox(SCREEN_WIDTH, SCREEN_HEIGHT, font)
        dialog.text_speed = 5
 
        generate_maze(MAZE_SIZE, "maze.txt")
        maze = [list(line.strip()) for line in open("maze.txt")][:MAZE_SIZE]
        dis = compute_distance_to_target(maze)
        initial_distance = dis[1][1]
        seen = [[False]*MAZE_SIZE for _ in range(MAZE_SIZE)]
        offset_x = (SCREEN_WIDTH - MAZE_SIZE*TILE_SIZE) // 2
        offset_y = (SCREEN_HEIGHT - MAZE_SIZE*TILE_SIZE) // 2
        player = Player(1, 1)
 
        dialog_tiers = [
            ["Je ne peux pas dormir. Il y a quelqu’un ?", "Pourquoi est-ce que je ressens ça tout le temps ?", "C’est trop silencieux... mais aussi trop bruyant dans ma tête."],
            ["Je suis bloqué. Je ne peux pas sortir.", "Personne ne comprend ce que je vis.", "Est-ce que je vais rester comme ça pour toujours ?"],
            ["J’ai besoin de quelqu’un à mes côtés.", "Besoin de quelqu’un qui écoute… vraiment.", "Peut-être… que je ne suis pas seul."],
            ["Je crois que je peux m’en sortir. Pas à pas."]
        ]
 
        DIALOG_COLORS = [ (20, 20, 20, 220), (50, 50, 50, 220), (90, 90, 90, 220), (130, 130, 130, 220) ]
        thresholds = [1.0, 0.85, 0.4, 0.2]
        dialog_shown = [False]*4
        dialog_queue = []
        dialog_index = 0
        dialog_timer = 0
        current_tier = -1
        switch_interval = 10
        time_delay = 0
 
        while self.running:
            self.screen.fill((0, 0, 0))
            LEFT_font = pygame.font.SysFont(None, 30)
            text = LEFT_font.render("Trouvez la sortie dans votre esprit", True, (255, 255, 0))
            dist = LEFT_font.render("distance: " + str(dis[player.y][player.x]), True, (255, 255, 0))
            self.screen.blit(text, (1, 1))
            self.screen.blit(dist, (1, 20))
            dt = self.clock.tick(60) / 1000
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                elif event.type == pygame.KEYDOWN:
                    if time_delay:
                        time.sleep(time_delay)
                    if event.key == pygame.K_UP: player.move(0, -1, maze)
                    if event.key == pygame.K_DOWN: player.move(0, 1, maze)
                    if event.key == pygame.K_LEFT: player.move(-1, 0, maze)
                    if event.key == pygame.K_RIGHT: player.move(1, 0, maze)
 
            for y in range(MAZE_SIZE):
                for x in range(MAZE_SIZE):
                    pygame.draw.rect(self.screen, COLORS.get(maze[y][x], (0, 0, 0)),
                                     (offset_x + x*TILE_SIZE, offset_y + y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
 
            player.draw(self.screen, offset_x, offset_y)
 
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    nx, ny = player.x + dx, player.y + dy
                    if 0 <= nx < MAZE_SIZE and 0 <= ny < MAZE_SIZE:
                        if abs(dx)+abs(dy) <= 2:
                            seen[ny][nx] = True
 
            fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for y in range(MAZE_SIZE):
                for x in range(MAZE_SIZE):
                    if not seen[y][x]:
                        pygame.draw.rect(fog, (0, 0, 0, 250), (offset_x + x*TILE_SIZE, offset_y + y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            self.screen.blit(fog, (0, 0))
 
            current_dis = dis[player.y][player.x]
            progress = current_dis / initial_distance if initial_distance else 1
 
            for i, threshold in enumerate(thresholds):
                if progress <= threshold and not dialog_shown[i]:
                    dialog_shown[i] = True
                    current_tier = i
                    dialog_queue = random.sample(dialog_tiers[i], len(dialog_tiers[i]))
                    dialog_index = 0
                    dialog_timer = 0
                    dialog.set_text(dialog_queue[dialog_index])
                    dialog.bg_color = DIALOG_COLORS[i]
                    break
 
            if 0 <= current_tier <= 2 and len(dialog_queue) > 1:
                dialog_timer += dt
                time_delay = 0.09
                if dialog.finished and dialog_timer >= switch_interval:
                    dialog_timer = 0
                    dialog_index = (dialog_index + 1) % len(dialog_queue)
                    dialog.set_text(dialog_queue[dialog_index])
 
            elif current_tier == 3:
                dialog_timer += dt
                time_delay = 0.15
                if dialog.finished and dialog_timer >= switch_interval:
                    dialog_timer = 0
                    dialog.set_text(dialog_tiers[3][0])
 
            if maze[player.y][player.x] == 'T':
                self.screen.fill((250, 248, 238))
                victory_font = pygame.font.SysFont(None, 150)
                text = victory_font.render("Victory!", True, (255, 255, 0))
                self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
                dialog.set_text("Toute souffrance a une fin, je peux marcher\nJe peux y aller")
                dialog.draw(self.screen)
                time.sleep(2)
                pygame.display.flip()
                self.running = False
                return
 
            dialog.update(dt)
            dialog.draw(self.screen)
            pygame.display.flip()
 
