import pygame

class MainMenuScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        pygame.font.init()

        # Fonts
        self.title_font = pygame.font.Font("assets/Pixel Emulator.otf", 50)
        self.button_font = pygame.font.Font("assets/Pixel Emulator.otf", 36)

        # Background & logo
        self.background = pygame.image.load("assets/menu_bg.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen.get_width(), self.screen.get_height())
        )

        self.logo = pygame.image.load("assets/logo.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (500, 500))
        self.logo_rect = self.logo.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # Buttons
        self.play_button_rect = pygame.Rect(100, 300, 300, 60)
        self.help_button_rect = pygame.Rect(100, 380, 300, 60)

        self.fade_duration = 2000
        self.hold_duration = 1000

        # 🎵 Nhạc nền menu
        # pygame.mixer.init()
        # pygame.mixer.music.load("assets/menu_music.wav")  # Đường dẫn đến file nhạc nền
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play(-1)  # Lặp vô hạn trong menu

    def show_intro_logo(self):
        print("✨ Hiển thị logo game (fade-in)...")
        start_time = pygame.time.get_ticks()
        while True:
            now = pygame.time.get_ticks()
            elapsed = now - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                    return

            self.screen.fill((0, 0, 0))

            if elapsed < self.fade_duration:
                alpha = int(255 * (elapsed / self.fade_duration))
            else:
                alpha = 255

            logo_surface = self.logo.copy()
            logo_surface.set_alpha(alpha)
            self.screen.blit(logo_surface, self.logo_rect)

            pygame.display.flip()
            self.clock.tick(60)

            if elapsed > self.fade_duration + self.hold_duration:
                break

    def draw_button(self, rect, text, hovered):
        pygame.draw.rect(self.screen, (70, 130, 180), rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=8)

        label = self.button_font.render(text, True, (255, 255, 255))
        self.screen.blit(label, (rect.x + 40, rect.y + 10))

        if hovered:
            arrow = self.button_font.render("▶", True, (255, 255, 255))
            self.screen.blit(arrow, (rect.x + 10, rect.y + 10))

    def run(self):
        self.show_intro_logo()

        print("▶ MainMenuScene đang chạy...")
        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button_rect.collidepoint(event.pos):
                        print("🟢 Nút PLAY được nhấn") 
                        self.running = False
                    elif self.help_button_rect.collidepoint(event.pos):
                        print("🟡 Nút HELP được nhấn")

            self.screen.blit(self.background, (0, 0))

            # Draw game title
            title = self.title_font.render("Les Échos du Passé", True, (0, 0, 0))
            self.screen.blit(title, (20, 100))

            # Draw buttons
            self.draw_button(self.play_button_rect, "JOUER", self.play_button_rect.collidepoint(mouse_pos))
            self.draw_button(self.help_button_rect, "AIDE", self.help_button_rect.collidepoint(mouse_pos))

            pygame.display.flip()
            self.clock.tick(60)
