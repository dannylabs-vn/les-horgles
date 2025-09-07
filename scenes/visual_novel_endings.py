import pygame
import sys
import os
from scenes.Dialog import DialogBox

class VisualNovelEndings:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        
        self.count = 0
        self.current_ending = None  # Will be set to 'A' or 'C'
        self.font = pygame.font.Font('assets/PressStart2P.ttf', 28)
        self.dialog = DialogBox(1200, 800, self.font)
        
        # Choice tracking
        self.showing_choice = False
        self.choice_made = False
        
        self.load_content()
        
    def load_content(self):
        """Load all images and scripts for both endings"""
        print("Loading content...")
        
        # Load ending A images (6 images)
        ending_a_images = []
        for i in range(6):
            img_loaded = False
            img_path_png = f"assets/Ending_A_{i+1}.png"
            img_path_jpg = f"assets/Ending_A_{i+1}.jpg"
            
            # Try PNG first
            if os.path.exists(img_path_png):
                try:
                    print(f"Found: {img_path_png}")
                    img = pygame.image.load(img_path_png).convert_alpha()
                    img = pygame.transform.scale(img, (1200, 800))
                    ending_a_images.append(img)
                    img_loaded = True
                except Exception as e:
                    print(f"Error loading {img_path_png}: {e}")
            
            # Try JPG if PNG failed
            elif os.path.exists(img_path_jpg):
                try:
                    print(f"Found: {img_path_jpg}")
                    img = pygame.image.load(img_path_jpg).convert_alpha()
                    img = pygame.transform.scale(img, (1200, 800))
                    ending_a_images.append(img)
                    img_loaded = True
                except Exception as e:
                    print(f"Error loading {img_path_jpg}: {e}")
            
            # Create placeholder if no image found
            if not img_loaded:
                print(f"No image found for Ending_A_{i+1}, creating placeholder")
                placeholder = pygame.Surface((1200, 800))
                placeholder.fill((100, 50, 50))  # Dark red for Ending A
                # Add text to placeholder
                try:
                    font = pygame.font.Font(None, 48)
                    text = font.render(f"Ending A - Image {i+1}", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(600, 400))
                    placeholder.blit(text, text_rect)
                except:
                    pass
                ending_a_images.append(placeholder)
        
        # Load ending C images (7 images)
        ending_c_images = []
        for i in range(7):
            img_loaded = False
            img_path_png = f"assets/Ending_C_{i+1}.png"
            img_path_jpg = f"assets/Ending_C_{i+1}.jpg"
            
            # Try PNG first
            if os.path.exists(img_path_png):
                try:
                    print(f"Found: {img_path_png}")
                    img = pygame.image.load(img_path_png).convert_alpha()
                    img = pygame.transform.scale(img, (1200, 800))
                    ending_c_images.append(img)
                    img_loaded = True
                except Exception as e:
                    print(f"Error loading {img_path_png}: {e}")
            
            # Try JPG if PNG failed
            elif os.path.exists(img_path_jpg):
                try:
                    print(f"Found: {img_path_jpg}")
                    img = pygame.image.load(img_path_jpg).convert_alpha()
                    img = pygame.transform.scale(img, (1200, 800))
                    ending_c_images.append(img)
                    img_loaded = True
                except Exception as e:
                    print(f"Error loading {img_path_jpg}: {e}")
            
            # Create placeholder if no image found
            if not img_loaded:
                print(f"No image found for Ending_C_{i+1}, creating placeholder")
                placeholder = pygame.Surface((1200, 800))
                placeholder.fill((50, 100, 50))  # Dark green for Ending C
                # Add text to placeholder
                try:
                    font = pygame.font.Font(None, 48)
                    text = font.render(f"Ending C - Image {i+1}", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(600, 400))
                    placeholder.blit(text, text_rect)
                except:
                    pass
                ending_c_images.append(placeholder)
        
        print(f"Loaded {len(ending_a_images)} images for Ending A")
        print(f"Loaded {len(ending_c_images)} images for Ending C")
        
        # Scripts
        self.choice_script = [
            "Scene 1 - Le passe de Paul (Couloir de l'ancienne ecole, lumiere sombre)",
            "Eleve harceleur 1 : « Tu crois que tu es intelligent, Paul ? »",
            "Eleve harceleur 2 : (rit fort) « Laisse-moi t'aider a \"decorer\" ton dos. »",
            "(Bruit de papier colle sur le dos. Les livres tombent bruyamment.)",
            "Paul (pensee) : « Pourquoi... personne ne vient m'aider ? »",
            "(Paul serre ses livres contre lui, les larmes coulent sur ses joues, puis il s'enfuit.)",
            "---",
            "Scene 2 - Retour au present (Salle de classe eclairee, atmosphere tendue)",
            "(Un BAM retentit.)",
            "Paul : « ... » (tete baissee, regard vide)",
            "Leo : « Paul ?! Qu'est-ce que... qu'est-ce qui se passe ici ? »",
            "(Paul ne repond pas, il reste silencieux.)"
        ]
        
        self.ending_a_script = [
            "Leo : « Arretez tout de suite ! Pourquoi faites-vous ca ?! »",
            "Le harceleur : (ricane) « Oh, le heros qui vole au secours ? Tu veux essayer ? »",
            "(Une main saisit fermement la chemise de Leo, la classe est en emoi.)",
            "Paul : « Tu es fou ?! Ils ne te laisseront jamais tranquille... »",
            "Leo : « Je ne pouvais pas rester la sans rien faire. »",
            "Professeur : « Vous deux, suivez-moi au bureau du proviseur immediatement. »",
            "Paul : (sourit faiblement en regardant par la fenetre sous la pluie) « Merci... Quoi qu'il en soit, je ne suis plus seul. »",
            "Leo (pensee) : « Mais au fond de moi... je sais que tout n'est pas termine. »"
        ]
        
        self.ending_c_script = [
            "Paul : « Si on le publie... ce sera dangereux. »",
            "Leo : « Nous resterons anonymes. Ce n'est pas seulement pour toi... mais aussi pour beaucoup d'autres. »",
            "(Le telephone vibre sans cesse, les notifications de partages et de commentaires envahissent l'ecran.)",
            "Paul : (sourit pour la premiere fois) « Tu ne m'as pas seulement sauve... tu as sauve beaucoup d'autres personnes aussi. »"
        ]
        
        # Store content
        self.content = {
            'choice': {
                'images': ending_a_images[:1] if ending_a_images else [pygame.Surface((1200, 800))],  # Fallback
                'script': self.choice_script
            },
            'A': {
                'images': ending_a_images,
                'script': self.ending_a_script
            },
            'C': {
                'images': ending_c_images,
                'script': self.ending_c_script
            }
        }
        
        # Start with choice sequence
        self.current_content = self.content['choice']
        if self.current_content['images']:
            self.current_image = self.current_content['images'][0]
            print(f"Current image set: {type(self.current_image)}")
        else:
            # Emergency fallback
            self.current_image = pygame.Surface((1200, 800))
            self.current_image.fill((50, 50, 50))
            print("Using emergency fallback image")
        
        if self.current_content['script']:
            self.dialog.set_text(self.current_content['script'][0])
            print(f"First text: {self.current_content['script'][0][:50]}...")
        
        # Apply fade in
        try:
            self.fade_in(self.screen, self.current_image)
        except Exception as e:
            print(f"Fade_in error: {e}")
        
    def fade_in(self, surface, image, duration=500):
        """Fade in effect for image transitions"""
        print(f"Starting fade_in with image {type(image)}")
        if not image:
            print("No image for fade_in!")
            return
            
        clock = pygame.time.Clock()
        alpha_img = image.copy()
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
        print("Fade_in complete")
    
    def draw_choice_menu(self):
        """Draw the choice selection menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((1200, 800))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Choice box
        choice_box = pygame.Surface((800, 400))
        choice_box.fill((40, 40, 60))
        pygame.draw.rect(choice_box, (255, 255, 255), choice_box.get_rect(), 3)
        
        # Title
        try:
            title_font = pygame.font.Font('assets/Minecraftia-Regular.ttf', 32)
        except:
            try:
                title_font = pygame.font.Font('assets/fonts/Minecraftia-Regular.ttf', 32)
            except:
                title_font = pygame.font.Font(None, 32)
        title = title_font.render("Choisissez votre voie :", True, (255, 255, 255))
        choice_box.blit(title, (50, 50))
        
        # Choices
        try:
            choice_font = pygame.font.Font('assets/Minecraftia-Regular.ttf', 24)
        except:
            try:
                choice_font = pygame.font.Font('assets/fonts/Minecraftia-Regular.ttf', 24)
            except:
                choice_font = pygame.font.Font(None, 24)
        
        # Choice A (Bad ending)
        choice_a_rect = pygame.Rect(50, 150, 700, 80)
        pygame.draw.rect(choice_box, (80, 40, 40), choice_a_rect)
        pygame.draw.rect(choice_box, (255, 100, 100), choice_a_rect, 2)
        choice_a_text = choice_font.render("A) Affronter directement", True, (255, 255, 255))
        choice_box.blit(choice_a_text, (60, 175))
        
        # Choice C (Good ending)  
        choice_c_rect = pygame.Rect(50, 270, 700, 80)
        pygame.draw.rect(choice_box, (40, 80, 40), choice_c_rect)
        pygame.draw.rect(choice_box, (100, 255, 100), choice_c_rect, 2)
        choice_c_text = choice_font.render("C) Partager l'histoire", True, (255, 255, 255))
        choice_box.blit(choice_c_text, (60, 295))
        
        # Center the choice box
        self.screen.blit(choice_box, (200, 200))
        
        # Store choice rects for click detection
        self.choice_a_rect = pygame.Rect(250, 350, 700, 80)
        self.choice_c_rect = pygame.Rect(250, 470, 700, 80)
        
    def handle_choice_click(self, pos):
        """Handle mouse clicks on choice menu"""
        if hasattr(self, 'choice_a_rect') and self.choice_a_rect.collidepoint(pos):
            self.current_ending = 'A'
            self.choice_made = True
            print("Choice A selected")
            return True
        elif hasattr(self, 'choice_c_rect') and self.choice_c_rect.collidepoint(pos):
            self.current_ending = 'C'  
            self.choice_made = True
            print("Choice C selected")
            return True
        return False
        
    def start_ending(self):
        """Start the selected ending"""
        print(f"Starting ending {self.current_ending}")
        self.showing_choice = False
        self.count = 0
        self.current_content = self.content[self.current_ending]
        
        if self.current_content['images']:
            self.current_image = self.current_content['images'][0]
            print(f"Set first image for ending: {type(self.current_image)}")
        else:
            print("No images for this ending!")
            return
            
        if self.current_content['script']:
            self.dialog.set_text(self.current_content['script'][0])
            print(f"Set first text: {self.current_content['script'][0][:50]}...")
        
        try:
            self.fade_in(self.screen, self.current_image)
        except Exception as e:
            print(f"Fade_in error in start_ending: {e}")
    
    def run(self):
        """Main loop for the visual novel endings"""
        print("VisualNovelEndings running...")
        
        while self.running:
            dt = self.clock.tick(60) / 5000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"Click at: {event.pos}")
                    if self.showing_choice:
                        # Handle choice selection
                        if self.handle_choice_click(event.pos):
                            self.start_ending()
                    else:
                        # Handle dialogue progression
                        if self.dialog.skip_or_next():
                            self.count += 1
                            print(f"Moving to dialogue {self.count}")
                            
                            # Show choice menu after pre-choice script
                            if (not self.choice_made and 
                                self.count >= len(self.current_content['script'])):
                                print("Showing choice menu")
                                self.showing_choice = True
                            
                            # Advance dialogues/images in ending
                            elif (self.choice_made and 
                                  self.count < len(self.current_content['script'])):
                                
                                self.dialog.set_text(self.current_content['script'][self.count])
                                print(f"New text: {self.current_content['script'][self.count][:50]}...")
                                
                                # Change image if available
                                if self.count < len(self.current_content['images']):
                                    new_image = self.current_content['images'][self.count]
                                    if new_image != self.current_image:
                                        print(f"Switching to image: {self.count + 1}")
                                        self.current_image = new_image
                                        try:
                                            self.fade_in(self.screen, self.current_image)
                                        except Exception as e:
                                            print(f"Fade_in error when switching image: {e}")
                                else:
                                    print(f"No image for index {self.count}")
                            
                            # End of ending
                            elif (self.choice_made and 
                                  self.count >= len(self.current_content['script'])):
                                print("End of ending")
                                self.running = False
            
            # Update and draw
            if not self.showing_choice:
                self.dialog.update(dt)
                if self.current_image:
                    self.screen.blit(self.current_image, (0, 0))
                else:
                    self.screen.fill((0, 0, 0))  # Black background if no image
                    print("No current image to draw!")
                self.dialog.draw(self.screen)
            else:
                if self.current_image:
                    self.screen.blit(self.current_image, (0, 0))
                else:
                    self.screen.fill((0, 0, 0))
                self.draw_choice_menu()
                
            pygame.display.flip()

# Test runner
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    game = type('Game', (object,), {'screen': screen, 'clock': clock, 'running': True})()
    
    visual_novel = VisualNovelEndings(game)
    visual_novel.run()
    
    pygame.quit()
    sys.exit()