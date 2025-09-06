import pygame

class DialogBox:
    def __init__(self, screen_width, screen_height, font, box_height=150, padding=20, text_speed=110):
        self.rect = pygame.Rect(0, screen_height - box_height, screen_width, box_height)
        self.bg_color = (30, 30, 30, 220)
        self.border_color = (200, 200, 200)

        self.padding = padding
        self.font = font
        self.text_speed = text_speed  # ký tự/giây

        self.full_text = ""       # đoạn text đầy đủ
        self.displayed_text = ""  # đoạn text đang hiển thị (gõ từng ký tự)

        self.timer = 0
        self.finished = True      # đã gõ xong toàn bộ đoạn

        self.blink_timer = 0
        self.show_indicator = True

    def set_text(self, text):
        self.full_text = text
        self.displayed_text = ""
        self.timer = 0
        self.finished = False
        self.blink_timer = 0

    def update(self, dt):
        if not self.finished:
            self.timer += dt
            chars_to_show = int(self.timer * self.text_speed)

            if chars_to_show >= len(self.full_text):
                chars_to_show = len(self.full_text)
                self.finished = True

            self.displayed_text = self.full_text[:chars_to_show]
        else:
            self.blink_timer += dt
            if self.blink_timer >= 0.5:
                self.blink_timer = 0
                self.show_indicator = not self.show_indicator

    def draw(self, surface):
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill(self.bg_color)
        surface.blit(s, (self.rect.x, self.rect.y))

        pygame.draw.rect(surface, self.border_color, self.rect, 10)

        words = self.displayed_text.split(' ')
        lines = []
        line = ""
        max_width = self.rect.width - 2 * self.padding

        for word in words:
            test_line = line + word + " "
            w, _ = self.font.size(test_line)
            if w > max_width:
                lines.append(line)
                line = word + " "
            else:
                line = test_line
        lines.append(line)

        y = self.rect.y + self.padding
        for line in lines:
            text_surface = self.font.render(line.strip(), True, (255, 255, 255))
            surface.blit(text_surface, (self.rect.x + self.padding, y))
            y += self.font.get_height() + 5

        if self.finished and self.show_indicator:
            triangle = [
                (self.rect.right - 30, self.rect.bottom - 25),
                (self.rect.right - 15, self.rect.bottom - 25),
                (self.rect.right - 22, self.rect.bottom - 10)
            ]
            pygame.draw.polygon(surface, (255, 255, 255), triangle)

    def skip_or_next(self):
        if not self.finished:
            self.displayed_text = self.full_text
            self.finished = True
            return False
        return True