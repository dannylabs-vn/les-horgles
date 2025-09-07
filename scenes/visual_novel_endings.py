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
        self.font = pygame.font.Font('assets/Minecraftia-Regular.ttf', 28)
        self.dialog = DialogBox(1200, 800, self.font)
        
        # Choice tracking
        self.showing_choice = False
        self.choice_made = False
        
        self.load_content()
        
    def load_content(self):
        """Load all images and scripts for both endings"""
        # Load ending A images (6 images)
        ending_a_images = []
        for i in range(6):
            try:
                img_path = f"assets/ending_a_{i+1}.png"
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path).convert_alpha()
                else:
                    # Fallback to jpg if png doesn't exist
                    img_path = f"assets/ending_a_{i+1}.jpg"
                    img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (1200, 800))
                ending_a_images.append(img)
            except:
                # Create placeholder if image doesn't exist
                placeholder = pygame.Surface((1200, 800))
                placeholder.fill((100, 50, 50))  # Dark red for Ending A
                ending_a_images.append(placeholder)
        
        # Load ending C images (7 images)
        ending_c_images = []
        for i in range(7):
            try:
                img_path = f"assets/ending_c_{i+1}.png"
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path).convert_alpha()
                else:
                    # Fallback to jpg if png doesn't exist
                    img_path = f"assets/ending_c_{i+1}.jpg"
                    img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (1200, 800))
                ending_c_images.append(img)
            except:
                # Create placeholder if image doesn't exist
                placeholder = pygame.Surface((1200, 800))
                placeholder.fill((50, 100, 50))  # Dark green for Ending C
                ending_c_images.append(placeholder)
        
        # Scripts for different parts
        self.choice_script = [
            "Léo regarde la photo dans sa main, puis vers Monsieur Huy.",
            "Il doit faire un choix crucial qui déterminera son avenir...",
            "Que devrait-il faire maintenant ?"
        ]
        
        # Ending A script (Bad ending - 6 dialogues)
        self.ending_a_script = [
            "Léo : Je vais tout révéler à Paul ! Il mérite de connaître la vérité !",
            "Monsieur Huy soupire profondément, ses épaules s'affaissent.",
            "Monsieur Huy : Tu ne comprends pas les conséquences...",
            "Paul arrive et découvre la vérité brutalement.",
            "La révélation détruit la famille. Paul ne peut pas supporter le choc.",
            "Tout s'effondre autour d'eux... C'était peut-être une erreur."
        ]
        
        # Ending C script (Good ending - 7 dialogues)  
        self.ending_c_script = [
            "Léo : Je pense que nous devrions parler calmement d'abord.",
            "Monsieur Huy : Tu es sage, Léo. Laisse-moi t'expliquer notre histoire.",
            "Ils s'assoient ensemble et commencent une longue conversation.",
            "Monsieur Huy révèle les détails avec précaution et empathie.",
            "Ensemble, ils trouvent un moyen de révéler la vérité à Paul progressivement.",
            "Paul comprend et accepte la situation avec le soutien de sa famille.",
            "La famille reste unie, plus forte grâce à la vérité et à la compréhension mutuelle."
        ]
        
        # Store content
        self.content = {
            'choice': {
                'images': ending_a_images[:1],  # Use first image for choice
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
        self.current_image = self.current_content['images'][0]
        self.dialog.set_text(self.current_content['script'][0])
        self.fade_in(self.screen, self.current_image)
        
    def fade_in(self, surface, image, duration=500):
        """Fade in effect for image transitions"""
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
        title_font = pygame.font.Font('assets/Minecraftia-Regular.ttf', 32)
        title = title_font.render("Choisissez votre voie:", True, (255, 255, 255))
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
        choice_a_text = choice_font.render("A) Révéler immédiatement la vérité à Paul", True, (255, 255, 255))
        choice_box.blit(choice_a_text, (60, 175))
        
        # Choice C (Good ending)  
        choice_c_rect = pygame.Rect(50, 270, 700, 80)
        pygame.draw.rect(choice_box, (40, 80, 40), choice_c_rect)
        pygame.draw.rect(choice_box, (100, 255, 100), choice_c_rect, 2)
        choice_c_text = choice_font.render("C) Parler d'abord calmement avec M. Huy", True, (255, 255, 255))
        choice_box.blit(choice_c_text, (60, 295))
        
        # Center the choice box
        self.screen.blit(choice_box, (200, 200))
        
        # Store choice rects for click detection (adjusted for screen position)
        self.choice_a_rect = pygame.Rect(250, 350, 700, 80)
        self.choice_c_rect = pygame.Rect(250, 470, 700, 80)
        
    def handle_choice_click(self, pos):
        """Handle mouse clicks on choice menu"""
        if hasattr(self, 'choice_a_rect') and self.choice_a_rect.collidepoint(pos):
            self.current_ending = 'A'
            self.choice_made = True
            return True
        elif hasattr(self, 'choice_c_rect') and self.choice_c_rect.collidepoint(pos):
            self.current_ending = 'C'  
            self.choice_made = True
            return True
        return False
        
    def start_ending(self):
        """Start the selected ending"""
        self.showing_choice = False
        self.count = 0
        self.current_content = self.content[self.current_ending]
        self.current_image = self.current_content['images'][0]
        self.dialog.set_text(self.current_content['script'][0])
        self.fade_in(self.screen, self.current_image)
    
    def run(self):
        """Main loop for the visual novel endings"""
        print("▶ VisualNovelEndings đang chạy...")
        
        while self.running:
            dt = self.clock.tick(60) / 5000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.showing_choice:
                        # Handle choice selection
                        if self.handle_choice_click(event.pos):
                            self.start_ending()
                    else:
                        # Handle dialogue progression
                        if self.dialog.skip_or_next():
                            self.count += 1
                            
                            # Check if we should show choice menu
                            if (not self.choice_made and 
                                self.count >= len(self.current_content['script'])):
                                self.showing_choice = True
                            
                            # Check if we should advance to next dialogue/image in ending
                            elif (self.choice_made and 
                                  self.count < len(self.current_content['script'])):
                                
                                # Update dialogue
                                self.dialog.set_text(self.current_content['script'][self.count])
                                
                                # Update image if available and different
                                if self.count < len(self.current_content['images']):
                                    new_image = self.current_content['images'][self.count]
                                    if new_image != self.current_image:
                                        self.current_image = new_image
                                        self.fade_in(self.screen, self.current_image)
                            
                            # End of ending reached
                            elif (self.choice_made and 
                                  self.count >= len(self.current_content['script'])):
                                self.running = False
            
            # Update and draw
            if not self.showing_choice:
                self.dialog.update(dt)
                self.screen.blit(self.current_image, (0, 0))
                self.dialog.draw(self.screen)
            else:
                self.screen.blit(self.current_image, (0, 0))
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