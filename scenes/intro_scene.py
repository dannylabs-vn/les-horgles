import pygame
import sys
from scenes.Dialog import DialogBox

class IntroScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True

        self.count = 0
        self.font = pygame.font.Font('assets/Minecraftia-Regular.ttf', 28)
        self.dialog = DialogBox(1200, 800, self.font)
        self.load_images()
        self.dialog.set_text(self.script[0])
        self.fade_in(self.screen, self.current_image)

    def load_images(self):
        P1 = [pygame.image.load(f"assets/P1_{i+1}.png").convert_alpha() for i in range(7)]
        P2 = [pygame.image.load(f"assets/P2_{i+1}.png").convert_alpha() for i in range(3)]
        P3 = [pygame.image.load(f"assets/P3_{i+1}.png").convert_alpha() for i in range(6)]

        for lst in [P1, P2, P3]:
            for i in range(len(lst)):
                lst[i] = pygame.transform.scale(lst[i], (1200, 800))

        self.all_images = P1 + P2 + P3

        self.all_images.insert(1, self.all_images[0])     # P1_1 again
        self.all_images.insert(5, P1[3])                  # P1_4
        self.all_images.insert(6, P1[4])                  # P1_5 first
        self.all_images.insert(7, P1[4])                  # P1_5 second
        self.all_images.insert(8, P1[5])                  # P1_6
        self.all_images.insert(9, P1[6])                  # P1_7
        self.all_images.insert(10, P2[0])                 # P2_1
        self.all_images.insert(11, P2[1])                 # P2_2
        self.all_images.insert(12, P2[2])                 # P2_3
        self.all_images.insert(13, P3[0])                 # P3_1 first
        self.all_images.insert(14, P3[0])                 # P3_1 second
        self.all_images.insert(15, P3[1])
        self.all_images.insert(16, P3[1])
        self.all_images.insert(17, P3[2])
        self.all_images.insert(18, P3[3])
        self.all_images.insert(19, P3[4])
        self.all_images.insert(20, P3[5])                 # P3_6 
        self.script = [
            "C'est Léo, un adolescent étranger étudiant dans un lycée vietnamien passionné de philosophie et sensible aux enjeux sociaux",
            "Récemment, il a perdu des points de comportement à l’école parce qu’il était trop absorbé par la lecture de livres sur l’histoire et la guerre",
            "À la fin du cours, Léo parle à Mme Hoa de ses points",
            "Hoa : Je te donne une mission : aide une personne en difficulté dans la ville, pour réfléchir à la justice et à la solidarité",
            "Ensuite, il est allé à la bibliothèque municipale pour chercher des documents",
            "À la bibliothèque, alors que Léo cherche des documents, il rencontre Mme My.",
            "Elle lui parle de Monsieur Huy, un ancien soldat que tout le monde appelle “le fou”.",
            "Puis, elle lui tend une vieille enveloppe.",
            "Dans l’enveloppe, il y a la photo d’un jeune homme en uniforme militaire. Mme My explique que personne au village n’écoute Monsieur Huy. Elle demande alors à Léo de découvrir la vérité sur son passé.",
            "C’est ainsi que commence son aventure.",
            "Dans la rue, Léo voit un homme en train de crier.",
            "Les passants l’évitent tous. Soudain, il comprend : c’est Monsieur Huy.",
            "Léo décide alors de le suivre jusqu’à chez lui.",
            "Quand il est arrivé au bout de la rue, il a vu que Monsieur Huy avait disparu."
            "Devant lui, il y avait une vieille maison mystérieuse.",
            "Il est arrivé devant une vieille maison abandonnée.",
            "Poussé par la curiosité, il est entré dans la maison et a vu Monsieur Huy tenant un cadre photo ",
            "Il était en train de murmurer des mots incompréhensibles",
            "Monsieur Huy : @#$%^&*!@###!@@!... ",
            "En voyant Léo, Monsieur Huy s’est précipité vers l’intérieur de la maison.",
            "Trouvant cela étrange, le jeune homme l’a suivi à l’intérieur",
            "Finalement, il est arrivé jusqu’au salon de Monsieur Huy",
        ]

        self.current_image = self.all_images[0]

    def fade_in(self, surface, image, duration=500):
        clock = pygame.time.Clock()
        alpha_img = image.copy()
        for alpha in range(0, 256, 10):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
            alpha_img.set_alpha(alpha)
            surface.fill((0, 0, 0))
            surface.blit(alpha_img, (0, 0))
            pygame.display.flip()
            clock.tick(1000 // (duration // 10))

    def run(self):
        print("▶ IntroScene đang chạy...")
        while self.running and self.count < len(self.script):
            dt = self.clock.tick(60) / 5000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.dialog.skip_or_next():
                        self.count += 1
                        if self.count < len(self.script) and self.count < len(self.all_images):
                            new_image = self.all_images[self.count]
                            if new_image != self.current_image:
                                self.current_image = new_image
                                self.dialog.set_text(self.script[self.count])
                                self.fade_in(self.screen, self.current_image)
                            else:
                                self.current_image = new_image
                                self.dialog.set_text(self.script[self.count])
                        else:
                            self.running = False

            self.dialog.update(dt)
            self.screen.blit(self.current_image, (0, 0))
            self.dialog.draw(self.screen)
            pygame.display.flip()