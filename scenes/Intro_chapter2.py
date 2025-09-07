
import pygame
import sys
import os
from scenes.Dialog import DialogBox

class IntroChapter2:
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
        # Load images for Chapter 2 (C2_1 to C2_8)
        C2 = [pygame.image.load(f"assets/C2_{i+1}.{'jpg' if i >= 3 else 'png'}").convert_alpha() for i in range(8)]

        # Scale all images to screen size
        for i in range(len(C2)):
            print(i)
            C2[i] = pygame.transform.scale(C2[i], (1200, 800))


        self.all_images = C2

        # Insert repeated images where needed for the story flow

        self.script = [
            "Après une période d'échange étudiant au Vietnam, Léo est retourné dans son pays d'origine. ",
            "Il était déterminé à découvrir la vérité sur son passé.",
            "En entrant dans le salon, il a remarqué quelque chose d'étrange...",
            "Il y avait plusieurs photos sur les murs, toutes couvertes de poussière.",
            "Dans un coin, il a trouvé une vieille armoire.",
            "L'armoire semblait contenir quelque chose d'important...",
            "Léo a décidé de l'examiner de plus près.",
            "Soudain, il a entendu des pas derrière lui...",
            "C'était Monsieur Huy, qui le regardait avec un mélange de surprise et de méfiance.",
            "Monsieur Huy : Que fais-tu ici ?",
            "Léo a sorti la photo que Mme My lui avait donnée."
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
        print("▶ IntroChapter2 đang chạy...")
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

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    game = type('Game', (object,), {'screen': screen, 'clock': clock, 'running': True})()
    intro = IntroChapter2(game)
    intro.run()
    pygame.quit()
    sys.exit()