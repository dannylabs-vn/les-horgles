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
        self.required_presses = 3
        
        # Timer setup
        self.game_duration = 12  # 12 seconds
        self.time_left = self.game_duration
        self.start_time = pygame.time.get_ticks()
        self.timer_width = 20
        self.timer_height = 200
        self.timer_x = self.screen_width - 40
        self.timer_y = (self.screen_height - self.timer_height) // 2
        
        self.reset_game()
        
        # Timer setup
        self.game_duration = 12  # 12 seconds
        self.time_left = self.game_duration
        self.start_time = pygame.time.get_ticks()
        self.timer_width = 20
        self.timer_height = 400
        self.timer_x = 50
        self.timer_y = (self.screen_height - self.timer_height) // 2
        
        # Hiệu ứng sáng tuần tự
        self.current_glow_index = 0  # Index của ô đang sáng
        self.glow_timer = 0  # Đếm thời gian sáng
        self.glow_duration = 30  # Thời gian mỗi ô sáng (frames)
        self.glow_alpha = 0  # Độ trong suốt
        self.glow_state = 'fade_in'  # Trạng thái hiệu ứng: 'fade_in', 'stay', 'fade_out'
        self.glow_speed = 15  # Tốc độ fade
        
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
            print(f"✅ Player image loaded successfully")
        except pygame.error as e:
            print(f"❌ Cannot load player image: {str(e)}")
            raise
            
        # Load tilemap
        self.tilemap = self.load_tilemap(tilemap_path)
        
        # Initialize map properties
        if self.tilemap:
            self.map_height = len(self.tilemap)
            self.map_width = len(self.tilemap[0]) if self.map_height > 0 else 0
            
            # Tìm tất cả các ô số 0 và 1, sắp xếp theo số
            self.special_tiles = []
            # Tìm các ô số 0 trước
            for y, row in enumerate(self.tilemap):
                for x, value in enumerate(row):
                    if value == 0:
                        self.special_tiles.append((x, y, value))
            # Sau đó tìm các ô số 1
            for y, row in enumerate(self.tilemap):
                for x, value in enumerate(row):
                    if value == 1:
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
        """Cập nhật hiệu ứng sáng tuần tự"""
        if not self.special_tiles:
            return
            
        # Cập nhật độ trong suốt dựa trên trạng thái
        if self.glow_state == 'fade_in':
            self.glow_alpha = min(255, self.glow_alpha + self.glow_speed)
            if self.glow_alpha >= 255:
                self.glow_state = 'stay'
                self.glow_timer = self.glow_duration
        
        elif self.glow_state == 'stay':
            self.glow_timer -= 1
            if self.glow_timer <= 0:
                self.glow_state = 'fade_out'
        
        elif self.glow_state == 'fade_out':
            self.glow_alpha = max(0, self.glow_alpha - self.glow_speed)
            if self.glow_alpha <= 0:
                # Chuyển sang ô tiếp theo
                self.current_glow_index = (self.current_glow_index + 1) % len(self.special_tiles)
                self.glow_state = 'fade_in'

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

    def draw_timer(self):
        """Vẽ thanh thời gian"""
        # Vẽ khung timer
        timer_border = pygame.Rect(self.timer_x - 2, self.timer_y - 2, 
                                 self.timer_width + 4, self.timer_height + 4)
        pygame.draw.rect(self.screen, (255, 255, 255), timer_border)
        
        # Tính toán chiều cao của thanh thời gian
        time_ratio = self.time_left / self.game_duration
        current_height = self.timer_height * time_ratio
        
        # Chọn màu dựa trên thời gian còn lại
        if time_ratio > 0.6:
            color = (0, 255, 0)  # Xanh lá
        elif time_ratio > 0.3:
            color = (255, 255, 0)  # Vàng
        else:
            color = (255, 0, 0)  # Đỏ
        
        # Vẽ thanh thời gian
        timer_rect = pygame.Rect(self.timer_x, 
                               self.timer_y + self.timer_height - current_height,
                               self.timer_width, current_height)
        pygame.draw.rect(self.screen, color, timer_rect)
        
        # Hiển thị số giây còn lại
        font = pygame.font.Font(None, 24)
        text = font.render(f"{int(self.time_left)}s", True, (255, 255, 255))
        text_rect = text.get_rect(midtop=(self.timer_x + self.timer_width/2, 
                                        self.timer_y + self.timer_height + 10))
        self.screen.blit(text, text_rect)

    def draw_tilemap(self):
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
        
        # Cập nhật và vẽ hiệu ứng sáng chỉ cho ô hiện tại
        self.update_glow_effect()
        if self.special_tiles:
            x, y, value = self.special_tiles[self.current_glow_index]
            self.draw_glow_effect(x, y, value)

    def draw_player(self):
        """Draw the player character"""
        if hasattr(self, 'player_img'):
            scaled_player = pygame.transform.scale(
                self.player_img, 
                (self.scaled_tile_size, self.scaled_tile_size)
            )
            
            player_x = self.offset_x + self.player_grid_x * self.scaled_tile_size
            player_y = self.offset_y + self.player_grid_y * self.scaled_tile_size
            
            self.screen.blit(scaled_player, (player_x, player_y))

    def draw_key_progress(self, last_key, key_press_count):
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
        
        # Draw progress
        if last_key is not None:
            progress = (key_press_count / self.required_presses) * bar_width
            if progress > 0:
                pygame.draw.rect(self.screen, fill_color,
                               (bar_x, bar_y, progress, bar_height))
        
        # Draw status text
        if self.can_move:
            status = f"Moving {self.get_direction_name(last_key)}!"
            color = (0, 255, 0)
        elif last_key is not None:
            key_name = self.get_direction_name(last_key)
            status = f"Pressing {key_name}: {key_press_count}/{self.required_presses}"
            color = (255, 255, 255)
        else:
            status = "Press same key 5 times to move"
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

    def is_special_tile_glowing(self, x, y):
        """Kiểm tra xem ô đặc biệt có đang sáng không"""
        if not self.special_tiles:
            return False
            
        current_tile = self.special_tiles[self.current_glow_index]
        return (x, y) == (current_tile[0], current_tile[1]) and self.glow_alpha > 0

    def get_tile_value(self, x, y):
        """Lấy giá trị của ô tại vị trí x, y"""
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            return self.tilemap[y][x]
        return -1

    game_is_over = False

    def handle_player_movement(self, key):
        """Handle WASD movement"""
        if not self.can_move:
            print("Need to press key 5 times first!")
            return
            
        new_x, new_y = self.player_grid_x, self.player_grid_y
        
        if key == pygame.K_w:
            # Ngăn không cho di chuyển lên hàng 1
            if self.player_grid_y <= 1:
                print("Cannot move up to row 1!")
                return
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
            
        # Kiểm tra vị trí mới có hợp lệ không
        if not (0 <= new_x < self.map_width and 0 <= new_y < self.map_height):
            print(f"Invalid position: ({new_x}, {new_y})")
            return
            
        # Lấy giá trị ô mới
        tile_value = self.get_tile_value(new_x, new_y)
        
        # Kiểm tra điều kiện di chuyển
        if tile_value in [0, 1]:
            # Nếu là ô đặc biệt, chỉ cho phép di chuyển khi đang sáng
            if not self.is_special_tile_glowing(new_x, new_y):
                print("Cannot move to special tile when it's not glowing!")
                return
            else:
                # Hiển thị màn hình WIN
                self.show_win_screen()
                self.game_is_over = True
                pygame.quit()  # Tự động thoát khi thắng
                return
                
        # Di chuyển bình thường
        print(f"Moving from ({self.player_grid_x}, {self.player_grid_y}) to ({new_x}, {new_y})")
        self.player_grid_x = new_x
        self.player_grid_y = new_y
        # Reset movement state
        self.current_key = None
        self.key_count = 0
        self.can_move = False
        self.move_direction = None

    def reset_game(self):
        """Reset game state"""
        self.player_grid_x = 3
        self.player_grid_y = 1
        self.current_key = None
        self.key_count = 0
        self.can_move = False
        self.move_direction = None
        self.time_left = self.game_duration
        self.start_time = pygame.time.get_ticks()

    def show_game_over_screen(self):
        """Hiển thị màn hình Game Over"""
        background = self.screen.copy()
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 74)
        text = font.render("Time's Up!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width/2, self.screen_height/2))
        self.screen.blit(text, text_rect)
        
        font_small = pygame.font.Font(None, 36)
        instruction = font_small.render("Press SPACE to try again or ESC to exit", True, (255, 255, 255))
        inst_rect = instruction.get_rect(center=(self.screen_width/2, self.screen_height/2 + 50))
        self.screen.blit(instruction, inst_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return False
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.screen.blit(background, (0, 0))
                        pygame.display.flip()
                        return True
        return True

    def draw_timer(self):
        """Vẽ thanh thời gian"""
        # Vẽ khung timer
        timer_border = pygame.Rect(self.timer_x - 2, self.timer_y - 2, 
                                 self.timer_width + 4, self.timer_height + 4)
        pygame.draw.rect(self.screen, (255, 255, 255), timer_border)
        
        # Tính toán chiều cao của thanh thời gian
        time_ratio = self.time_left / self.game_duration
        current_height = self.timer_height * time_ratio
        
        # Chọn màu dựa trên thời gian còn lại
        if time_ratio > 0.6:
            color = (0, 255, 0)  # Xanh lá
        elif time_ratio > 0.3:
            color = (255, 255, 0)  # Vàng
        else:
            color = (255, 0, 0)  # Đỏ
        
        # Vẽ thanh thời gian
        timer_rect = pygame.Rect(self.timer_x, 
                               self.timer_y + self.timer_height - current_height,
                               self.timer_width, current_height)
        pygame.draw.rect(self.screen, color, timer_rect)
        
        # Hiển thị số giây còn lại
        font = pygame.font.Font(None, 24)
        text = font.render(f"{int(self.time_left)}s", True, (255, 255, 255))
        text_rect = text.get_rect(midtop=(self.timer_x + self.timer_width/2, 
                                        self.timer_y + self.timer_height + 10))
        self.screen.blit(text, text_rect)

    def show_win_screen(self):
        """Hiển thị màn hình WIN"""
        # Lưu màn hình hiện tại
        background = self.screen.copy()
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)  # 50% transparent
        
        # Vẽ overlay
        self.screen.blit(overlay, (0, 0))
        
        # Vẽ text WIN
        font = pygame.font.Font(None, 74)
        text = font.render("YOU WIN!", True, (255, 255, 0))
        text_rect = text.get_rect(center=(self.screen_width/2, self.screen_height/2))
        self.screen.blit(text, text_rect)
        
        # Vẽ hướng dẫn
        font_small = pygame.font.Font(None, 36)
        instruction = font_small.render("Press SPACE to continue or ESC to exit", True, (255, 255, 255))
        inst_rect = instruction.get_rect(center=(self.screen_width/2, self.screen_height/2 + 50))
        self.screen.blit(instruction, inst_rect)
        
        pygame.display.flip()
        
        # Chờ người chơi nhấn phím
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    if event.key == pygame.K_SPACE:
                        # Khôi phục màn hình và tiếp tục game
                        self.screen.blit(background, (0, 0))
                        pygame.display.flip()
                        waiting = False
                        # Reset vị trí player
                        self.player_grid_x = 3
                        self.player_grid_y = 1
                        return

    def run(self):
        clock = pygame.time.Clock()
        running = True
        last_key = None
        key_press_count = 0
        
        while running:
            # Cập nhật thời gian
            current_time = pygame.time.get_ticks()
            self.time_left = max(0, self.game_duration - (current_time - self.start_time) / 1000)
            
            # Kiểm tra hết thời gian
            if self.time_left <= 0:
                if self.show_game_over_screen():
                    self.time_left = self.game_duration
                    self.start_time = pygame.time.get_ticks()
                else:
                    running = False
                continue

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                        # Kiểm tra nếu là phím mới
                        if last_key != event.key:
                            last_key = event.key
                            key_press_count = 1
                            self.can_move = False
                        else:
                            key_press_count += 1
                            if key_press_count >= self.required_presses:
                                self.can_move = True
                                print(f"Ready to move {self.get_direction_name(event.key)}!")
                                self.handle_player_movement(event.key)
                                # Reset sau khi di chuyển
                                last_key = None
                                key_press_count = 0
                                self.can_move = False
                        
            # Draw everything
            if (not self.game_is_over):
                self.screen.fill((0, 0, 0))
                self.draw_tilemap()  # This now includes sequential glow effects
                self.draw_player()
                self.draw_key_progress(last_key, key_press_count)
                self.draw_timer()  # Draw the timer bar
                
                pygame.display.flip()
                clock.tick(60)
            else:
                running = False
        
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
