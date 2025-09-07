
import pygame
import sys
import os
from scenes.Dialog import DialogBox

class IntroChapter2:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True

        self.count = 0
        self.font = pygame.font.Font('assets/Minecraftia-Regular.ttf', 28)
        self.dialog = DialogBox(1200, 800, self.font)
        self.load_images()
        self.dialog.set_text(self.script[0])
        self.fade_in(self.screen, self.current_image)

    def load_images(self):
        # Load images for Chapter 2 (C2_1 to C2_8)
        C2 = [pygame.image.load(f"assets/C2_{i+1}.{'jpg' if i >= 3 else 'png'}").convert_alpha() for i in range(8)]

        # Scale all images to screen size
        for i in range(len(C2)):
            print(i)
            C2[i] = pygame.transform.scale(C2[i], (1200, 800))

        # Tạo mảng ảnh với mỗi ảnh được lặp lại cho số lần script tương ứng
        self.all_images = []
        
        # Script và mapping ảnh tương ứng
        self.script = []
        
        # Part 1 - C2_1
        self.script.append("Sau một thời gian tham gia chương trình trao đổi học sinh tại Việt Nam, Léo đã trở về quê hương.")
        self.all_images.append(C2[0])

        # Part 2 - C2_2
        part2_scripts = [
            "Léo: Mình thật sự rất hạnh phúc khi được trở về nhà, cuối cùng mình cũng sẽ gặp lại Paul.",
            "Léo: Chào, mình vừa mới về. Anh em à, cậu ổn chứ? Nếu cuối tuần này rảnh thì ra quán cà phê với mình nhé.",
            "Paul: Mình không được ổn lắm… Mình có chuyện muốn nhờ cậu…",
            "Léo (tự hỏi): Chuyện gì đã xảy ra với cậu ấy vậy?"
        ]
        self.script.extend(part2_scripts)
        self.all_images.extend([C2[1]] * len(part2_scripts))

        # Part 3 - C2_3
        self.script.append("Léo: Chào Paul, đã lâu lắm rồi chúng ta không gặp nhau. Mình cứ hy vọng là cậu vẫn ổn.")
        self.all_images.append(C2[2])

        # Part 4 - C2_4
        part4_scripts = [
            "Léo: Chuyện gì đã xảy ra với cậu thế?",
            "Paul: Mình bị ngã, không có gì đâu.",
            "Léo: Thật sao? Những vết bầm này đâu giống như chỉ do ngã."
        ]
        self.script.extend(part4_scripts)
        self.all_images.extend([C2[3]] * len(part4_scripts))

        # Part 5 - C2_5
        part5_scripts = [
            "Paul: Mình… thật ra… Cậu còn nhớ chuyện mình nói là muốn kể với cậu không? Sự thật là mình đang bị một số bạn cùng lớp bắt nạt ở trường.",
            "Léo: Thật tệ quá!",
            "Paul: Giờ thì mình không biết phải làm sao nữa… Làm ơn, hãy giúp mình.",
            "Léo: Được rồi, mình sẽ giúp cậu. Chúng ta hãy đến trường của cậu để xem tình hình thế nào."
        ]
        self.script.extend(part5_scripts)
        self.all_images.extend([C2[4]] * len(part5_scripts))

        # Part 6 - C2_6
        self.script.append("Trong lớp, Paul bị cô lập… thậm chí có cả cục gôm dán trên ghế ngồi.")
        self.all_images.append(C2[5])

        # Part 7 - C2_7
        part7_scripts = [
            "Paul (nghĩ thầm): Mình… đã quen rồi…",
            "Léo (nghĩ thầm): Sao họ có thể đối xử với cậu ấy như vậy?"
        ]
        self.script.extend(part7_scripts)
        self.all_images.extend([C2[6]] * len(part7_scripts))

        # Part 8 - C2_8
        self.script.append("Góc nhìn của Paul: Điều gì đã xảy ra và được viết vào nhật ký của cậu ấy")
        self.all_images.append(C2[7])

        self.script = [
<<<<<<< HEAD
            "Après une période d'échange étudiant au Vietnam, Léo est retourné dans son pays d'origine. ",
            "Il était déterminé à découvrir la vérité sur son passé.",
            "En entrant dans le salon, il a remarqué quelque chose d'étrange...",
            "Il y avait plusieurs photos sur les murs, toutes couvertes de poussière.",
            "Dans un coin, il a trouvé une vieille armoire.",
            "L'armoire semblait contenir quelque chose d'important...",
            "Léo a décidé de l'examiner de plus près.",
            "Soudain, il a entendu des pas derrière lui...",
            "C'était Monsieur Huy, qui le regardait avec un mélange de surprise et de méfiance.",
            "Monsieur Huy : Que fais-tu ici ?",
            "Léo a sorti la photo que Mme My lui avait donnée."
=======
            # Part 1
            "Sau một thời gian tham gia chương trình trao đổi học sinh tại Việt Nam, Léo đã trở về quê hương.",
            # Part 2
            "Léo: Mình thật sự rất hạnh phúc khi được trở về nhà, cuối cùng mình cũng sẽ gặp lại Paul.",
            "Léo: Chào, mình vừa mới về. Anh em à, cậu ổn chứ? Nếu cuối tuần này rảnh thì ra quán cà phê với mình nhé.",
            "Paul: Mình không được ổn lắm… Mình có chuyện muốn nhờ cậu…",
            "Léo (tự hỏi): Chuyện gì đã xảy ra với cậu ấy vậy?",
            # Part 3
            "Léo: Chào Paul, đã lâu lắm rồi chúng ta không gặp nhau. Mình cứ hy vọng là cậu vẫn ổn.",
            # Part 4
            "Léo: Chuyện gì đã xảy ra với cậu thế?",
            "Paul: Mình bị ngã, không có gì đâu.",
            "Léo: Thật sao? Những vết bầm này đâu giống như chỉ do ngã.",
            # Part 5
            "Paul: Mình… thật ra… Cậu còn nhớ chuyện mình nói là muốn kể với cậu không?",
            "Paul: Sự thật là mình đang bị một số bạn cùng lớp bắt nạt ở trường.",
            "Léo: Thật tệ quá!",
            "Paul: Giờ thì mình không biết phải làm sao nữa… Làm ơn, hãy giúp mình.",
            "Léo: Được rồi, mình sẽ giúp cậu. Chúng ta hãy đến trường của cậu để xem tình hình thế nào.",
            # Part 6
            "Trong lớp, Paul bị cô lập… thậm chí có cả cục gôm dán trên ghế ngồi.",
            # Part 7
            "Paul (nghĩ thầm): Mình… đã quen rồi…",
            "Léo (nghĩ thầm): Sao họ có thể đối xử với cậu ấy như vậy?",
            # Part 8
            "Góc nhìn của Paul: Điều gì đã xảy ra và được viết vào nhật ký của cậu ấy"
>>>>>>> cec6aa923cf281ee588112d7aceb72c147e2cb1b
        ]

        self.current_image = self.all_images[0]

    def fade_in(self, surface, image, duration=500):
        clock = pygame.time.Clock()
        alpha_img = image.copy()
        for alpha in range(0, 256, 10):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
            alpha_img.set_alpha(alpha)
            surface.fill((0, 0, 0))
            surface.blit(alpha_img, (0, 0))
            pygame.display.flip()
            clock.tick(1000 // (duration // 10))

    def run(self):
        print("▶ IntroChapter2 đang chạy...")
        while self.running and self.count < len(self.script):
            dt = self.clock.tick(60) / 5000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.dialog.skip_or_next():
                        self.count += 1
                        if self.count < len(self.script) and self.count < len(self.all_images):
                            new_image = self.all_images[self.count]
                            if new_image != self.current_image:
                                self.current_image = new_image
                                self.dialog.set_text(self.script[self.count])
                                self.fade_in(self.screen, self.current_image)
                            else:
                                self.current_image = new_image
                                self.dialog.set_text(self.script[self.count])
                        else:
                            self.running = False

            self.dialog.update(dt)
            self.screen.blit(self.current_image, (0, 0))
            self.dialog.draw(self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    game = type('Game', (object,), {'screen': screen, 'clock': clock, 'running': True})()
    intro = IntroChapter2(game)
    intro.run()
    pygame.quit()
    sys.exit()