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
        # Load only 7 images
        self.all_images = [
            pygame.image.load("assets/P1_1.png").convert_alpha(),
            pygame.image.load("assets/P1_4.png").convert_alpha(),
            pygame.image.load("assets/P2_1.png").convert_alpha(),
            pygame.image.load("assets/P2_3.png").convert_alpha(),
            pygame.image.load("assets/P3_1.png").convert_alpha(),
            pygame.image.load("assets/P3_3.png").convert_alpha(),
            pygame.image.load("assets/P3_6.png").convert_alpha()
        ]

        # Scale all images
        for i in range(len(self.all_images)):
            self.all_images[i] = pygame.transform.scale(self.all_images[i], (1200, 800))

        self.script = [
            # Image 1 - School scene
            "C'est Léo, un adolescent étranger étudiant dans un lycée vietnamien passionné de philosophie et sensible aux enjeux sociaux",
            "Récemment, il a perdu des points de comportement à l'école parce qu'il était trop absorbé par la lecture de livres sur l'histoire et la guerre",
            "À la fin du cours, Léo parle à Mme Hoa de ses points",
            "Hoa : Je te donne une mission : aide une personne en difficulté dans la ville, pour réfléchir à la justice et à la solidarité",

            # Image 2 - Library scene
            "Ensuite, il est allé à la bibliothèque municipale pour chercher des documents",
            "À la bibliothèque, alors que Léo cherche des documents, il rencontre Mme My.",
            "Elle lui parle de Monsieur Huy, un ancien soldat que tout le monde appelle 'le fou'",
            "Dans l'enveloppe, il y a la photo d'un jeune homme en uniforme militaire",

            # Image 3 - Street scene
            "C'est ainsi que commence son aventure",
            "Dans la rue, Léo voit un homme en train de crier",
            "Les passants l'évitent tous. Soudain, il comprend : c'est Monsieur Huy",
            "Léo décide alors de le suivre jusqu'à chez lui",

            # Image 4 - Following scene
            "Il suit Monsieur Huy discrètement dans les rues",
            "Les rues deviennent de plus en plus étroites et sombres",
            "Quand il est arrivé au bout de la rue, il a vu que Monsieur Huy avait disparu",
            "Devant lui, il y avait une vieille maison mystérieuse",

            # Image 5 - House exterior
            "Il est arrivé devant une vieille maison abandonnée",
            "La maison semblait inhabitée depuis longtemps",
            "Les fenêtres étaient couvertes de poussière",
            "Poussé par la curiosité, il s'approche de l'entrée",

            # Image 6 - Inside house
            "À l'intérieur, il trouve Monsieur Huy tenant un cadre photo",
            "Il était en train de murmurer des mots incompréhensibles",
            "Monsieur Huy : @#$%^&*!@###!@@!...",
            "En voyant Léo, Monsieur Huy s'est précipité vers l'intérieur de la maison",

            # Image 7 - Final scene
            "Trouvant cela étrange, le jeune homme l'a suivi à l'intérieur",
            "Les couloirs de la maison sont remplis de vieux souvenirs",
            "Des photos jaunies tapissent les murs",
            "Finalement, il est arrivé jusqu'au salon de Monsieur Huy"
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
                        if self.count < len(self.script):
                            # Change image every 4 messages
                            new_image = self.all_images[self.count // 4]
                            if new_image != self.current_image:
                                self.current_image = new_image
                                self.fade_in(self.screen, self.current_image)
                            self.dialog.set_text(self.script[self.count])
                        else:
                            self.running = False

            self.dialog.update(dt)
            self.screen.blit(self.current_image, (0, 0))
            self.dialog.draw(self.screen)
            pygame.display.flip()