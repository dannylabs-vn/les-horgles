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
        
        # Lưu các thuộc tính
        self.tileset_path = tileset_path
        self.tilemap_path = tilemap_path
        self.tile_size = tile_size
        
        # Load tileset
        try:
            self.tileset = pygame.image.load(tileset_path).convert_alpha()
            print("✅ Tileset loaded successfully")
        except pygame.error as e:
            print(f"❌ Cannot load tileset: {str(e)}")
            raise
            
        # Load tilemap
        self.tilemap = self.load_tilemap(tilemap_path)
        
        if self.tilemap:
            self.map_height = len(self.tilemap)
            self.map_width = len(self.tilemap[0]) if self.map_height > 0 else 0
            
            # Tính toán scale và offsets
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

    def get_tile(self, tile_id):
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
        if not self.tilemap:
            return
            
        map_background = pygame.Rect(
            self.offset_x, 
            self.offset_y, 
            self.scaled_map_width, 
            self.scaled_map_height
        )
        pygame.draw.rect(self.screen, (0, 50, 100), map_background)
        
        for row_idx, row in enumerate(self.tilemap):
            for col_idx, tile_id in enumerate(row):
                tile = self.get_tile(tile_id)
                if tile:
                    x = self.offset_x + col_idx * self.scaled_tile_size
                    y = self.offset_y + row_idx * self.scaled_tile_size
                    self.screen.blit(tile, (x, y))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.screen.fill((0, 0, 0))
            self.draw_tilemap()
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
            pygame.init()
            renderer = TilemapRenderer(tileset_path, tilemap_path, tile_size=32)
            renderer.run()
        except Exception as e:
            print(f"❌ Lỗi khi chạy game: {str(e)}")
            raise
