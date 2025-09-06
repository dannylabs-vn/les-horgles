import pygame
import time
import math
import sys

# -----------------------------
# CẤU HÌNH & MÀU SẮC
# -----------------------------
WIDTH, HEIGHT = 1200, 800
FPS = 120

LIVES_START = 3
ROUNDS_TO_WIN = 8

LANE_OFFSET_X = 420        # vị trí xuất phát trái/phải so với tâm
MOVE_SPEED_START = 700.0   # px/s lúc đầu
MOVE_SPEED_GROWTH = 60.0   # tăng tốc mỗi nhịp
TARGET_GAP = 80.0          # khoảng cách mục tiêu giữa 2 nửa tim khi bấm chuẩn
HIT_WINDOW = 36.0          # biên độ sai số cho phép
ROUND_TIMEOUT = 2.0        # quá thời gian 1 nhịp → tính miss

WHITE = (240, 240, 240)
BLACK = (15, 15, 18)
GREY  = (60, 60, 70)
RED   = (220, 70, 80)
RED_D = (200, 60, 70)
GOLD  = (255, 220, 100)
GREEN = (90, 220, 120)

# -----------------------------
# HÀM VẼ TIM
# -----------------------------
def draw_heart(surface, x, y, size, color):
    """Vẽ trái tim từ 2 hình tròn + đa giác nhọn phía dưới (kiểu cartoon)."""
    r = size
    pygame.draw.circle(surface, color, (int(x - r*0.6), int(y - r*0.2)), int(r*0.7))
    pygame.draw.circle(surface, color, (int(x + r*0.6), int(y - r*0.2)), int(r*0.7))
    points = [
        (x - r*1.3, y - r*0.1),
        (x + r*1.3, y - r*0.1),
        (x,         y + r*1.5),
    ]
    pygame.draw.polygon(surface, color, points)

def draw_half_heart(surface, x, y, size, color, side="left"):
    """Vẽ nửa trái tim bằng cách vẽ tim đầy rồi che 1 nửa."""
    temp = pygame.Surface((size*4, size*4), pygame.SRCALPHA)
    draw_heart(temp, size*2, size*2, size, color)

    mask = pygame.Surface((size*4, size*4), pygame.SRCALPHA)
    if side == "left":
        pygame.draw.rect(mask, (255,255,255,255), (0, 0, size*2, size*4))
    else:
        pygame.draw.rect(mask, (255,255,255,255), (size*2, 0, size*2, size*4))
    temp.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

    rect = temp.get_rect(center=(int(x), int(y)))
    surface.blit(temp, rect.topleft)

# -----------------------------
# GAME
# -----------------------------
class HeartbeatClosetGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Heartbeat – Hiding in the Closet")
        self.clock = pygame.time.Clock()
        try:
            self.font = pygame.font.SysFont("Arial", 32)
            self.big = pygame.font.SysFont("Arial", 72, bold=True)
        except Exception:
            pygame.font.init()
            self.font = pygame.font.SysFont("Arial", 32)
            self.big = pygame.font.SysFont("Arial", 72, bold=True)

        self.running = True

        # Tâm, lane
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2

        # Trạng thái nhịp
        self.lives = LIVES_START
        self.round = 0
        self.speed = MOVE_SPEED_START
        self.left_x = self.center_x - LANE_OFFSET_X
        self.right_x = self.center_x + LANE_OFFSET_X

        # Hiệu ứng
        self.flash_alpha = 0
        self.message = ""
        self.msg_timer = 0.0

    def reset_round(self):
        self.left_x = self.center_x - LANE_OFFSET_X
        self.right_x = self.center_x + LANE_OFFSET_X
        self.message = ""
        self.msg_timer = 0.0

    def start_round(self):
        self.reset_round()
        self.round += 1

    def current_gap(self):
        return self.right_x - self.left_x

    def check_hit(self):
        gap = abs(self.current_gap() - TARGET_GAP)
        return gap <= HIT_WINDOW

    # ------------ VẼ NỀN "TỦ QUẦN ÁO" ------------
    def draw_closet_background(self):
        # Phòng tối
        self.screen.fill(BLACK)

        # Khung tủ ở giữa
        closet_w = int(WIDTH * 0.60)
        closet_h = int(HEIGHT * 0.75)
        closet_rect = pygame.Rect(
            (WIDTH - closet_w) // 2,
            (HEIGHT - closet_h) // 2,
            closet_w, closet_h
        )

        # Lớp tối & viền gỗ đơn giản
        shade = pygame.Surface(closet_rect.size, pygame.SRCALPHA)
        shade.fill((0, 0, 0, 110))
        pygame.draw.rect(shade, (80, 60, 40, 160), shade.get_rect(), width=6, border_radius=12)
        self.screen.blit(shade, closet_rect.topleft)

        # Vignette nhẹ cho cảm giác "núp"
        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(vignette, (0, 0, 0, 80), (0, 0, WIDTH, HEIGHT))
        self.screen.blit(vignette, (0, 0))

    def run(self):
        # Bắt đầu nhịp đầu tiên
        self.start_round()
        round_start_time = time.perf_counter()

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            # --------- INPUT ---------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        if self.check_hit():
                            # Trúng nhịp
                            self.message = "ĐÚNG NHỊP!"
                            self.msg_timer = 0.45
                            self.flash_alpha = 120
                            self.speed += MOVE_SPEED_GROWTH
                            if self.round >= ROUNDS_TO_WIN:
                                self.end_screen("THẮNG!", GREEN)
                                return
                            self.start_round()
                            round_start_time = time.perf_counter()
                        else:
                            # Chệch nhịp
                            self.lives -= 1
                            self.message = "TRƯỢT!"
                            self.msg_timer = 0.6
                            if self.lives <= 0:
                                self.end_screen("THUA", RED)
                                return
                            self.start_round()
                            round_start_time = time.perf_counter()

            # Auto-miss nếu quá thời gian 1 nhịp
            if time.perf_counter() - round_start_time >= ROUND_TIMEOUT:
                self.lives -= 1
                self.message = "CHẬM QUÁ!"
                self.msg_timer = 0.6
                if self.lives <= 0:
                    self.end_screen("THUA", RED)
                    return
                self.start_round()
                round_start_time = time.perf_counter()

            # Auto-miss nếu hai nửa tim đã vượt qua nhau mà chưa bấm
            if self.left_x >= self.right_x:
                self.lives -= 1
                self.message = "LỠ NHỊP!"
                self.msg_timer = 0.6
                if self.lives <= 0:
                    self.end_screen("THUA", RED)
                    return
                self.start_round()
                round_start_time = time.perf_counter()

            # --------- CẬP NHẬT VỊ TRÍ ---------
            self.left_x += self.speed * dt
            self.right_x -= self.speed * dt

            if self.flash_alpha > 0:
                self.flash_alpha = max(0, self.flash_alpha - 300 * dt)
            if self.msg_timer > 0:
                self.msg_timer = max(0, self.msg_timer - dt)

            # --------- VẼ ---------
            self.draw_closet_background()

            # Vùng mục tiêu (2 vạch dọc)
            target_left = self.center_x - TARGET_GAP / 2
            target_right = self.center_x + TARGET_GAP / 2
            guide_h = 220
            pygame.draw.rect(self.screen, GREY, (target_left - 2, self.center_y - guide_h//2, 4, guide_h))
            pygame.draw.rect(self.screen, GREY, (target_right - 2, self.center_y - guide_h//2, 4, guide_h))

            # Tim trung tâm
            draw_heart(self.screen, self.center_x, self.center_y, 26, RED_D)

            # Hai nửa tim lao vào
            draw_half_heart(self.screen, self.left_x,  self.center_y, 32, RED, side="right")
            draw_half_heart(self.screen, self.right_x, self.center_y, 32, RED, side="left")

            # HUD
            hud = self.font.render(
                f"Nhịp {self.round}/{ROUNDS_TO_WIN}   Mạng {self.lives}   Tốc {int(self.speed)}",
                True, WHITE
            )
            self.screen.blit(hud, (20, 20))
            hint = self.font.render("SPACE để chốt nhịp  |  ESC để thoát", True, (180, 190, 200))
            self.screen.blit(hint, (20, 70))

            if self.msg_timer > 0 and self.message:
                txt = self.big.render(self.message, True, GOLD)
                self.screen.blit(txt, txt.get_rect(center=(self.center_x, self.center_y - 220)))

            if self.flash_alpha > 0:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, int(self.flash_alpha)))
                self.screen.blit(overlay, (0, 0))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def end_screen(self, text, color):
        t = 0.0
        while t < 1.2:
            dt = self.clock.tick(FPS) / 1000.0
            t += dt
            self.draw_closet_background()
            label = self.big.render(text, True, color)
            self.screen.blit(label, label.get_rect(center=(self.center_x, self.center_y)))
            pygame.display.flip()
        pygame.quit()
        sys.exit()

# -----------------------------
# CHẠY GAME
# -----------------------------
if __name__ == "__main__":
    HeartbeatClosetGame().run()
