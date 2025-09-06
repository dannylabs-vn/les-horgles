# import pygame
# import os
# import time
# from scenes.scene import Scene
# from scenes.quiz_scene import QuizScene
# from scenes.maze_scene import MazeScene
# from scenes.Dialog import DialogBox
# from scenes.outro_scene import OutroScene
# class MapScene:
#     def load_assets(self):
#         project_root = os.path.dirname(os.path.dirname(__file__))
#         assets = os.path.join(project_root, "assets")
#         self.scenes = [
#             Scene(pygame.transform.scale(pygame.image.load(os.path.join(assets, "bg1.png")), (self.WIDTH, self.HEIGHT)), []),
#             Scene(pygame.transform.scale(pygame.image.load(os.path.join(assets, "bg2.png")), (self.WIDTH, self.HEIGHT)), [])
#         ]
#         self.character = pygame.transform.scale(pygame.image.load(os.path.join(assets,"Leo.png")),(533 // 1.5,690 // 1.5))
#     def __init__(self, game):
#         self.game = game
#         self.screen = game.screen
#         self.clock = game.clock
#         self.running = True
#         self.WIDTH, self.HEIGHT = 1200, 800
#         self.left_rect = pygame.Rect(0, self.HEIGHT // 2 - 40, 80, 80)
#         self.right_rect = pygame.Rect(self.WIDTH - 80, self.HEIGHT // 2 - 40, 80, 80)
#         project_root = os.path.dirname(os.path.dirname(__file__))
#         assets_path = os.path.join(project_root, "assets")       
#         self.font = pygame.font.Font(os.path.join(assets_path, "Minecraftia-Regular.ttf"), 30)
#         self.showing_dialog = False
#         self.dialog_text = ""
#         self.dialog_btn = pygame.Rect(self.WIDTH//2 - 80, 100, 160, 50)
#         self.quiz_completed = False #setting chọn theo thứ tự
#         self.load_assets()
#         self.current_scene = 0
 
#     def show_dialog(self, text):
#         self.dialog_text = text
#         self.showing_dialog = True
 
#     def draw_character(self):
#         w, h = self.character.get_size()
#         x = 2
#         y = self.screen.get_height() - 150 - h + 20
#         self.screen.blit(self.character, (x, y))
 
#     def draw_dialog(self):
#         pygame.draw.rect(self.screen, (0, 0, 0), self.dialog_btn)
#         pygame.draw.rect(self.screen, (255, 255, 255), self.dialog_btn, 2)
#         label = self.font.render("Continuer", True, (255, 255, 255))
#         self.screen.blit(label, (self.dialog_btn.centerx - label.get_width()//2, self.dialog_btn.centery - label.get_height()//2))
 
#         text_surface = self.font.render(self.dialog_text, True, (255, 255, 255))
#         self.screen.blit(text_surface, (self.WIDTH // 2 - text_surface.get_width() // 2 + 20, 50))
 
#     def fade_in(self, surface, image, duration=1000):
#         clock = pygame.time.Clock()
#         fade_img = image.copy()
#         for alpha in range(256, 0, -10):
#             fade_img.set_alpha(alpha)
#             surface.fill((0, 0, 0))
#             surface.blit(fade_img, (0, 0))
#             pygame.display.flip()
#             clock.tick(1000 // (duration // 10))
 
#     def show_character(self,text):
#         intro_text = text
#         dialog_box = DialogBox(self.WIDTH, self.HEIGHT, self.font)
#         dialog_box.text_speed = 30
#         dialog_box.set_text(intro_text)
 
#         clock = pygame.time.Clock()
#         while True:
#             dt = clock.tick(60) / 1000  
 
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False
#                     self.game.running = False
#                     return
#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     if dialog_box.skip_or_next():
#                         return
 
#             dialog_box.update(dt)
 
#             self.screen.fill((0, 0, 0))   # Xóa màn hình
#             self.draw_character()         # Vẽ nhân vật trước
#             dialog_box.draw(self.screen)  # Sau đó vẽ dialog
 
#             pygame.display.flip()
 
#     def print_Note(self, text):
#         text_speed = 10  # ký tự/giây
#         displayed_text = "REMARQUE : le PTSD (SSPT) et les événements survenus."
#         timer = 0
#         finished = False
#         clock = pygame.time.Clock()
#         project_root = os.path.dirname(os.path.dirname(__file__))
#         assets_path = os.path.join(project_root, "assets")      
#         self.font = pygame.font.Font(os.path.join(assets_path, "FONT.ttf"), 40)
#         while True:
#             dt = clock.tick(60) / 1000
#             timer += dt
 
#             if not finished:
#                 chars_to_show = int(timer * text_speed)
#                 if chars_to_show >= len(text):
#                     chars_to_show = len(text)
#                     finished = True
#                 displayed_text = text[:chars_to_show]
 
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False
#                     self.game.running = False
#                     return
#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     if finished:
#                         return
#                     else:
#                         displayed_text = text
#                         finished = True
 
#             # Vẽ nền đen mờ
#             self.screen.fill((0, 0, 0))
#             overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
#             overlay.fill((0, 0, 0, 180))
#             self.screen.blit(overlay, (0, 0))
 
#             # Render text
#             text_surface = self.font.render(displayed_text, True, (255, 255, 255))
#             text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
#             self.screen.blit(text_surface, text_rect)
 
#             pygame.display.flip()
 
 
#     def run(self):
#         self.show_character("Ce vieil homme est vraiment étrange. Je devrais peut-être jeter un œil aux alentours.")
#         stage = "map"
#         while self.running:
#             self.screen.blit(self.scenes[self.current_scene].bg, (0, 0))
 
#             pygame.draw.polygon(self.screen, (255, 255, 255), [(20, self.HEIGHT // 2), (60, self.HEIGHT // 2 - 30), (60, self.HEIGHT // 2 + 30)])
#             pygame.draw.polygon(self.screen, (255, 255, 255), [(self.WIDTH - 20, self.HEIGHT // 2), (self.WIDTH - 60, self.HEIGHT // 2 - 30), (self.WIDTH - 60, self.HEIGHT // 2 + 30)])
 
#             if self.showing_dialog:
#                 self.draw_dialog()
 
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False
#                     self.game.running = False
 
#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     pos = pygame.mouse.get_pos()
#                     if self.showing_dialog:
#                         if self.dialog_btn.collidepoint(pos):
#                             self.showing_dialog = False
#                             if stage == "quiz":
#                                 quiz = QuizScene(self.game)
#                                 self.print_Note("REMARQUE : le PTSD (SSPT) et les événements survenus.")
#                                 quiz.run()
#                                 project_root = os.path.dirname(os.path.dirname(__file__))
#                                 assets_path = os.path.join(project_root, "assets")      
#                                 self.font = pygame.font.Font(os.path.join(assets_path, "Pixel Emulator.otf"), 30)
#                                 stage = "map"
#                                 self.show_character("Peut-être que je commence à le comprendre un peu… C’est si triste.")
#                                 self.show_character("Je vais faire le tour de la maison pour voir s'il y a autre chose à trouver.")
#                             elif stage == "maze":
#                                 self.show_character("Ce livre me paraît étrange.")
#                                 self.fade_in(self.screen, self.scenes[self.current_scene].bg)
#                                 maze = MazeScene(self.game)
#                                 maze.run()
#                                 self.show_dialog("🎉 Vous avez terminé le labyrinthe !")
#                                 stage = "outro"
#                             elif stage == "outro":
#                                 outro = OutroScene(self)
#                                 outro.run()
#                         continue
 
#                     if self.left_rect.collidepoint(pos):
#                         self.current_scene = max(0, self.current_scene - 1)
#                     elif self.right_rect.collidepoint(pos):
#                         self.current_scene = min(len(self.scenes) - 1, self.current_scene + 1)
#                     else:
#                         if self.current_scene == 0:
#                             if pygame.Rect(100, 530, 100, 100).collidepoint(pos) and self.quiz_completed == False:
#                                 self.show_dialog("🎉 Vous avez trouvé le premier objet !")
#                                 stage = "quiz"
#                                 self.quiz_completed = True
#                         elif self.current_scene == 1:
#                             if pygame.Rect(510, 570, 120, 60).collidepoint(pos) and self.quiz_completed == True:
#                                 self.show_dialog("📘 Vous avez trouvé un ancien livre...")
#                                 stage = "maze"
 
#             pygame.display.flip()
#             self.clock.tick(60)
import pygame
import os
import time
from scenes.scene import Scene
from scenes.quiz_scene import QuizScene
from scenes.maze_scene import MazeScene
from scenes.Dialog import DialogBox
from scenes.outro_scene import OutroScene

class MapScene:
    def load_assets(self):
        project_root = os.path.dirname(os.path.dirname(__file__))
        assets = os.path.join(project_root, "assets")
        self.scenes = [
            Scene(pygame.transform.scale(pygame.image.load(os.path.join(assets, "bg1.png")), (self.WIDTH, self.HEIGHT)), []),
            Scene(pygame.transform.scale(pygame.image.load(os.path.join(assets, "bg2.png")), (self.WIDTH, self.HEIGHT)), [])
        ]
        self.character = pygame.transform.scale(pygame.image.load(os.path.join(assets, "Leo.png")), (533 // 1.5, 690 // 1.5))

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        self.WIDTH, self.HEIGHT = 1200, 800
        self.left_rect = pygame.Rect(0, self.HEIGHT // 2 - 40, 80, 80)
        self.right_rect = pygame.Rect(self.WIDTH - 80, self.HEIGHT // 2 - 40, 80, 80)
        project_root = os.path.dirname(os.path.dirname(__file__))
        assets_path = os.path.join(project_root, "assets")       
        self.font = pygame.font.Font(os.path.join(assets_path, "Minecraftia-Regular.ttf"), 30)
        self.showing_dialog = False
        self.dialog_text = ""
        self.dialog_btn = pygame.Rect(self.WIDTH//2 - 80, 100, 160, 50)
        self.quiz_completed = False
        self.load_assets()
        self.current_scene = 0

        # 👉 Thêm biến cho note hướng dẫn
        self.show_instruction = True
        self.instruction_rect = pygame.Rect(self.WIDTH // 2 - 300, self.HEIGHT // 2 - 200, 600, 320)
        self.instruction_close_btn = pygame.Rect(self.instruction_rect.right - 40, self.instruction_rect.top + 10, 30, 30)

    def show_dialog(self, text):
        self.dialog_text = text
        self.showing_dialog = True

    def draw_character(self):
        w, h = self.character.get_size()
        x = 2
        y = self.screen.get_height() - 150 - h + 20
        self.screen.blit(self.character, (x, y))

    def draw_dialog(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.dialog_btn)
        pygame.draw.rect(self.screen, (255, 255, 255), self.dialog_btn, 2)
        label = self.font.render("Continuer", True, (255, 255, 255))
        self.screen.blit(label, (self.dialog_btn.centerx - label.get_width()//2, self.dialog_btn.centery - label.get_height()//2))
        text_surface = self.font.render(self.dialog_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.WIDTH // 2 - text_surface.get_width() // 2 + 20, 50))

    def fade_in(self, surface, image, duration=1000):
        clock = pygame.time.Clock()
        fade_img = image.copy()
        for alpha in range(256, 0, -10):
            fade_img.set_alpha(alpha)
            surface.fill((0, 0, 0))
            surface.blit(fade_img, (0, 0))
            pygame.display.flip()
            clock.tick(1000 // (duration // 10))

    def show_character(self, text):
        dialog_box = DialogBox(self.WIDTH, self.HEIGHT, self.font)
        dialog_box.text_speed = 30
        dialog_box.set_text(text)

        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if dialog_box.skip_or_next():
                        return
            dialog_box.update(dt)
            self.screen.fill((0, 0, 0))
            self.draw_character()
            dialog_box.draw(self.screen)
            pygame.display.flip()

    def print_Note(self, text):
        text_speed = 10
        displayed_text = ""
        timer = 0
        finished = False
        clock = pygame.time.Clock()
        project_root = os.path.dirname(os.path.dirname(__file__))
        assets_path = os.path.join(project_root, "assets")      
        self.font = pygame.font.Font(os.path.join(assets_path, "FONT.ttf"), 40)
        while True:
            dt = clock.tick(60) / 1000
            timer += dt
            if not finished:
                chars_to_show = int(timer * text_speed)
                if chars_to_show >= len(text):
                    chars_to_show = len(text)
                    finished = True
                displayed_text = text[:chars_to_show]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if finished:
                        return
                    else:
                        displayed_text = text
                        finished = True
            self.screen.fill((0, 0, 0))
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            text_surface = self.font.render(displayed_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()

    # 👉 Hàm vẽ note vàng giữa màn hình
    def draw_instruction_note(self):
        pygame.draw.rect(self.screen, (255, 255, 150), self.instruction_rect, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), self.instruction_rect, 3, border_radius=10)
        pygame.draw.rect(self.screen, (200, 50, 50), self.instruction_close_btn)

    # Nút X
        small_font = pygame.font.Font(None, 25)
        x_font = small_font.render("X", True, (255, 255, 255))
        self.screen.blit(x_font, (self.instruction_close_btn.x + 7, self.instruction_close_btn.y))

    # Nội dung
        note_text = (
            "PTSD : Le TSPT est un trouble mental grave causé par des événements "
            "traumatisants comme la guerre. Invisible, il est souvent mal compris. "
            "Cela explique pourquoi des anciens combattants comme M. Huy sont parfois "
            "rejetés ou stigmatisés.\n\n"
            "📌Instruction: Sélectionnez le bon objet pour débloquer le prochain mini-jeu"
        )

    # Font nhỏ hơn để vừa khung
        instruction_font = pygame.font.Font(os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets/Minecraftia-Regular.ttf"), 20)

    # Ngắt dòng
        words = note_text.split(' ')
        lines = []
        current_line = ""
        max_width = self.instruction_rect.width - 40

        for word in words:
            test_line = current_line + word + " "
            if instruction_font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

    # Vẽ từng dòng
        line_height = instruction_font.get_height() + 4
        start_y = self.instruction_rect.top + 50
        for i, line in enumerate(lines):
            rendered_line = instruction_font.render(line.strip(), True, (0, 0, 0))
            self.screen.blit(rendered_line, (self.instruction_rect.left + 20, start_y + i * line_height))

    def run(self):
        self.show_character("Ce vieil homme est vraiment étrange. Je devrais peut-être jeter un œil aux alentours.")
        stage = "map"
        while self.running:
            self.screen.blit(self.scenes[self.current_scene].bg, (0, 0))

            # 👉 Hiển thị note khi vào bg1
            if self.current_scene == 0 and self.show_instruction:
                self.draw_instruction_note()

            pygame.draw.polygon(self.screen, (255, 255, 255), [(20, self.HEIGHT // 2), (60, self.HEIGHT // 2 - 30), (60, self.HEIGHT // 2 + 30)])
            pygame.draw.polygon(self.screen, (255, 255, 255), [(self.WIDTH - 20, self.HEIGHT // 2), (self.WIDTH - 60, self.HEIGHT // 2 - 30), (self.WIDTH - 60, self.HEIGHT // 2 + 30)])

            if self.showing_dialog:
                self.draw_dialog()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if self.show_instruction and self.instruction_close_btn.collidepoint(pos):
                        self.show_instruction = False
                        continue

                    if self.showing_dialog:
                        if self.dialog_btn.collidepoint(pos):
                            self.showing_dialog = False
                            if stage == "quiz":
                                quiz = QuizScene(self.game)
                                self.print_Note("REMARQUE : le PTSD (SSPT) et les événements survenus.")
                                quiz.run()
                                project_root = os.path.dirname(os.path.dirname(__file__))
                                assets_path = os.path.join(project_root, "assets")      
                                self.font = pygame.font.Font(os.path.join(assets_path, "Pixel Emulator.otf"), 30)
                                stage = "map"
                                self.show_character("Peut-être que je commence à le comprendre un peu… C’est si triste.")
                                self.show_character("Je vais faire le tour de la maison pour voir s'il y a autre chose à trouver.")
                            elif stage == "maze":
                                self.show_character("Ce livre me paraît étrange.")
                                self.fade_in(self.screen, self.scenes[self.current_scene].bg)
                                maze = MazeScene(self.game)
                                maze.run()
                                self.show_dialog("🎉 Vous avez terminé le labyrinthe !")
                                stage = "outro"
                            elif stage == "outro":
                                outro = OutroScene(self)
                                outro.run()
                        continue

                    if self.left_rect.collidepoint(pos):
                        self.current_scene = max(0, self.current_scene - 1)
                    elif self.right_rect.collidepoint(pos):
                        self.current_scene = min(len(self.scenes) - 1, self.current_scene + 1)
                    else:
                        if self.current_scene == 0:
                            if pygame.Rect(100, 530, 100, 100).collidepoint(pos) and not self.quiz_completed:
                                self.show_dialog("🎉 Vous avez trouvé le premier objet !")
                                stage = "quiz"
                                self.quiz_completed = True
                        elif self.current_scene == 1:
                            if pygame.Rect(510, 570, 120, 60).collidepoint(pos) and self.quiz_completed:
                                self.show_dialog("📘 Vous avez trouvé un ancien livre...")
                                stage = "maze"

            pygame.display.flip()
            self.clock.tick(60)




