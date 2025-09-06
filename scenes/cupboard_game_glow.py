import pygame
import os
import csv

class TilemapRenderer:
    def __init__(self, tileset_path, tilemap_path, tile_size=32):
        # Khởi tạo pygame và màn hình
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Cupboard Game")
        
        # Initialize player position and movement system
        self.player_grid_x = 3  # Starting X position
        self.player_grid_y = 1  # Starting Y position
        self.current_key = None  # Track which key is being pressed
        self.key_count = 0  # Count consecutive presses of the same key
        self.required_presses = 5  # Number of consecutive presses needed
        self.can_move = False  # Whether player can move
        self.move_direction = None  # Direction to move when ready
        
        # Hiệu ứng sáng cho các ô
        self.glow_alpha = 0  # Độ trong suốt của hiệu ứng sáng
        self.glow_increasing = True  # Hướng thay đổi độ sáng
        self.glow_speed = 5  # Tốc độ thay đổi độ sáng
        self.special_tiles = []  # List các ô có số 0 hoặc 1
        
        # Load assets
        self.tileset_path = tileset_path
        self.tilemap_path = tilemap_path
        self.tile_size = tile_size
        
        try:
            self.tileset = pygame.image.load(tileset_path).convert_alpha()
            print("✅ Tileset loaded successfully")
        except pygame.error as e:
            print(f"❌ Cannot load tileset: {str(e)}")
            raise
        
        # Load player image
        try:
            self.player_img = pygame.image.load(os.path.join("assets", "PAUL.png")).convert_alpha()
            print(f"✅ Player image loaded successfully at position ({self.player_grid_x}, {self.player_grid_y})")
        except pygame.error as e:
            print(f"❌ Cannot load player image: {str(e)}")
            raise
            
        # Load tilemap
        self.tilemap = self.load_tilemap(tilemap_path)
        
        # Initialize map properties
        if self.tilemap:
            self.map_height = len(self.tilemap)
            self.map_width = len(self.tilemap[0]) if self.map_height > 0 else 0
            
            # Find special tiles (0 and 1)
            for y, row in enumerate(self.tilemap):
                for x, value in enumerate(row):
                    if value in [0, 1]:
                        self.special_tiles.append((x, y, value))
            
            # Calculate scaling and offsets
            margin = 50
            original_map_width = self.map_width * self.tile_size
            original_map_height = self.map_height * self.tile_size
            
            width_scale = (self.screen_width - 2 * margin) / original_map_width
            height_scale = (self.screen_height - 2 * margin) / original_map_height
            self.scale_factor = min(width_scale, height_scale)
            
            self.scaled_map_width = int(original_map_width * self.scale_factor)
            self.scaled_map_height = int(original_map_height * self.scale_factor)
            self.scaled_tile_size = int(self.tile_size * self.scale_factor)
            
            self.offset_x = (self.screen_width - self.scaled_map_width) // 2
            self.offset_y = (self.screen_height - self.scaled_map_height) // 2
        else:
            print("❌ No tilemap loaded")
            self.map_width = self.map_height = 0
            self.scale_factor = 1.0
            self.scaled_map_width = self.scaled_map_height = 0
            self.scaled_tile_size = self.tile_size
            self.offset_x = self.offset_y = 0
            
        self.tile_cache = {}

    def load_tilemap(self, filepath):
        """Load tilemap từ file CSV"""
        tilemap = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    # Chuyển đổi chuỗi số thành integers
                    tilemap.append([int(cell) if cell.strip() else -1 for cell in row])
            print(f"✅ Tilemap loaded: {len(tilemap)} rows, {len(tilemap[0]) if tilemap else 0} columns")
        except FileNotFoundError:
            print(f"❌ Tilemap file not found: {filepath}")
            return []
        except Exception as e:
            print(f"❌ Error loading tilemap: {str(e)}")
            return []
        return tilemap

    def update_glow_effect(self):
        """Cập nhật hiệu ứng sáng cho các ô đặc biệt"""
        if self.glow_increasing:
            self.glow_alpha = min(255, self.glow_alpha + self.glow_speed)
            if self.glow_alpha >= 255:
                self.glow_increasing = False
        else:
            self.glow_alpha = max(0, self.glow_alpha - self.glow_speed)
            if self.glow_alpha <= 0:
                self.glow_increasing = True

    def draw_glow_effect(self, x, y, value):
        """Vẽ hiệu ứng sáng cho một ô"""
        glow_surface = pygame.Surface((self.scaled_tile_size, self.scaled_tile_size), pygame.SRCALPHA)
        # Màu khác nhau cho số 0 và 1
        if value == 0:
            glow_color = (255, 255, 150, self.glow_alpha)  # Vàng cho số 0
        else:
            glow_color = (150, 255, 150, self.glow_alpha)  # Xanh lá cho số 1
            
        pygame.draw.rect(glow_surface, glow_color, 
                        (0, 0, self.scaled_tile_size, self.scaled_tile_size))
        self.screen.blit(glow_surface, 
                        (self.offset_x + x * self.scaled_tile_size,
                         self.offset_y + y * self.scaled_tile_size))

    def get_tile(self, tile_id):
        """Get a tile from the tileset"""
        if tile_id == -1 or tile_id < 0:
            return None
            
        if tile_id in self.tile_cache:
            return self.tile_cache[tile_id]
            
        tileset_width = self.tileset.get_width()
        tiles_per_row = tileset_width // self.tile_size
        
        if tiles_per_row == 0:
            return None
            
        tile_x = (tile_id % tiles_per_row) * self.tile_size
        tile_y = (tile_id // tiles_per_row) * self.tile_size
        
        if (tile_x + self.tile_size > tileset_width or 
            tile_y + self.tile_size > self.tileset.get_height()):
            return None
        
        tile_rect = pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size)
        tile_surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        tile_surface.blit(self.tileset, (0, 0), tile_rect)
        
        if self.scaled_tile_size != self.tile_size:
            scaled_tile = pygame.transform.scale(
                tile_surface, 
                (self.scaled_tile_size, self.scaled_tile_size)
            )
        else:
            scaled_tile = tile_surface
            
        self.tile_cache[tile_id] = scaled_tile
        return scaled_tile

    def draw_tilemap(self):
        """Draw the tilemap with glowing effects"""
        if not self.tilemap:
            return
            
        # Draw background
        map_background = pygame.Rect(
            self.offset_x, 
            self.offset_y, 
            self.scaled_map_width, 
            self.scaled_map_height
        )
        pygame.draw.rect(self.screen, (0, 50, 100), map_background)
        
        # Draw tiles
        for row_idx, row in enumerate(self.tilemap):
            for col_idx, tile_id in enumerate(row):
                tile = self.get_tile(tile_id)
                if tile:
                    x = self.offset_x + col_idx * self.scaled_tile_size
                    y = self.offset_y + row_idx * self.scaled_tile_size
                    self.screen.blit(tile, (x, y))
        
        # Cập nhật và vẽ hiệu ứng sáng
        self.update_glow_effect()
        for x, y, value in self.special_tiles:
            self.draw_glow_effect(x, y, value)

    def draw_player(self):
        """Draw the player character"""
        if hasattr(self, 'player_img'):
            # Scale player to fit tile
            scaled_player = pygame.transform.scale(
                self.player_img, 
                (self.scaled_tile_size, self.scaled_tile_size)
            )
            
            # Calculate player position
            player_x = self.offset_x + self.player_grid_x * self.scaled_tile_size
            player_y = self.offset_y + self.player_grid_y * self.scaled_tile_size
            
            # Draw player
            self.screen.blit(scaled_player, (player_x, player_y))

    def draw_key_progress(self):
        """Draw the key press progress bar"""
        font = pygame.font.Font(None, 24)
        bar_height = 20
        bar_width = 200
        
        # Position the bar at the top center of the screen
        bar_x = (self.screen_width - bar_width) // 2
        bar_y = 20
        
        # Define colors
        bg_color = (100, 100, 100)  # Gray
        fill_color = (0, 255, 0)    # Green
        
        # Draw background
        pygame.draw.rect(self.screen, bg_color,
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Draw progress if a key is being pressed
        if self.current_key is not None:
            progress = (self.key_count / self.required_presses) * bar_width
            if progress > 0:
                pygame.draw.rect(self.screen, fill_color,
                               (bar_x, bar_y, progress, bar_height))
        
        # Draw status text
        if self.can_move:
            status = f"Press {self.get_direction_name(self.move_direction)} to move!"
            color = (0, 255, 0)
        elif self.current_key is not None:
            key_name = self.get_direction_name(self.current_key)
            status = f"Pressing {key_name}: {self.key_count}/{self.required_presses}"
            color = (255, 255, 255)
        else:
            status = "Press W/A/S/D 5 times to move"
            color = (255, 255, 255)
        
        status_text = font.render(status, True, color)
        status_rect = status_text.get_rect(center=(self.screen_width // 2, bar_y + 40))
        self.screen.blit(status_text, status_rect)

    def get_direction_name(self, key):
        """Get the name of a direction key"""
        if key == pygame.K_w:
            return "UP"
        elif key == pygame.K_s:
            return "DOWN"
        elif key == pygame.K_a:
            return "LEFT"
        elif key == pygame.K_d:
            return "RIGHT"
        return ""

    def handle_player_movement(self, key):
        """Handle WASD movement"""
        if not self.can_move:
            print("Need to press key 5 times first!")
            return
            
        new_x, new_y = self.player_grid_x, self.player_grid_y
        
        if key == pygame.K_w:
            new_y -= 1
            print(f"Moving UP: {new_x}, {new_y}")
        elif key == pygame.K_s:
            new_y += 1
            print(f"Moving DOWN: {new_x}, {new_y}")
        elif key == pygame.K_a:
            new_x -= 1
            print(f"Moving LEFT: {new_x}, {new_y}")
        elif key == pygame.K_d:
            new_x += 1
            print(f"Moving RIGHT: {new_x}, {new_y}")
            
        # Check if new position is valid and update position
        if (0 <= new_x < self.map_width and 0 <= new_y < self.map_height):
            print(f"Moving from ({self.player_grid_x}, {self.player_grid_y}) to ({new_x}, {new_y})")
            self.player_grid_x = new_x
            self.player_grid_y = new_y
            # Reset movement state
            self.current_key = None
            self.key_count = 0
            self.can_move = False
            self.move_direction = None
        else:
            print(f"Invalid position: ({new_x}, {new_y})")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                        # Increment key count
                        if self.current_key is None:
                            self.current_key = event.key
                            self.key_count = 1
                        elif event.key == self.current_key:
                            self.key_count += 1
                            # Check if enough presses
                            if self.key_count >= self.required_presses:
                                self.can_move = True
                                self.move_direction = event.key
                                print(f"Ready to move {self.get_direction_name(event.key)}!")
                        else:
                            # Different key pressed, reset
                            self.current_key = event.key
                            self.key_count = 1
                            self.can_move = False
                        
            # Draw everything
            self.screen.fill((0, 0, 0))
            self.draw_tilemap()  # This now includes glow effects
            self.draw_player()
            self.draw_key_progress()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    print(f"Current working directory: {os.getcwd()}")
    
    tileset_path = os.path.join("assets", "cupboard_tiles.png")
    tilemap_path = os.path.join("assets", "tile_cb.csv")
    
    print(f"Looking for tileset at: {os.path.abspath(tileset_path)}")
    print(f"Looking for tilemap at: {os.path.abspath(tilemap_path)}")
    
    if not os.path.exists(tileset_path):
        print(f"❌ Tileset file not found: {tileset_path}")
    elif not os.path.exists(tilemap_path):
        print(f"❌ Tilemap file not found: {tilemap_path}")
    else:
        print("✅ Tất cả file đều tồn tại!")
        try:
            renderer = TilemapRenderer(tileset_path, tilemap_path, tile_size=32)
            renderer.run()
        except Exception as e:
            print(f"❌ Lỗi khi chạy game: {str(e)}")
            raise
