# import pygame
# from scenes.Dialog import DialogBox

# class OutroScene:
#     def __init__(self, game):
#         self.game = game
#         self.screen = game.screen
#         self.clock = game.clock
#         self.running = True

#         self.font = pygame.font.Font('assets/Minecraftia-Regular.ttf', 28)
#         self.dialog = DialogBox(1200, 800, self.font)

#         # Load các frame hình ảnh từ P4_1 đến P4_14
#         self.frames = [
#             pygame.transform.scale(pygame.image.load(f"assets/P4_{i+1}.png").convert_alpha(), (1200, 800))
#             for i in range(14)
#         ]

#         # Danh sách thoại từng frame
#         self.scripts = [
#             [  # P4_1
#                 "Léo: Ugh… J’ai une sensation étrange… c-c’est comme si ça tournait en boucle dans ma tête…",
#                 "Léo: Ughh... J’ai de plus en plus mal à la tête… Pourquoi ça m’arrive ?"
#             ],
#             [  # P4_2
#                 "Voici Huy, un jeune soldat ayant servi dans l’armée vietnamienne pendant la guerre.",
#                 "Il était particulièrement optimiste, plein de vie, et se battait toujours de tout cœur pour son peuple bien-aimé."
#             ],
#             [  # P4_3
#                 "De plus, il n’était pas seulement un soldat fidèle, mais aussi un camarade, un ami exceptionnel.",
#                 "Toujours prêt à aider les autres dans la misère, sans jamais rien attendre en retour.",
#                 "Même dans les circonstances les plus difficiles, il gardait toujours son optimisme.",
#                 "Et il combattait avec le sourire aux lèvres, comme pour rassurer ceux autour de lui."
#             ],
#             [  # P4_4
#                 "Et pourtant, jour après jour, ses camarades tombaient les uns après les autres. La guerre était trop brutale, les pertes ne cessaient d’augmenter. ",
#                 "Et un jour, son camarade, son meilleur ami Minh, fut gravement blessé à la poitrine par une balle ennemie, alors qu’il avait déjà une forte fièvre. Alité, il a agonisé quelques minutes avant de s’éteindre."
#             ],
#             [  # P4_5
#                 "Huy murmurait sans cesse : Ne me laisse pas, Minh… Minh… tu m’entends ? Minh… ",
#                 "Le camarade Minh s’en est allé, laissant Huy avec le cœur brisé. Le sourire de ce jeune soldat d’autrefois s’est peu à peu effacé."
#             ],
#             [  # P4_6
#                 "Le temps passe, mais les blessures psychologiques et les visages de ses camarades continuent de le hanter",
#                 "Parfois, il se tourmente lui-même, se demandant pourquoi il n’a pas pu protéger ceux qui lui étaient les plus chers.",
#                 "Huy : Pourquoiii ? Pourquoi la vie me traite-t-elle aussi cruellement ? (Des larmes commencent à couler lentement sur son visage)"
#             ],
#             [  # P4_7
#                 "Jour après jour, cette blessure s’approfondissait, et son esprit ne pouvait plus jamais redevenir comme avant."
#             ],
#             [  # P4_8
#                 "Ces pensées négatives se sont accumulées au fil du temps, menant Huy à développer un trouble de stress post-traumatique (TSPT)."
#             ],
#             [  # P4_9
#                 "Chaque fois qu’il sortait dans la rue, les gens le regardaient avec méfiance, le prenant pour un marginal, un homme troublé mentalement.",
#                 "Certains allaient jusqu’à chuchoter : “Il paraît qu’autrefois, il aurait causé la mort de ses camarades… C’est pour ça qu’il est comme ça maintenant.”"
#             ],
#             [  # P4_10
#                 "En entendant de telles paroles, il sursauta, paniqua, fut bouleversé — un véritable choc émotionnel l’envahit en cet instant."
#             ],
#             [  # P4_11
#                 "Léo (ouvre les yeux lentement) : Huh… Où suis-je ?",
#                 "Huy : Tu t’es évanoui, mon garçon… Mais tout va bien maintenant.",
#                 "Léo : Monsieur, j’ai fait un rêve très étrange… mais je crois que j’ai enfin compris ce qui s’est passé pour vous.",
#                 "Léo : Laissez-moi vous aider, d’accord ?",
#                 "Huy : Petit, tu sais… il y a des choses dans la vie qu’on ne peut pas changer, même en connaissant le résultat à l’avance.",
#                 "Léo : Donnez-vous une chance, redonnez un sens à votre vie.",
#                 "Léo : Ce qui est arrivé… ce n’est pas votre faute. C’est la vie. Cela fait partie de la vie.",
#                 "Léo : Nous devons apprendre à vivre… et à accepter.",
#                 "Le vieux vétéran, comme réveillé par ces paroles, réfléchit profondément… et décida de donner au garçon une chance de l’aider."
#             ],
#             [#P4_12
#                 "Le temps passe, voilà déjà un an qui s’est écoulé…"
                
#             ],
#             [#P4_13 
#                 "Léo : C’est toujours moi, Léo. Aujourd’hui, je retourne à la bibliothèque municipale, mais avec une émotion très différente : celle du bonheur." 
#             ],
#             [#P4_14 
#                 "Léo : Tu ne trouves pas que cet homme te semble familier ? C’est Monsieur Huy. Après un an à l’aider à surmonter son trouble de stress post-traumatique et à lui trouver un nouvel emploi, il est maintenant devenu le sous-bibliothécaire de la bibliothèque municipale.",
#                 "Depuis, lui et Mademoiselle My travaillent côte à côte à la bibliothèque municipale"

#             ],
            
#         ]

#         self.current_frame = 0
#         self.dialog_index = 0
#         self.dialog.set_text(self.scripts[self.current_frame][self.dialog_index])
#         self.fade_done = False

#     def fade_to_black(self, duration=1200):
#         fade_surface = pygame.Surface((1200, 800))
#         fade_surface.fill((0, 0, 0))
#         step = 255 // (duration // 30)
#         for alpha in range(0, 256, step):
#             fade_surface.set_alpha(alpha)
#             self.screen.blit(self.frames[self.current_frame], (0, 0))
#             self.dialog.draw(self.screen)
#             self.screen.blit(fade_surface, (0, 0))
#             pygame.display.flip()
#             self.clock.tick(60)

#     def fade_in(self, image, duration=1000):
#         clock = pygame.time.Clock()
#         fade_surface = pygame.Surface((1200, 800))
#         for alpha in range(255, -1, -15):
#             self.screen.blit(image, (0, 0))
#             fade_surface.set_alpha(alpha)
#             fade_surface.fill((0, 0, 0))
#             self.screen.blit(fade_surface, (0, 0))
#             pygame.display.flip()
#             clock.tick(1000 // (duration // 15))

#     def eye_open_transition(self, image, duration=1000):
#         clock = pygame.time.Clock()
#         steps = 45
#         for step in range(steps + 1):
#             t = step / steps
#             radius = int(t * 200)  # max radius

#             # Mặt nạ đen
#             mask = pygame.Surface((1200, 800), pygame.SRCALPHA)
#             mask.fill((0, 0, 0, 255))

#             # Vị trí hai con mắt (elip)
#             left_eye_rect = pygame.Rect(300 - radius, 400 - radius // 2, radius * 2, radius)
#             right_eye_rect = pygame.Rect(900 - radius, 400 - radius // 2, radius * 2, radius)

#             # Xóa hai hình elip khỏi mặt nạ (giống mở mắt)
#             pygame.draw.ellipse(mask, (0, 0, 0, 0), left_eye_rect)
#             pygame.draw.ellipse(mask, (0, 0, 0, 0), right_eye_rect)

#             # Áp dụng hiệu ứng lên màn hình
#             self.screen.blit(image, (0, 0))
#             self.screen.blit(mask, (0, 0))
#             pygame.display.flip()
#             clock.tick(1000 // (duration // steps))


#     def run(self):
#         print("▶ OutroScene đang chạy...")
#         while self.running:
#             dt = self.clock.tick(60) / 1000

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False
#                     self.game.running = False

#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     if not self.dialog.finished:
#                         self.dialog.skip_or_next()
#                         continue

#                     self.dialog_index += 1
#                     if self.dialog_index < len(self.scripts[self.current_frame]):
#                         self.dialog.set_text(self.scripts[self.current_frame][self.dialog_index])
#                     else:
#                         self.current_frame += 1
#                         if self.current_frame < len(self.frames):
#                             self.dialog_index = 0
#                             if self.current_frame == 10:
#                                 self.eye_open_transition(self.frames[self.current_frame])
#                             else:
#                                 self.fade_in(self.frames[self.current_frame])
#                             self.dialog.set_text(self.scripts[self.current_frame][self.dialog_index])
#                         else:
#                             if not self.fade_done:
#                                 self.fade_to_black()
#                                 self.fade_done = True
#                                 self.running = False

#             self.dialog.update(dt)
#             self.screen.blit(self.frames[self.current_frame], (0, 0))
#             self.dialog.draw(self.screen)
#             pygame.display.flip()
import pygame
from scenes.Dialog import DialogBox

class OutroScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True

        self.font = pygame.font.Font('assets/Minecraftia-Regular.ttf', 28)
        self.dialog = DialogBox(1200, 800, self.font)

        self.frames = [
            pygame.transform.scale(pygame.image.load(f"assets/P4_{i+1}.png").convert_alpha(), (1200, 800))
            for i in range(14)
        ]

        self.scripts = [
            [  # P4_1
                "Léo: Ugh… J’ai une sensation étrange… c-c’est comme si ça tournait en boucle dans ma tête…",
                "Léo: Ughh... J’ai de plus en plus mal à la tête… Pourquoi ça m’arrive ?"
            ],
            [  # P4_2
                "Voici Huy, un jeune soldat ayant servi dans l’armée vietnamienne pendant la guerre.",
                "Il était particulièrement optimiste, plein de vie, et se battait toujours de tout cœur pour son peuple bien-aimé."
            ],
            [  # P4_3
                "De plus, il n’était pas seulement un soldat fidèle, mais aussi un camarade, un ami exceptionnel.",
                "Toujours prêt à aider les autres dans la misère, sans jamais rien attendre en retour.",
                "Même dans les circonstances les plus difficiles, il gardait toujours son optimisme.",
                "Et il combattait avec le sourire aux lèvres, comme pour rassurer ceux autour de lui."
            ],
            [  # P4_4
                "Et pourtant, jour après jour, ses camarades tombaient les uns après les autres. La guerre était trop brutale, les pertes ne cessaient d’augmenter. ",
                "Et un jour, son camarade, son meilleur ami Minh, fut gravement blessé à la poitrine par une balle ennemie, alors qu’il avait déjà une forte fièvre. Alité, il a agonisé quelques minutes avant de s’éteindre."
            ],
            [  # P4_5
                "Huy murmurait sans cesse : Ne me laisse pas, Minh… Minh… tu m’entends ? Minh… ",
                "Le camarade Minh s’en est allé, laissant Huy avec le cœur brisé. Le sourire de ce jeune soldat d’autrefois s’est peu à peu effacé."
            ],
            [  # P4_6
                "Le temps passe, mais les blessures psychologiques et les visages de ses camarades continuent de le hanter",
                "Parfois, il se tourmente lui-même, se demandant pourquoi il n’a pas pu protéger ceux qui lui étaient les plus chers.",
                "Huy : Pourquoiii ? Pourquoi la vie me traite-t-elle aussi cruellement ? (Des larmes commencent à couler lentement sur son visage)"
            ],
            [  # P4_7
                "Jour après jour, cette blessure s’approfondissait, et son esprit ne pouvait plus jamais redevenir comme avant."
            ],
            [  # P4_8
                "Ces pensées négatives se sont accumulées au fil du temps, menant Huy à développer un trouble de stress post-traumatique (TSPT)."
            ],
            [  # P4_9
                "Chaque fois qu’il sortait dans la rue, les gens le regardaient avec méfiance, le prenant pour un marginal, un homme troublé mentalement.",
                "Certains allaient jusqu’à chuchoter : “Il paraît qu’autrefois, il aurait causé la mort de ses camarades… C’est pour ça qu’il est comme ça maintenant.”"
            ],
            [  # P4_10
                "En entendant de telles paroles, il sursauta, paniqua, fut bouleversé — un véritable choc émotionnel l’envahit en cet instant."
            ],
            [  # P4_11
                "Léo (ouvre les yeux lentement) : Huh… Où suis-je ?",
                "Huy : Tu t’es évanoui, mon garçon… Mais tout va bien maintenant.",
                "Léo : Monsieur, j’ai fait un rêve très étrange… mais je crois que j’ai enfin compris ce qui s’est passé pour vous.",
                "Léo : Laissez-moi vous aider, d’accord ?",
                "Huy : Petit, tu sais… il y a des choses dans la vie qu’on ne peut pas changer, même en connaissant le résultat à l’avance.",
                "Léo : Donnez-vous une chance, redonnez un sens à votre vie.",
                "Léo : Ce qui est arrivé… ce n’est pas votre faute. C’est la vie. Cela fait partie de la vie.",
                "Léo : Nous devons apprendre à vivre… et à accepter.",
                "Le vieux vétéran, comme réveillé par ces paroles, réfléchit profondément… et décida de donner au garçon une chance de l’aider."
            ],
            [  # P4_12
                "Le temps passe, voilà déjà un an qui s’est écoulé…"
            ],
            [  # P4_13
                "Léo : C’est toujours moi, Léo. Aujourd’hui, je retourne à la bibliothèque municipale, mais avec une émotion très différente : celle du bonheur."
            ],
            [  # P4_14
                "Léo : Tu ne trouves pas que cet homme te semble familier ? C’est Monsieur Huy. Après un an à l’aider à surmonter son trouble de stress post-traumatique et à lui trouver un nouvel emploi, il est maintenant devenu le sous-bibliothécaire de la bibliothèque municipale.",
                "Depuis, lui et Mademoiselle My travaillent côte à côte à la bibliothèque municipale"
            ],
        ]

        self.current_frame = 0
        self.dialog_index = 0
        self.dialog.set_text(self.scripts[self.current_frame][self.dialog_index])
        self.fade_done = False

    def fade_to_black(self, duration=1200):
        fade_surface = pygame.Surface((1200, 800))
        fade_surface.fill((0, 0, 0))
        step = 255 // (duration // 30)
        for alpha in range(0, 256, step):
            fade_surface.set_alpha(alpha)
            self.screen.blit(self.frames[self.current_frame], (0, 0))
            self.dialog.draw(self.screen)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

    def fade_in(self, image, duration=1000):
        clock = pygame.time.Clock()
        fade_surface = pygame.Surface((1200, 800))
        for alpha in range(255, -1, -15):
            self.screen.blit(image, (0, 0))
            fade_surface.set_alpha(alpha)
            fade_surface.fill((0, 0, 0))
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            clock.tick(1000 // (duration // 15))

    def eye_open_transition(self, image, duration=1000):
        clock = pygame.time.Clock()
        steps = 45
        for step in range(steps + 1):
            t = step / steps
            radius = int(t * 200)
            mask = pygame.Surface((1200, 800), pygame.SRCALPHA)
            mask.fill((0, 0, 0, 255))
            left_eye_rect = pygame.Rect(300 - radius, 400 - radius // 2, radius * 2, radius)
            right_eye_rect = pygame.Rect(900 - radius, 400 - radius // 2, radius * 2, radius)
            pygame.draw.ellipse(mask, (0, 0, 0, 0), left_eye_rect)
            pygame.draw.ellipse(mask, (0, 0, 0, 0), right_eye_rect)
            self.screen.blit(image, (0, 0))
            self.screen.blit(mask, (0, 0))
            pygame.display.flip()
            clock.tick(1000 // (duration // steps))

    def run(self):
        print("▶ OutroScene đang chạy...")
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.dialog.finished:
                        self.dialog.skip_or_next()
                        continue

                    self.dialog_index += 1
                    if self.dialog_index < len(self.scripts[self.current_frame]):
                        self.dialog.set_text(self.scripts[self.current_frame][self.dialog_index])
                    else:
                        self.current_frame += 1
                        if self.current_frame < len(self.frames):
                            self.dialog_index = 0

                            if self.current_frame == 10:
                                self.eye_open_transition(self.frames[self.current_frame])
                            elif self.current_frame == 12:
                                self.fade_to_black(duration=800)
                                self.fade_in(self.frames[self.current_frame], duration=800)
                            else:
                                self.fade_in(self.frames[self.current_frame])

                            self.dialog.set_text(self.scripts[self.current_frame][self.dialog_index])
                        else:
                            if not self.fade_done:
                                self.fade_to_black()
                                self.fade_done = True
                                self.running = False

            self.dialog.update(dt)
            self.screen.blit(self.frames[self.current_frame], (0, 0))
            self.dialog.draw(self.screen)
            pygame.display.flip()
