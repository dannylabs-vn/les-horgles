import pygame
import sys
import os


from scenes.main_menu_scene import MainMenuScene
from scenes.chapter_scene import ChapterScene
from scenes.intro_scene import IntroScene
from scenes.map_scene import MapScene
from scenes.quiz_scene import QuizScene
from scenes.maze_scene import MazeScene
from scenes.outro_scene import OutroScene
# from scenes.chapter2_complete import Chapter2Complete
from scenes.Intro_chapter2 import IntroChapter2
from scenes.cupboard_game_sequence import TilemapRenderer
from scenes.heartbeat_scene import HeartbeatGame
from scenes.visual_novel_endings import VisualNovelEndings

WIDTH, HEIGHT = 1200, 800

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Les Échos du Passé")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Chapter completion tracking
        self.chapter1_completed = False
        self.chapter2_completed = False
        self.selected_chapter = None

        # Music configuration for different scenes
        self.music_by_scene = {
            "MainMenuScene": "assets/music/menu_music.wav",
            "ChapterScene": "assets/music/menu_music.wav",
            "IntroScene": "assets/music/Pixel 2.wav",
            "MapScene": "assets/music/Pixel 4.wav",
            "QuizScene": "assets/music/Pixel 8.wav",
            "MazeScene": "assets/music/Pixel 7.wav",
            "OutroScene": "assets/music/Pixel 9.wav",
            "Chapter2Complete": "assets/music/Pixel 3.wav",
            "CupboardMinigame": "assets/music/Pixel 5.wav",
            "HeartbeatMinigame": "assets/music/Pixel 6.wav"
        }

    def play_music_for_scene(self, scene_name):
        """Play background music for a scene"""
        path = self.music_by_scene.get(scene_name)
        if path:
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)
                print(f"Playing music: {path}")
            except Exception as e:
                print(f"Error loading music {path}: {e}")

    def run_scene(self, SceneClass):
        """Run a single scene"""
        scene_name = SceneClass.__name__
        print(f"Running scene: {scene_name}")
        self.play_music_for_scene(scene_name)
        scene = SceneClass(self)
        scene.run()

    def run_chapter_1(self):
        # """Run all Chapter 1 scenes"""
        print("Starting Chapter 1...")
        chapter_1_scenes = [
            IntroScene,
            MapScene,
            QuizScene,
            MazeScene,
            OutroScene
        ]
        
        for SceneClass in chapter_1_scenes:
            if not self.running:
                break
            self.run_scene(SceneClass)
        
        # Mark Chapter 1 as completed
        if self.running:
            self.chapter1_completed = True
            print("Chapter 1 completed!")
            # Return to main menu
            self.run_scene(MainMenuScene)

    def run_chapter_2(self):
        """Run Chapter 2 with integrated minigames"""
        print("Starting Chapter 2...")
        
        # Run IntroChapter2 first
        if self.running:
            self.run_scene(IntroChapter2)
            
        # Run the cupboard sequence
        if self.running:
            self.play_music_for_scene("CupboardMinigame")
            tileset_path = os.path.join("assets", "cupboard_tiles.png")
            tilemap_path = os.path.join("assets", "tile_cb.csv")
            cupboard_game = TilemapRenderer(tileset_path, tilemap_path, tile_size=32)
            cupboard_game.run()
        
        # Re-initialize pygame after cupboard game (since it calls pygame.quit())
        if self.running:
            pygame.init()
            pygame.mixer.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Les Échos du Passé")
            
            # Run heartbeat game
            self.play_music_for_scene("HeartbeatMinigame")
            heartbeat_game = HeartbeatGame(1200, 800)
            heartbeat_game.screen = self.screen  # Pass the screen reference
            heartbeat_game.clock = self.clock    # Pass the clock reference
            heartbeat_game.run()

        # Run visual novel endings
        if self.running:
            # Ensure pygame is still initialized
            if not pygame.get_init():
                pygame.init()
                self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Les Échos du Passé")
            
            visual_novel = VisualNovelEndings(self)
            visual_novel.run()

        # Mark Chapter 2 as completed and return to main menu
        if self.running:
            self.chapter2_completed = True
            print("Chapter 2 completed!")
            # Return to main menu
            self.run_scene(MainMenuScene)

    def run_chapter_3(self):
        """Placeholder for Chapter 3"""
        print("Chapter 3 is not implemented yet...")
        
        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        return
            
            # Draw placeholder screen
            self.screen.fill((40, 60, 100))
            
            # Title
            title = font_large.render("Chapter 3", True, (255, 255, 255))
            title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 120))
            self.screen.blit(title, title_rect)
            
            # Subtitle
            subtitle = font_medium.render("Coming Soon!", True, (200, 200, 200))
            subtitle_rect = subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            self.screen.blit(subtitle, subtitle_rect)
            
            # Description
            desc1 = font_small.render("This chapter will continue Léo's journey", True, (150, 150, 150))
            desc1_rect = desc1.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
            self.screen.blit(desc1, desc1_rect)
            
            desc2 = font_small.render("with new challenges and adventures.", True, (150, 150, 150))
            desc2_rect = desc2.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            self.screen.blit(desc2, desc2_rect)
            
            # Instructions
            instruction = font_small.render("Press SPACE or ESC to return to menu", True, (120, 120, 120))
            instruction_rect = instruction.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
            self.screen.blit(instruction, instruction_rect)
            
            pygame.display.flip()
            self.clock.tick(60)

    def show_completion_screen(self):
        """Show completion screen when all chapters are done"""
        print("All available chapters completed!")
        
        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)
        
        # Celebration colors
        celebration_time = 0
        
        while self.running:
            celebration_time += self.clock.tick(60) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        return
            
            # Animated background color
            bg_intensity = int(abs(math.sin(celebration_time * 2) * 50) + 20)
            self.screen.fill((bg_intensity, bg_intensity + 10, bg_intensity + 30))
            
            # Main title with slight animation
            title_y = HEIGHT//2 - 150 + int(math.sin(celebration_time * 3) * 5)
            title = font_large.render("Félicitations!", True, (255, 255, 100))
            title_rect = title.get_rect(center=(WIDTH//2, title_y))
            self.screen.blit(title, title_rect)
            
            # Subtitle
            subtitle = font_medium.render("Vous avez terminé tous les chapitres disponibles!", True, (200, 255, 200))
            subtitle_rect = subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 - 80))
            self.screen.blit(subtitle, subtitle_rect)
            
            # Game title
            game_title = font_medium.render("Les Échos du Passé", True, (255, 255, 255))
            game_title_rect = game_title.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
            self.screen.blit(game_title, game_title_rect)
            
            # Thank you message
            thanks = font_small.render("Merci d'avoir joué à notre jeu!", True, (180, 220, 180))
            thanks_rect = thanks.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
            self.screen.blit(thanks, thanks_rect)
            
            # Credits
            credits1 = font_small.render("Un jeu sur l'empathie, la justice et la solidarité", True, (150, 180, 150))
            credits1_rect = credits1.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))
            self.screen.blit(credits1, credits1_rect)
            
            # Instructions
            instruction = font_small.render("Appuyez sur ESPACE ou ÉCHAP pour revenir au menu", True, (120, 150, 120))
            instruction_rect = instruction.get_rect(center=(WIDTH//2, HEIGHT//2 + 140))
            self.screen.blit(instruction, instruction_rect)
            
            pygame.display.flip()

    def run(self):
        """Main game loop"""
        # Start with main menu
        self.run_scene(MainMenuScene)
        
        # Main game loop
        while self.running:
            # Show chapter selection
            self.run_scene(ChapterScene)
            
            if not self.running:
                break
            
            # Run the selected chapter
            if self.selected_chapter == 1:
                self.run_chapter_1()
            elif self.selected_chapter == 2:
                self.run_chapter_2()
            elif self.selected_chapter == 3:
                self.run_chapter_3()
            
            # Check if player has completed both available chapters
            if self.chapter1_completed and self.chapter2_completed:
                self.show_completion_screen()
            
            # Reset selection for next loop
            self.selected_chapter = None

        # Cleanup
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()

# Add math import for completion screen animation
import math

if __name__ == "__main__":
    try:
        print("Starting Les Échos du Passé...")
        print("=" * 50)
        print("A visual novel about empathy, justice, and solidarity")
        print("=" * 50)
        Game().run()
    except Exception as e:
        print(f"Game crashed with error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)