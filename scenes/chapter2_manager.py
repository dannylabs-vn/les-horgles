"""
Chapter 2 Scene Manager - Handles the flow of all Chapter 2 scenes
"""
import pygame
import sys
import os
from scenes.Intro_chapter2 import IntroChapter2
from scenes.visual_novel_endings import VisualNovelEndings

class Chapter2Manager:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        
    def run_cupboard_minigame(self):
        """Run the cupboard minigame"""
        try:
            print("Starting Cupboard Minigame...")
            from scenes.cupboard_game_sequence import TilemapRenderer
            tileset_path = os.path.join("assets", "cupboard_tiles.png")
            tilemap_path = os.path.join("assets", "tile_cb.csv")
            
            cupboard_game = TilemapRenderer(tileset_path, tilemap_path, tile_size=32)
            cupboard_game.run()
            print("Cupboard minigame completed")
            return True
        except Exception as e:
            print(f"Error in cupboard game: {e}")
            return False

    def run_heartbeat_minigame(self):
        """Run the heartbeat minigame"""
        try:
            print("💗 Starting Heartbeat Minigame...")
            from scenes.heartbeat_scene import HeartbeatGame
            
            # Create heartbeat game with shared resources
            HB = HeartbeatGame(1200, 800)
            HB.screen = self.screen
            HB.clock = self.clock
            HB.run()
            print("✅ Heartbeat minigame completed")
            return True
        except Exception as e:
            print(f"❌ Error in heartbeat game: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run_visual_novel_endings(self):
        """Run the visual novel endings"""
        try:
            print("📖 Starting Visual Novel Endings...")
            visual_novel = VisualNovelEndings(self.game)
            visual_novel.run()
            print("✅ Visual novel endings completed")
            return True
        except Exception as e:
            print(f"❌ Error in visual novel endings: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run_full_chapter_2(self):
        """Run the complete Chapter 2 sequence"""
        print("🎬 Starting Chapter 2 - Complete Sequence...")
        print("=" * 50)
        
        # Scene 1: Intro Chapter 2
        if self.running:
            print("📝 Scene 1: Introduction")
            try:
                intro = IntroChapter2(self.game)
                intro.run()
                if not self.game.running:
                    self.running = False
                    return False
            except Exception as e:
                print(f"❌ Error in IntroChapter2: {e}")
                return False
        
        # Scene 2: Cupboard Minigame  
        if self.running:
            print("\n📝 Scene 2: Cupboard Minigame")
            if not self.run_cupboard_minigame():
                print("⚠️ Cupboard game failed, but continuing...")
                
        # Scene 3: Heartbeat Minigame
        if self.running:
            print("\n📝 Scene 3: Heartbeat Minigame")
            if not self.run_heartbeat_minigame():
                print("⚠️ Heartbeat game failed, but continuing...")
                
        # Scene 4: Visual Novel Endings
        if self.running:
            print("\n📝 Scene 4: Visual Novel Endings")
            if not self.run_visual_novel_endings():
                print("⚠️ Visual novel failed, but continuing...")
        
        print("\n🎉 Chapter 2 sequence completed!")
        print("=" * 50)
        return True

# Test runner
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Chapter 2 Test")
    clock = pygame.time.Clock()
    
    # Create mock game object
    game = type('Game', (object,), {
        'screen': screen, 
        'clock': clock, 
        'running': True
    })()
    
    # Run Chapter 2
    chapter2 = Chapter2Manager(game)
    chapter2.run_full_chapter_2()
    
    pygame.quit()
    sys.exit()