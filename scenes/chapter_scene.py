import pygame

class ChapterScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        pygame.font.init()

        self.font = pygame.font.Font("assets/Pixel Emulator.otf", 40)
        self.button_font = pygame.font.Font("assets/Pixel Emulator.otf", 30)

        self.continue_button = pygame.Rect(450, 680, 300, 60)
        self.selected_chapter = None

        # Leo icon
        self.leo_icon = pygame.image.load("assets/leo_face.png").convert_alpha()
        self.leo_icon = pygame.transform.scale(self.leo_icon, (48, 48))

        # Paul icon for chapter 2
        try:
            self.paul_icon = pygame.image.load("assets/paul_face.png").convert_alpha()
            self.paul_icon = pygame.transform.scale(self.paul_icon, (48, 48))
        except:
            # If Paul icon doesn't exist, create a placeholder
            self.paul_icon = pygame.Surface((48, 48))
            self.paul_icon.fill((100, 150, 200))  # Blue placeholder

        # Chapter completion status - in a real game, this would be saved/loaded
        self.chapter_completion = {
            1: getattr(game, 'chapter1_completed', True),  # Chapter 1 starts unlocked
            2: getattr(game, 'chapter2_completed', False)
        }

    def draw_chapters(self):
        chapters = [
            ("CHAPITRE 1 : LA JUSTICE ET L'EMPATHIE", self.chapter_completion[1], 1),
            ("CHAPITRE 2 : LUTTE CONTRE LA VIOLENCE", True, 2),  # Always show chapter 2 as available
            ("CHAPITRE 3 : ÉLIMINER LA DISCRIMINATION", False, 3)
        ]

        title = self.font.render("CHAPITRES", True, (0, 0, 0))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

        for i, (text, available, chapter_num) in enumerate(chapters):
            y = 200 + i * 100
            chapter_rect = pygame.Rect(35, y - 10, self.screen.get_width() - 70, 80)
            
            # Highlight selected chapter
            if self.selected_chapter == chapter_num:
                pygame.draw.rect(self.screen, (220, 235, 255), chapter_rect, border_radius=10)
                pygame.draw.rect(self.screen, (0, 100, 200), chapter_rect, 3, border_radius=10)
            elif chapter_rect.collidepoint(pygame.mouse.get_pos()) and available:
                pygame.draw.rect(self.screen, (240, 245, 255), chapter_rect, border_radius=10)

            color = (0, 0, 0) if available else (120, 120, 120)
            label = self.font.render(text, True, color)
            self.screen.blit(label, (95, y))

            if not available:
                lock = self.font.render("🔒", True, color)
                self.screen.blit(lock, (self.screen.get_width() - 200, y))
            else:
                # Draw appropriate character icon
                if chapter_num == 1:
                    self.screen.blit(self.leo_icon, (35, y))
                elif chapter_num == 2:
                    self.screen.blit(self.paul_icon, (35, y))

            # Store rect for click detection
            setattr(self, f'chapter_{chapter_num}_rect', chapter_rect)

    def draw_continue_button(self):
        if self.selected_chapter:
            button_color = (0, 102, 204)
            text_color = (255, 255, 255)
            button_text = f"JOUER CHAPITRE {self.selected_chapter}"
        else:
            button_color = (150, 150, 150)
            text_color = (200, 200, 200)
            button_text = "SÉLECTIONNER UN CHAPITRE"

        pygame.draw.rect(self.screen, button_color, self.continue_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.continue_button, 3, border_radius=10)
        
        label = self.button_font.render(button_text, True, text_color)
        self.screen.blit(label, (
            self.continue_button.centerx - label.get_width() // 2,
            self.continue_button.centery - label.get_height() // 2
        ))

    def run(self):
        while self.running:
            self.screen.fill((250, 240, 210))

            self.draw_chapters()
            self.draw_continue_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check chapter selection
                    if hasattr(self, 'chapter_1_rect') and self.chapter_1_rect.collidepoint(event.pos):
                        self.selected_chapter = 1
                    elif hasattr(self, 'chapter_2_rect') and self.chapter_2_rect.collidepoint(event.pos):
                        self.selected_chapter = 2
                    elif hasattr(self, 'chapter_3_rect') and self.chapter_3_rect.collidepoint(event.pos) and self.chapter_completion.get(3, False):
                        self.selected_chapter = 3
                    
                    # Check continue button
                    elif self.continue_button.collidepoint(event.pos) and self.selected_chapter:
                        # Set the selected chapter in game object
                        self.game.selected_chapter = self.selected_chapter
                        self.running = False

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    game = type('Game', (object,), {'screen': screen, 'clock': clock, 'running': True, 'chapter1_completed': True, 'chapter2_completed': False})()
    chapter_scene = ChapterScene(game)
    chapter_scene.run()
    pygame.quit()