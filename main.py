import pygame
import random
import os
import time


class Game:

    def set_values(self):
        # Movement variables
        self.PROJECTILE_DELTA = 60
        self.BANANA_VELOCITY = 5
        self.APE_VELOCITY = 5
        self.BULLET_VELOCITY = 10

        # Logistic variables
        self.TIME_COUNT = 0
        self.bananas = []
        self.NUM_OF_HEARTS = 3
        self.HEART_LIST = []
        self.SOUND_ON = True
        self.BULLET_COUNT_NUM = "000"
        self.running = True
        self.START = True
        self.ALT_SCREEN = True
        self.prev_time = 0.0
        self.clock = pygame.time.Clock()
        self.bullets = []
        self.is_audio_playing = False
        self.cur_audio = None
        self.key_pressed = False
        self.CUR_BULLETS = 0
        self.MAX_BULLETS = 2
        self.monk_rectangle = pygame.Rect(0, 300, self.MONKEY_WIDTH, self.MONKEY_HEIGHT)
        self.TIME_COUNT = 0
        self.FPS = 60
        self.GAME_RUNNING = True
        self.PROJECTILE_DELTA_INCREMENT = 0
        self.CYCLES_TILL_INCREMENT = 5
        self.monk_rectangle.x = 0
        self.monk_rectangle.y = 300
        self.MAX_VELOCITY = 40
        self.GAGA_BOOL = False
        self.KEN_BOOL = False

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        # Directories
        self.cur_directory = os.path.dirname(os.path.abspath(__file__))
        self.image_directory = os.path.join(self.cur_directory, "images")
        self.audio_directory = os.path.join(self.cur_directory, "audio")

        # Audio
        self.SPIT = pygame.mixer.Sound(os.path.join(self.audio_directory, "spit.wav"))
        self.FART = pygame.mixer.Sound(os.path.join(self.audio_directory, "fart.mp3"))
        self.MONKEY_SCREAM = pygame.mixer.Sound(os.path.join(self.audio_directory, "458396__befig__monkey-cry.ogg"))
        self.BAD_ROMANCE = pygame.mixer.Sound(os.path.join(self.audio_directory, "Lady Gaga - Bad Romance (Lyrics).mp3"))
        self.IM_KENOUGH = pygame.mixer.Sound(os.path.join(self.audio_directory, "im_just_ken.mp3"))
        self.OUCH = pygame.mixer.Sound(os.path.join(self.audio_directory, "ouch.mp3"))
        self.BATMAN = pygame.mixer.Sound(os.path.join(self.audio_directory, "bman2.mp3"))
        self.SHOOT_SOUND = self.FART
        self.FAIL = pygame.mixer.Sound(os.path.join(self.audio_directory,"wah_wah.mp3"))
        self.PHILLY = pygame.mixer.Sound(os.path.join(self.audio_directory,"philly.mp3"))
        self.PARK = pygame.mixer.Sound(os.path.join(self.audio_directory,"park_sounds.mp3"))
        self.SPINNING_AWAY = pygame.mixer.Sound(os.path.join(self.audio_directory,"spinning_away.mp3"))
        self.P2 = pygame.mixer.Sound(os.path.join(self.audio_directory,"p2.mp3"))
        self.IM = pygame.mixer.Sound(os.path.join(self.audio_directory,"imperfect_murder.mp3"))
        self.ACTION = pygame.mixer.Sound(os.path.join(self.audio_directory, "action.mp3"))
        self.YT = pygame.mixer.Sound(os.path.join(self.audio_directory, "old_youtube_music.mp3"))
        self.BACKGROUND_LIST = [self.P2, self.IM, self.ACTION, self.BATMAN, self.SPINNING_AWAY]
        self.GAME_FONT = pygame.font.SysFont("timesnewroman", 40)
        self.SMALLER_GAME_FONT = pygame.font.SysFont("timesnewroman", 30)
        self.BULLET_FONT = pygame.font.SysFont('timesnewroman', 40)

        # Dimensions
        self.BOX_WIDTH = 200
        self.BOX_HEIGHT = 60
        self.MONKEY_WIDTH = 150
        self.MONKEY_HEIGHT = 150

        # Visual
        self.screen_width = 1200
        self.screen_height = 700
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        pygame.display.set_caption("Banana Bedlam")
        self.HEART = pygame.transform.scale(pygame.image.load(self.image_directory + "/heart.png"), (40, 40))
        self.BANANA_PROJECTILE = pygame.transform.scale(pygame.image.load(self.image_directory + "/banana.png").convert_alpha(), (100, 100))
        self.LE_MONKE = pygame.image.load(self.image_directory + "/le_monke.png")
        self.le_monke_resized = pygame.transform.scale(self.LE_MONKE, (self.MONKEY_WIDTH, self.MONKEY_HEIGHT))
        self.GAGA = pygame.transform.scale(pygame.image.load(self.image_directory + "/lady_gaga.jpeg"), (self.screen_width, self.screen_height))
        self.KEN = pygame.transform.scale(pygame.image.load(self.image_directory + "/ken.jpeg"), (self.screen_width, self.screen_height))
        self.INTRO = pygame.image.load(self.image_directory + "/bb2.png")
        self.OUTRO = pygame.transform.scale(pygame.image.load(self.image_directory + "/le_monke_ending.png"), (self.screen_width, self.screen_height))
        self.GAME_BACKGROUND = pygame.transform.scale(pygame.image.load(self.image_directory + "/game_background.png"), (self.screen_width, self.screen_height))

        self.set_values()
        self.BACKGROUND_MUSIC = None
        

    def draw_setup_window(self):
        center_x = self.screen_width / 4
        center_y = self.screen_height / 4        

        if self.START:
            self.cur_audio = self.BATMAN
            self.cur_audio.play()
            self.screen.blit(self.INTRO, (0, 0))
        else:
            self.screen.blit(self.OUTRO, (0, 0))
            score_text = self.GAME_FONT.render("Final Score: " + str(self.BULLET_COUNT_NUM), True, (0, 0, 0))
            self.screen.blit(score_text, (center_x*2.7, center_y*2.5))
            instructions = self.SMALLER_GAME_FONT.render("Press RETURN to try", True, (0, 0, 0))
            instructions2 = self.SMALLER_GAME_FONT.render("again - ESC to quit.", True, (0, 0, 0))
            
            self.screen.blit(instructions, (center_x*2.7, center_y*3))
            self.screen.blit(instructions2, (center_x*2.75, center_y*3.15))

        pygame.display.update()

    def draw_window(self):        
        while self.NUM_OF_HEARTS != 0:
            self.HEART_LIST.append(self.HEART)
            self.NUM_OF_HEARTS -= 1

        if self.GAGA_BOOL:
            self.screen.blit(self.GAGA, (0, 0))
        elif self.KEN_BOOL:
            self.screen.blit(self.KEN, (0, 0))
        else:
            self.screen.fill((200, 150, 250))
        
        yellow_box_surface = pygame.Surface((self.BOX_WIDTH, self.BOX_HEIGHT))
        yellow_box_surface.fill((255, 255, 0))

        self.screen.blit(self.le_monke_resized, (self.monk_rectangle.x, self.monk_rectangle.y))
        cur_bullet_text = self.BULLET_FONT.render(str(self.BULLET_COUNT_NUM), True, (0, 0, 0))

        for banana_projectile in self.bananas:
            nanner, bx, by = banana_projectile
            if bx <= 0:
                self.bananas.remove(banana_projectile)
                self.HEART_LIST.pop()
                self.OUCH.play()
                if len(self.HEART_LIST) == 0:
                    self.cur_audio.stop()
                    self.cur_audio = self.PARK
                    self.FAIL.play()
                    self.cur_audio.play()
                    self.running = False
                    self.START = False
                    self.ALT_SCREEN = True
                    return 
                    

            else:
                bx -= self.BULLET_VELOCITY
                banana_projectile[1] = bx
                self.screen.blit(nanner, (bx, by))

        for bullet in self.bullets:
            pygame.draw.rect(self.screen, (255, 0, 0), bullet)

        yellow_box_surface.blit(cur_bullet_text, (9, 5))
        heart_x = 70
        for heart in self.HEART_LIST:
            yellow_box_surface.blit(heart, (heart_x, 10))
            heart_x += 45
        self.screen.blit(yellow_box_surface, (10, 10))
        pygame.display.update()

    def move_monkey(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.monk_rectangle.x - self.APE_VELOCITY > -self.APE_VELOCITY:
            if not (self.monk_rectangle.x - self.APE_VELOCITY < 210 and self.monk_rectangle.y < 70):
                self.monk_rectangle.x -= self.APE_VELOCITY

        if keys_pressed[pygame.K_s] and self.monk_rectangle.y + self.APE_VELOCITY + self.monk_rectangle.height < self.screen_height + self.APE_VELOCITY:
            self.monk_rectangle.y += self.APE_VELOCITY
        if keys_pressed[pygame.K_d] and self.monk_rectangle.x + self.APE_VELOCITY + self.monk_rectangle.width < self.screen_width + self.APE_VELOCITY:
            self.monk_rectangle.x += self.APE_VELOCITY
        if keys_pressed[pygame.K_w] and self.monk_rectangle.y - self.APE_VELOCITY > -self.APE_VELOCITY:
            if not (self.monk_rectangle.x - self.APE_VELOCITY < 210 and self.monk_rectangle.y < 70):
                self.monk_rectangle.y -= self.APE_VELOCITY

    def move_projectiles(self):
        for bul in self.bullets:
            if bul.x == self.screen_width:
                self.bullets.remove(bul)
            else:
                bul.x += self.BULLET_VELOCITY
            for banana in self.bananas:
                image, bx, by = banana
                start_x = bx
                end_x = bx + 100
                start_y = by
                end_y = by + 100
                if start_x <= bul.x <= end_x and start_y <= bul.y <= end_y:
                    self.bananas.remove(banana)
                    self.bullets.remove(bul)
                    self.BULLET_COUNT_NUM = int(self.BULLET_COUNT_NUM)
                    self.BULLET_COUNT_NUM += 1
                    self.BULLET_COUNT_NUM = str(self.BULLET_COUNT_NUM)
                    if len(self.BULLET_COUNT_NUM) == 1:
                        self.BULLET_COUNT_NUM = "0" + "0" + self.BULLET_COUNT_NUM
                    if len(self.BULLET_COUNT_NUM) == 2:
                        self.BULLET_COUNT_NUM = "0" + self.BULLET_COUNT_NUM


    def play_song(self):
        song_num = len(self.BACKGROUND_LIST) - 1
        r = random.randint(0,song_num)
        self.BACKGROUND_MUSIC = self.BACKGROUND_LIST[r]
        self.cur_audio = self.BACKGROUND_MUSIC
        self.cur_audio.play()

    def handle_music(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            if not self.GAGA_BOOL:
                self.cur_audio.stop()
                self.cur_audio = self.BAD_ROMANCE
                self.GAGA_BOOL = True
                self.KEN_BOOL = False
            else:
                self.GAGA_BOOL = False
                self.cur_audio.stop()
                self.cur_audio = self.BACKGROUND_MUSIC
            self.cur_audio.play()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
            if not self.KEN_BOOL:
                self.cur_audio.stop()
                self.cur_audio = self.IM_KENOUGH
                self.KEN_BOOL = True
                self.GAGA_BOOL = False
            else:
                self.KEN_BOOL = False
                self.cur_audio.stop()
                self.cur_audio = self.BACKGROUND_MUSIC
            self.cur_audio.play()

    def main(self):

        self.draw_window()
        while self.GAME_RUNNING:
            while self.ALT_SCREEN:
                self.clock.tick(self.FPS)
                if self.START:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                self.ALT_SCREEN = False
                                self.START = False
                                self.cur_audio.stop()
                            if (event.key == pygame.K_ESCAPE) or (event.key == pygame.K_q):
                                pygame.quit()
                            
                    self.draw_setup_window()
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                self.ALT_SCREEN = False
                                self.cur_audio.stop()
                                self.running = True
                                
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                    self.draw_setup_window()

            # This will reset all the relevant variables
            self.set_values()
            self.play_song()
            while self.running == True:
                self.clock.tick(self.FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN and ((event.key == pygame.K_ESCAPE) or (event.key == pygame.K_q)):
                        pygame.quit()

                    # checks if they're pressing space, if so a bullet will be shot
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.CUR_BULLETS != self.MAX_BULLETS:
                        bullet = pygame.Rect(self.monk_rectangle.x + 70, self.monk_rectangle.y + 35, 10, 10)
                        self.SHOOT_SOUND.play()
                        self.CUR_BULLETS += 1
                        self.bullets.append(bullet)
                    
                    self.handle_music(event)

                # checks if time is ready to shoot a banana projectile
                if self.TIME_COUNT == self.PROJECTILE_DELTA:
                    self.TIME_COUNT = 0
                    random_x_axis = random.randint(0, 550)
                    banana_projectile = [self.BANANA_PROJECTILE, self.screen_width + 100, random_x_axis]
                    self.bananas.append(banana_projectile)
                    self.PROJECTILE_DELTA_INCREMENT += 1
                    self.CUR_BULLETS = 0
                    if self.PROJECTILE_DELTA_INCREMENT == self.CYCLES_TILL_INCREMENT:
                        self.PROJECTILE_DELTA_INCREMENT = 0
                        if self.PROJECTILE_DELTA != 0:
                            self.PROJECTILE_DELTA -= 1
                            if self.BANANA_VELOCITY != self.MAX_VELOCITY:
                                self.BANANA_VELOCITY += 1
                                self.APE_VELOCITY += 1
                self.TIME_COUNT += 1
                self.move_projectiles()
                keys_pressed = pygame.key.get_pressed()
                self.move_monkey(keys_pressed)
                self.draw_window()

        pygame.quit()


game = Game()
game.main()
