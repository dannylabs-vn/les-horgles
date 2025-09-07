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
        
        # Font loading with fallback
        try:
            self.font = pygame.font.Font('assets/Minecraftia-Regular.ttf', 28)
        except:
            try:
                self.font = pygame.font.Font('assets/fonts/Minecraftia-Regular.ttf', 28)
            except:
                print("Warning: Could not load Minecraftia font, using default")
                self.font = pygame.font.Font(None, 28)
        
        self.dialog = DialogBox(1200, 800, self.font)
        self.load_images()
        self.dialog.set_text(self.script[0])
        self.fade_in(self.screen, self.current_image)

    def load_images(self):
        try:
            # Load images for Chapter 2 (C2_1 to C2_8)
            C2 = []
            for i in range(8):
                try:
                    if i >= 3:  # jpg for images 4-8
                        img_path = f"assets/C2_{i+1}.jpg"
                    else:       # png for images 1-3
                        img_path = f"assets/C2_{i+1}.png"
                    
                    if os.path.exists(img_path):
                        img = pygame.image.load(img_path).convert_alpha()
                    else:
                        # Create placeholder if image doesn't exist
                        print(f"Warning: Image {img_path} not found, creating placeholder")
                        img = pygame.Surface((1200, 800))
                        img.fill((50, 50, 100))  # Dark blue placeholder
                        
                    # Scale to screen size
                    img = pygame.transform.scale(img, (1200, 800))
                    C2.append(img)
                    
                except Exception as e:
                    print(f"Error loading image C2_{i+1}: {e}")
                    # Create placeholder
                    placeholder = pygame.Surface((1200, 800))
                    placeholder.fill((50, 50, 100))
                    C2.append(placeholder)

            # Create arrays for images and scripts
            self.all_images = []
            self.script = []
            
            # Part 1 - C2_1: Léo returns home
            part1_scripts = [
                "Après une période d'échange étudiant au Vietnam, Léo est retourné dans son pays d'origine.",
            ]
            self.script.extend(part1_scripts)
            self.all_images.extend([C2[0]] * len(part1_scripts))

            # Part 2 - C2_2: Phone conversation
            part2_scripts = [
                "Léo : Je suis tellement heureux de rentrer chez moi, je vais enfin revoir Paul.",
                "Léo : Salut, je viens d'arriver. Frère, ça va ? Si tu es libre ce week-end, viens prendre un café avec moi.",
                "Paul : Je ne vais pas très bien… J'ai quelque chose à te demander…",
                "Léo se demande : Qu'est-ce qui se passe avec lui ?"
            ]
            self.script.extend(part2_scripts)
            self.all_images.extend([C2[1]] * len(part2_scripts))

            # Part 3 - C2_3: Meeting Paul
            part3_scripts = [
                "Léo : Salut Paul, ça fait si longtemps qu'on ne s'est pas vus. J'espérais que tu allais bien."
            ]
            self.script.extend(part3_scripts)
            self.all_images.extend([C2[2]] * len(part3_scripts))

            # Part 4 - C2_4: Paul reveals the truth
            part4_scripts = [
                "Léo : Qu'est-ce qui t'est arrivé ?",
                "Paul : Je suis tombé, ce n'est rien.",
                "Léo : Vraiment ? Ces bleus ne ressemblent pas à une simple chute.",
                "Paul : Je… en fait… Tu te souviens de ce dont je voulais te parler ?",
                "Paul : La vérité, c'est que je me fais harceler par certains camarades à l'école.",
                "Léo : QUEL DOMMAGE !",
                "Paul : Maintenant je ne sais plus quoi faire… S'il te plaît, aide-moi.",
                "Léo : D'accord, je vais t'aider. Allons à ton école pour voir ce qu'il en est."
            ]
            self.script.extend(part4_scripts)
            self.all_images.extend([C2[3]] * len(part4_scripts))

            # Part 5 - C2_5: At school - Paul isolated
            part5_scripts = [
                "En classe, Paul est isolé… même de la gomme collée sur sa chaise.",
                "Paul (pensée) : J'y suis… habitué…",
                "Léo (pensée) : Comment peuvent-ils le traiter ainsi ?"
            ]
            self.script.extend(part5_scripts)
            self.all_images.extend([C2[4]] * len(part5_scripts))

            # Part 6 - C2_6: The slapping incident
            part6_scripts = [
                "Soudain, un élève se lève… CLAC ! – il gifle Paul."
                "Paul (abasourdi) :  …Pourquoi… "
                " Léo (en colère) : Arrête tout de suite !!! "
            ]
            self.script.extend(part6_scripts)
            self.all_images.extend([C2[5]] * len(part6_scripts))

            # Part 7 - C2_7: Léo's intervention
            part7_scripts = [
                "La tête de Léo se met à lui faire mal. Des souvenirs défilent… Paul a déjà subi tant de harcèlements."
                " Léo (paniqué) : Ça… ce sont les souvenirs de Paul ?!"
            ]
            self.script.extend(part7_scripts)
            self.all_images.extend([C2[6]] * len(part7_scripts))

            # Part 8 - C2_8: Paul's diary perspective
            part8_scripts = [
                "En rouvrant les yeux, Léo comprend… il est devenu Paul dans le passé."
                " Léo (dans le corps de Paul) : Oh non… je suis vraiment devenu Paul… "
            ]
            self.script.extend(part8_scripts)
            self.all_images.extend([C2[7]] * len(part8_scripts))

            self.current_image = self.all_images[0]
            
        except Exception as e:
            print(f"Error in load_images: {e}")
            # Create minimal fallback
            self.script = ["Erreur de chargement des images. Appuyez pour continuer."]
            placeholder = pygame.Surface((1200, 800))
            placeholder.fill((50, 50, 100))
            self.all_images = [placeholder]
            self.current_image = placeholder

    def fade_in(self, surface, image, duration=500):
        """Fade in effect for image transitions"""
        if not surface or not image:
            return
            
        clock = pygame.time.Clock()
        alpha_img = image.copy()
        
        try:
            for alpha in range(0, 256, 10):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.game.running = False
                        return
                        
                alpha_img.set_alpha(alpha)
                surface.fill((0, 0, 0))
                surface.blit(alpha_img, (0, 0))
                pygame.display.flip()
                clock.tick(1000 // (duration // 10))
        except Exception as e:
            print(f"Error in fade_in: {e}")

    def run(self):
        """Main loop for IntroChapter2"""
        print("Starting IntroChapter2...")
        
        while self.running and self.count < len(self.script):
            try:
                dt = self.clock.tick(60) / 5000
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.game.running = False
                        return

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.dialog.skip_or_next():
                            self.count += 1
                            
                            if self.count < len(self.script) and self.count < len(self.all_images):
                                new_image = self.all_images[self.count]
                                
                                # Update dialog text
                                self.dialog.set_text(self.script[self.count])
                                
                                # Only fade if image changed
                                if new_image != self.current_image:
                                    self.current_image = new_image
                                    self.fade_in(self.screen, self.current_image)
                                else:
                                    self.current_image = new_image
                            else:
                                # End of scene
                                self.running = False

                # Update and draw
                if self.dialog:
                    self.dialog.update(dt)
                    
                if self.current_image:
                    self.screen.blit(self.current_image, (0, 0))
                    
                if self.dialog:
                    self.dialog.draw(self.screen)
                    
                pygame.display.flip()
                
            except Exception as e:
                print(f"Error in main loop: {e}")
                self.running = False
        
        print("IntroChapter2 completed")

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    game = type('Game', (object,), {'screen': screen, 'clock': clock, 'running': True})()
    
    intro = IntroChapter2(game)
    intro.run()
    
    pygame.quit()
    sys.exit()