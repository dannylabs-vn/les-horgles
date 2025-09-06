import pygame
from Intro_chapter2 import IntroChapter2
from cupboard_game_sequence import TilemapRenderer
from heartbeat_scene import HeartbeatClosetGame

class Chapter2Scene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        self.current_scene_index = 0
        self.scenes = []
        self.initialize_scenes()

    def initialize_scenes(self):
        # Create instances of all scenes
        self.scenes = [
            IntroChapter2(self.game),
            TilemapRenderer(self.game),
            HeartbeatClosetGame(self.game)
        ]

    def run(self):
        print("▶ Chapter 2 đang chạy...")
        
        while self.running and self.current_scene_index < len(self.scenes):
            # Get the current scene
            current_scene = self.scenes[self.current_scene_index]
            
            # Run the current scene
            current_scene.run()
            
            # If the game is not running, break the loop
            if not self.game.running:
                self.running = False
                break
                
            # Move to the next scene
            self.current_scene_index += 1
            
            # If all scenes are complete, end the chapter
            if self.current_scene_index >= len(self.scenes):
                self.running = False

        print("✓ Chapter 2 hoàn thành")

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    game = type('Game', (object,), {'screen': screen, 'clock': clock, 'running': True})()
    chapter2 = Chapter2Scene(game)
    chapter2.run()
    pygame.quit()