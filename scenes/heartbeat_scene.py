# -*- coding: utf-8 -*-
"""
Heartbeat Minigame - time-based scoring + ghost guides + cupboard background
Tốc độ theo số lần thua:
- Start: 600 px/s
- Sau thua #1: 500 px/s
- Sau thua #2: 400 px/s
- Thua #3: hiện màn thua, cho restart (về 600)
"""

import os
import pygame
import time
import sys
import math


class HeartbeatGame:
    def __init__(
        self,
        width: int = 1200,
        height: int = 800,
        rounds_to_win: int = 8,
        lives: int = 3,
        target_gap: float = 0.0,     # mục tiêu ghép sát
        time_window: float = 0.15,   # cửa sổ thời gian ±0.15s
        round_timeout: float = 2.0,  # hết giờ 1 vòng
        show_ghost: bool = True,
        ghost_gap: float | None = 12.0,
        bg_path: str = "assets/cupboard_bg.png"  # hình nền tủ
    ):
        # Init pygame
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption("Heartbeat Minigame")
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True

        # Progress
        self.rounds_to_win = rounds_to_win
        self.round = 0

        # Lives & speed
        self.max_lives = lives
        self.lives = lives
        self.loss_count = 0
        self.speed = 600.0

        # Geometry
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        self.lane_offset_x = 420
        self.left_x = self.center_x - self.lane_offset_x
        self.right_x = self.center_x + self.lane_offset_x

        # Scoring
        self.target_gap = max(0.0, target_gap)
        self.time_window = max(0.0, time_window)
        self.round_timeout = round_timeout

        # Ghost guides
        self.show_ghost = show_ghost
        self.ghost_gap = self.target_gap if ghost_gap is None else max(0.0, ghost_gap)
        self.t = 0.0

        # UI / FX
        self.flash_alpha = 0
        self.message = ""
        self.msg_timer = 0.0
        self.round_start_time = time.perf_counter()

        # Fonts
        self.heart_font, self.heart_big_font = self._load_fonts()

        # Background
        self.bg_image = None
        if bg_path and os.path.exists(bg_path):
            try:
                raw = pygame.image.load(bg_path).convert()
                self.bg_image = pygame.transform.scale(raw, (self.screen_width, self.screen_height))
            except Exception as e:
                print("⚠️ Lỗi load background:", e)
                self.bg_image = None

    # ---------- FONT HELPERS ----------
    def _first_existing_path(self, candidates):
        for p in candidates:
            if p and os.path.exists(p):
                return p
        return None

    def _load_fonts(self):
        regular_candidates = [
            "assets/fonts/NotoSans-Regular.ttf",
            "assets/fonts/DejaVuSans.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ]
        bold_candidates = [
            "assets/fonts/NotoSans-Bold.ttf",
            "assets/fonts/DejaVuSans-Bold.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ]

        reg_path = self._first_existing_path(regular_candidates)
        bold_path = self._first_existing_path(bold_candidates)

        try:
            if reg_path:
                heart_font = pygame.font.Font(reg_path, 32)
            else:
                heart_font = pygame.font.Font(None, 32)

            if bold_path:
                heart_big_font = pygame.font.Font(bold_path, 72)
            else:
                heart_big_font = pygame.font.Font(None, 72)
                heart_big_font.set_bold(True)
        except Exception as e:
            print("⚠️ Font load error:", e)
            heart_font = pygame.font.Font(None, 32)
            heart_big_font = pygame.font.Font(None, 72)

        return heart_font, heart_big_font

    # ========= SPEED by LOSSES =========
    def update_speed_by_losses(self):
        if self.loss_count <= 0:
            self.speed = 600.0
        elif self.loss_count == 1:
            self.speed = 500.0
        else:
            self.speed = 400.0

    # ========= DRAWING =========
    def draw_heart(self, surface, x, y, size, color):
        r = size
        pygame.draw.circle(surface, color, (int(x - r * 0.6), int(y - r * 0.2)), int(r * 0.7))
        pygame.draw.circle(surface, color, (int(x + r * 0.6), int(y - r * 0.2)), int(r * 0.7))
        points = [(x - r * 1.3, y - r * 0.1), (x + r * 1.3, y - r * 0.1), (x, y + r * 1.5)]
        pygame.draw.polygon(surface, color, points)

    def draw_half_heart(self, surface, x, y, size, color, side="left"):
        temp = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
        self.draw_heart(temp, size * 2, size * 2, size, color)
        mask = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
        if side == "left":
            keep_rect = pygame.Rect(0, 0, size * 2, size * 4)
        else:
            keep_rect = pygame.Rect(size * 2, 0, size * 2, size * 4)
        pygame.draw.rect(mask, (255, 255, 255, 255), keep_rect)
        temp.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        rect = temp.get_rect(center=(int(x), int(y)))
        surface.blit(temp, rect.topleft)

    def draw_ghost_guides(self):
        alpha = int(105 + 35 * math.sin(self.t * 2.0 * math.pi * 0.8))
        ghost_color = (220, 70, 80, max(60, min(alpha, 160)))
        left_target_x  = self.center_x - self.ghost_gap / 2.0
        right_target_x = self.center_x + self.ghost_gap / 2.0
        self.draw_half_heart(self.screen, left_target_x,  self.center_y, 32, ghost_color, side="left")
        self.draw_half_heart(self.screen, right_target_x, self.center_y, 32, ghost_color, side="right")

    def draw_scene(self):
        # Background tủ
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((15, 15, 18))

        # Overlay mờ để tạo cảm giác trong tủ
        dark_overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 100))
        self.screen.blit(dark_overlay, (0, 0))

        # Ghost guides
        if self.show_ghost:
            self.draw_ghost_guides()

        # Hai nửa tim
        self.draw_half_heart(self.screen, self.left_x,  self.center_y, 32, (220, 70, 80), side="left")
        self.draw_half_heart(self.screen, self.right_x, self.center_y, 32, (220, 70, 80), side="right")

        # HUD
        hud = self.heart_font.render(
            f"Round {self.round}/{self.rounds_to_win}   Lives {self.lives}   Speed {int(self.speed)}",
            True, (240, 240, 240)
        )
        self.screen.blit(hud, (20, 20))

        if self.msg_timer > 0 and self.message:
            txt = self.heart_big_font.render(self.message, True, (255, 220, 100))
            self.screen.blit(txt, txt.get_rect(center=(self.center_x, self.center_y - 220)))

        if self.flash_alpha > 0:
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, int(self.flash_alpha)))
            self.screen.blit(overlay, (0, 0))

    # ========= HELPERS =========
    def gap(self) -> float:
        return abs(self.right_x - self.left_x)

    def lose_life_and_maybe_continue(self, reason_msg: str):
        self.lives -= 1
        self.message = reason_msg
        self.msg_timer = 0.6
        if self.lives <= 0:
            self.show_failure()
            return
        self.loss_count = min(self.loss_count + 1, 2)
        self.update_speed_by_losses()
        self.reset_round_positions_only()

    # ========= ROUND / SCORING =========
    def reset_round_positions_only(self):
        self.left_x = self.center_x - self.lane_offset_x
        self.right_x = self.center_x + self.lane_offset_x
        self.round_start_time = time.perf_counter()

    def full_reset_after_success(self):
        self.round += 1
        if self.round >= self.rounds_to_win:
            self.show_success()
            self.running = False
            return
        self.reset_round_positions_only()

    def hard_reset_game(self):
        self.round = 0
        self.lives = self.max_lives
        self.loss_count = 0
        self.update_speed_by_losses()
        self.message = ""
        self.msg_timer = 0.0
        self.reset_round_positions_only()

    def handle_space(self):
        g = self.gap()
        v_rel = 2.0 * self.speed
        t_to_target = (g - self.target_gap) / v_rel
        if abs(t_to_target) <= self.time_window:
            self.message = "Perfect!"
            self.msg_timer = 0.45
            self.flash_alpha = 120
            self.full_reset_after_success()
        else:
            self.lose_life_and_maybe_continue("Missed!")

    # ========= RESULT SCREENS =========
    def show_success(self):
        self.screen.fill((15, 15, 18))
        label = self.heart_big_font.render("Success! You stayed hidden!", True, (0, 255, 0))
        self.screen.blit(label, label.get_rect(center=(self.center_x, self.center_y)))
        pygame.display.flip()
        pygame.time.wait(1200)

    def show_failure(self):
        self.screen.fill((15, 15, 18))
        label = self.heart_big_font.render("Caught! Try again!", True, (255, 0, 0))
        self.screen.blit(label, label.get_rect(center=(self.center_x, self.center_y)))
        retry_text = self.heart_font.render(
            "Nhấn SPACE để chơi lại hoặc ESC để thoát", True, (255, 255, 255)
        )
        self.screen.blit(retry_text, retry_text.get_rect(center=(self.center_x, self.center_y + 100)))
        pygame.display.flip()
        waiting = True
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        waiting = False
                    elif event.key == pygame.K_SPACE:
                        self.hard_reset_game()
                        waiting = False

    # ========= MAIN LOOP =========
    def run(self):
        self.update_speed_by_losses()
        self.reset_round_positions_only()
        while self.running:
            dt = self.clock.tick(120) / 1000.0
            self.t += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.handle_space()
            if time.perf_counter() - self.round_start_time >= self.round_timeout:
                self.lose_life_and_maybe_continue("Too slow!")
                continue
            if self.left_x >= self.right_x:
                self.lose_life_and_maybe_continue("Missed!")
                continue
            self.left_x += self.speed * dt
            self.right_x -= self.speed * dt
            if self.flash_alpha > 0:
                self.flash_alpha = max(0, self.flash_alpha - 300 * dt)
            if self.msg_timer > 0:
                self.msg_timer = max(0, self.msg_timer - dt)
            self.draw_scene()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    try:
        game = HeartbeatGame(1200, 800)
        game.run()
    except Exception as e:
        print("Unhandled exception:", e)
        pygame.quit()
        sys.exit(1)
