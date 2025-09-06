# import pygame
# import os

# class QuizScene:
#     def __init__(self, game):
#         self.game = game
#         self.screen = game.screen
#         self.clock = game.clock
#         self.running = True
#         self.WIDTH, self.HEIGHT = 1200, 800

#         pygame.font.init()
#         self.FONT = pygame.font.SysFont("Arial", 30)
#         self.BIG_FONT = pygame.font.SysFont("Arial", 50)

#         self.load_assets()
#         self.questions = self.get_questions()
#         self.reset_game()

#     def load_assets(self):
#         base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#         assets_dir = os.path.join(base_dir, 'assets')
#         bg_path = os.path.join(assets_dir, "soft_gradient_bg.jpg")
#         self.bg_image = pygame.image.load(bg_path)
#         self.bg_image = pygame.transform.scale(self.bg_image, (self.WIDTH, self.HEIGHT))

#     def get_questions(self):
#         return [
#             {
#                 "question": "Le trouble de stress post-traumatique (TSPT) survient généralement après :",
#                 "choices": [
#                     "Un rêve étrange",
#                     "Une blessure physique légère",
#                     "Une expérience extrêmement douloureuse ou terrifiante",
#                     "Un événement joyeux et inattendu"
#                 ],
#                 "answer": 2
#             },
#             {
#                 "question": "Pourquoi certains anciens combattants comme M. Philippe sont-ils souvent incompris ou stigmatisés dans la société ?",
#                 "choices": [
#                     "Parce qu'ils refusent de parler de leur passé",
#                     "Parce que la communauté manque de connaissances sur les traumatismes psychologiques",
#                     "Parce qu'ils vivent isolés",
#                     "Parce qu'ils sont âgés et excentriques"
#                 ],
#                 "answer": 1
#             },
#             {
#                 "question": "Certaines personnes dans la ville pensent que M. Philippe 'fait semblant'. Laquelle des affirmations suivantes est vraie à propos du TSPT ?",
#                 "choices": [
#                     "Le TSPT est une faiblesse mentale, il suffit de penser positivement pour guérir",
#                     "Le TSPT ne survient que juste après un événement traumatisant et ne peut pas durer des années",
#                     "Le TSPT est un véritable trouble psychologique, pouvant affecter les émotions, la mémoire et le comportement",
#                     "Les anciens soldats souffrent rarement de TSPT car ils sont habitués aux traumatismes"
#                 ],
#                 "answer": 2
#             },
#             # Thêm các câu hỏi khác như trong file gốc nếu cần
#         ]

#     def reset_game(self):
#         self.current_q = 0
#         self.correct = 0
#         self.selected_choice = None
#         self.show_result = False
#         self.result_time = 0
#         self.game_state = "playing"
#         self.typed_text = ""
#         self.type_index = 0
#         self.type_time = 0

#     def run(self):
#         print("▶ Đang chạy QuizScene")
#         while self.running:
#             self.handle_events()
#             if self.game_state == "playing":
#                 self.draw_question()
#                 self.update_typing()
#             elif self.game_state in ["win", "lose"]:
#                 self.draw_end_screen()
#             pygame.display.flip()
#             self.clock.tick(60)

#     def handle_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False
#                 self.game.running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if self.game_state == "playing" and not self.show_result:
#                     selected = self.get_choice(event.pos)
#                     if selected is not None:
#                         self.selected_choice = selected
#                         self.show_result = True
#                         self.result_time = pygame.time.get_ticks()
#                         if selected == self.questions[self.current_q]["answer"]:
#                             self.correct += 1
#                 elif self.game_state in ["win", "lose"]:
#                     if self.retry_btn.collidepoint(event.pos):
#                         self.reset_game()

#     def update_typing(self):
#         if not self.show_result:
#             full_text = self.questions[self.current_q]["question"]
#             if self.type_index < len(full_text):
#                 now = pygame.time.get_ticks()
#                 if now - self.type_time > 30:
#                     self.typed_text += full_text[self.type_index]
#                     self.type_index += 1
#                     self.type_time = now
#         elif pygame.time.get_ticks() - self.result_time > 1200:
#             self.current_q += 1
#             self.selected_choice = None
#             self.show_result = False
#             self.typed_text = ""
#             self.type_index = 0
#             if self.current_q >= len(self.questions):
#                 self.game_state = "win" if self.correct >= 6 else "lose"

#     def draw_question(self):
#         self.screen.blit(self.bg_image, (0, 0))
#         q = self.questions[self.current_q]

#         question_box = pygame.Rect(100, 80, self.WIDTH - 200, 140)
#         pygame.draw.rect(self.screen, (197, 209, 235), question_box, border_radius=30)
#         pygame.draw.rect(self.screen, (128, 128, 128), question_box, 5, border_radius=30)

#         lines = self.wrap_text(self.typed_text, self.FONT, question_box.width - 40)
#         for i, line in enumerate(lines):
#             text_surface = self.FONT.render(line, True, (0, 0, 0))
#             self.screen.blit(text_surface, (question_box.x + 20, question_box.y + 20 + i * 35))

#         for i, choice in enumerate(q["choices"]):
#             rect = pygame.Rect(130, 260 + i * 100, 980, 80)
#             color = (255, 235, 0)
#             if self.show_result:
#                 if i == q["answer"]:
#                     color = (57, 91, 80)
#                 elif i == self.selected_choice:
#                     color = (230, 100, 100)
#             elif i == self.selected_choice:
#                 color = (100, 170, 255)
#             elif rect.collidepoint(pygame.mouse.get_pos()):
#                 color = (57, 91, 80)

#             pygame.draw.rect(self.screen, color, rect, border_radius=15)
#             pygame.draw.rect(self.screen, (128, 128, 128), rect, 4, border_radius=15)

#             lines = self.wrap_text(choice, self.FONT, rect.width - 40)
#             for j, line in enumerate(lines):
#                 text_surface = self.FONT.render(line, True, (0, 0, 0))
#                 self.screen.blit(text_surface, (rect.x + 20, rect.y + 10 + j * 25))

#         progress_text = self.FONT.render(f"{self.correct} correct / {len(self.questions)}", True, (57, 91, 80))
#         self.screen.blit(progress_text, (20, 20))

#     def draw_end_screen(self):
#         self.screen.blit(self.bg_image, (0, 0))
#         result = self.game_state
#         msg = "🎉 Vous avez gagné !" if result == "win" else "❌ Vous avez perdu."
#         label = self.BIG_FONT.render(msg, True, (255, 255, 0))
#         self.screen.blit(label, (self.WIDTH//2 - label.get_width()//2, 250))
#         self.retry_btn = pygame.Rect(self.WIDTH//2 - 120, 400, 240, 70)
#         pygame.draw.rect(self.screen, (57, 91, 80), self.retry_btn, border_radius=6)
#         pygame.draw.rect(self.screen, (0, 0, 0), self.retry_btn, 4, border_radius=6)
#         text = self.FONT.render("Chơi lại", True, (0, 0, 0))
#         self.screen.blit(text, (self.retry_btn.x + 70, self.retry_btn.y + 20))

#     def get_choice(self, pos):
#         for i in range(4):
#             rect = pygame.Rect(130, 260 + i * 100, 980, 80)
#             if rect.collidepoint(pos):
#                 return i
#         return None

#     def wrap_text(self, text, font, max_width):
#         words = text.split(' ')
#         lines = []
#         current_line = ""
#         for word in words:
#             test_line = current_line + word + " "
#             if font.size(test_line)[0] <= max_width:
#                 current_line = test_line
#             else:
#                 lines.append(current_line.strip())
#                 current_line = word + " "
#         if current_line:
#             lines.append(current_line.strip())
#         return lines
import pygame
import os
import sys

class QuizScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        self.WIDTH, self.HEIGHT = 1200, 800

        pygame.font.init()
        self.FONT = pygame.font.SysFont("Arial", 30)
        self.BIG_FONT = pygame.font.SysFont("Arial", 50)

        self.load_assets()
        self.questions = self.get_questions()
        self.reset_game()

    def load_assets(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        assets_dir = os.path.join(base_dir, 'assets')
        bg_path = os.path.join(assets_dir, "soft_gradient_bg.jpg")
        self.bg_image = pygame.image.load(bg_path)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.WIDTH, self.HEIGHT))

    def get_questions(self):
        return [
            {
                "question": "Le trouble de stress post-traumatique (TSPT) survient généralement après :",
                "choices": [
                    "Un rêve étrange",
                    "Une blessure physique légère",
                    "Une expérience extrêmement douloureuse ou terrifiante",
                    "Un événement joyeux et inattendu"
                ],
                "answer": 2
            },
            {
                "question": "Pourquoi certains anciens combattants comme M. Huy sont-ils souvent incompris ou stigmatisés dans la société ?",
                "choices": [
                    "Parce qu'ils refusent de parler de leur passé",
                    "Parce que la communauté manque de connaissances sur les traumatismes psychologiques",
                    "Parce qu'ils vivent isolés",
                    "Parce qu'ils sont âgés et excentriques"
                ],
                "answer": 1
            },
            {
                "question": "Certaines personnes dans la ville pensent que M. Huy 'fait semblant'. Laquelle des affirmations suivantes est vraie à propos du TSPT ?",
                "choices": [
                    "Le TSPT est une faiblesse mentale, il suffit de penser positivement pour guérir",
                    "Le TSPT ne survient que juste après un événement traumatisant et ne peut pas durer des années",
                    "Le TSPT est un véritable trouble psychologique, pouvant affecter les émotions, la mémoire et le comportement",
                    "Les anciens soldats souffrent rarement de TSPT car ils sont habitués aux traumatismes"
                ],
                "answer": 2
            },
            {
                "question": "Que représente l'ODD 16 ?",
                "choices": [
                    "La technologie verte",
                    "L'éducation mondiale",
                    "La paix, la justice et des institutions efficaces",
                    "Le tourisme durable"
                ],
                "answer": 2
            },
            {
                "question": "Dans le contexte de l'ODD 16, laquelle des actions suivantes ne contribue pas à construire une société pacifique et équitable ?",
                "choices": [
                    "Encourager le dialogue entre les générations",
                    "Exclure les personnes atteintes de troubles psychologiques",
                    "Respecter la vérité et écouter les personnes vulnérables",
                    "Réduire la stigmatisation dans la communauté"
                ],
                "answer": 1
            },
            {
                "question": "Selon l'esprit de l'ODD 16, que devrait faire une communauté lorsqu'une personne vit isolée en raison d'un traumatisme ?",
                "choices": [
                    "L'ignorer pour éviter les problèmes",
                    "Chercher à créer des liens, l'écouter et l'aider à se réintégrer",
                    "La confier aux autorités compétentes",
                    "L'utiliser comme exemple pour avertir les autres"
                ],
                "answer": 1
            },
            {
                "question": "Quel comportement reflète véritablement l'esprit de l'ODD 16 ?",
                "choices": [
                    "Garder le silence face à l'injustice",
                    "Juger les autres uniquement sur leur apparence",
                    "Propager des rumeurs sur les autres",
                    "Créer un espace sûr où chacun peut s'exprimer et être écouté"
                ],
                "answer": 3
            },
            {
                "question": "Pourquoi juger une personne uniquement sur des rumeurs ou son passé va-t-il à l'encontre de l'esprit de l'ODD 16 ?",
                "choices": [
                    "Parce que cela aide la société à se protéger contre les dangers potentiels",
                    "Parce que chacun a droit au respect et à un jugement équitable, sans préjugés",
                    "Parce que seuls les proches peuvent juger une personne correctement",
                    "Parce que le passé se répète toujours et ne peut pas être changé"
                ],
                "answer": 1
            }
        ]

    def reset_game(self):
        self.current_q = 0
        self.correct = 0
        self.selected_choice = None
        self.show_result = False
        self.result_time = 0
        self.game_state = "playing"
        self.typed_text = ""
        self.type_index = 0
        self.type_time = 0

    def run(self):
        print("▶ Đang chạy QuizScene")
        while self.running:
            self.handle_events()
            if self.game_state == "playing":
                self.draw_question()
                self.update_typing()
            elif self.game_state in ["win", "lose"]:
                self.running = False
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "playing" and not self.show_result:
                    selected = self.get_choice(event.pos)
                    if selected is not None:
                        self.selected_choice = selected
                        self.show_result = True
                        self.result_time = pygame.time.get_ticks()
                        if selected == self.questions[self.current_q]["answer"]:
                            self.correct += 1

    def get_choice(self, pos):
        for i in range(4):
            rect = pygame.Rect(130, 260 + i * 100, 980, 80)
            if rect.collidepoint(pos):
                return i
        return None

    def update_typing(self):
        if not self.show_result:
            full_text = self.questions[self.current_q]["question"]
            if self.type_index < len(full_text):
                now = pygame.time.get_ticks()
                if now - self.type_time > 30:
                    self.typed_text += full_text[self.type_index]
                    self.type_index += 1
                    self.type_time = now
        elif pygame.time.get_ticks() - self.result_time > 1200:
            self.current_q += 1
            self.selected_choice = None
            self.show_result = False
            self.typed_text = ""
            self.type_index = 0
            if self.current_q >= len(self.questions):
                self.game_state = "win" if self.correct >= 6 else "lose"

    def draw_question(self):
        self.screen.blit(self.bg_image, (0, 0))
        q = self.questions[self.current_q]

        question_box = pygame.Rect(100, 80, self.WIDTH - 200, 140)
        pygame.draw.rect(self.screen, (197, 209, 235), question_box, border_radius=30)
        pygame.draw.rect(self.screen, (128, 128, 128), question_box, 5, border_radius=30)

        lines = self.wrap_text(self.typed_text, self.FONT, question_box.width - 40)
        for i, line in enumerate(lines):
            text_surface = self.FONT.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (question_box.x + 20, question_box.y + 20 + i * 35))

        for i, choice in enumerate(q["choices"]):
            rect = pygame.Rect(130, 260 + i * 100, 980, 80)
            color = (255, 235, 0)
            if self.show_result:
                if i == q["answer"]:
                    color = (57, 91, 80)
                elif i == self.selected_choice:
                    color = (230, 100, 100)
            elif i == self.selected_choice:
                color = (100, 170, 255)
            elif rect.collidepoint(pygame.mouse.get_pos()):
                color = (57, 91, 80)

            pygame.draw.rect(self.screen, color, rect, border_radius=15)
            pygame.draw.rect(self.screen, (128, 128, 128), rect, 4, border_radius=15)

            lines = self.wrap_text(choice, self.FONT, rect.width - 40)
            for j, line in enumerate(lines):
                text_surface = self.FONT.render(line, True, (0, 0, 0))
                self.screen.blit(text_surface, (rect.x + 20, rect.y + 10 + j * 25))

        progress_text = self.FONT.render(f"{self.correct} correct / {len(self.questions)}", True, (57, 91, 80))
        self.screen.blit(progress_text, (20, 20))

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

