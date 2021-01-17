import pygame
import sys
from pygame.sprite import Sprite
from pygame.sprite import Group
import pygame.font
from random import randint



class Settings():
    def __init__(self):
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(211,240,239)
        self.bg_music_file='Blazer Rail 2.wav'

        #self.block_color=(220,98,48)
        self.block_width=50
        #self.block_height=100
        #self.block_speed=5
        self.block_direction=1

        self.ship_image_file='ship.png'
        self.ship_speed=5
        self.ship_direction=1

        self.bullet_width=10
        self.bullet_height=10
        self.bullet_speed=50
        self.bullet_color=(25,121,169)
        self.bullet_limit=10

        self.button_width=200
        self.button_height=50
        self.button_color=(0,255,0)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)
        
        self.play_button_centerx=self.screen_width/2
        self.play_button_centery=self.screen_height/2

        self.score_button_centerx=self.screen_width/2
        self.score_button_centery=self.screen_height-self.button_height/2

        self.speed_up_scale=1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.block_speed=5
        self.block_height=100
        self.block_color=(220,98,48)
        self.block_rect_right=self.screen_width
        self.block_rect_y=self.screen_height/2
    def increase_speed(self):
        self.block_speed*=self.speed_up_scale
        self.block_height*=0.9
        self.block_color=((randint(0,255),randint(0,255),randint(0,255)))

class Heart():
    def __init__(self,settings,screen):
        self.screen=screen
        self.image=pygame.image.load('heart.png')
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        
    def draw_heart(self):
        self.screen.blit(self.image,self.rect)
        
class GameStats():
    def __init__(self,settings):
        self.game_active=False
        self.game_reset(settings)

    def game_reset(self,settings):
        self.bullet_left=settings.bullet_limit
        self.shot_number=0
        #self.block_color=settings.block_color
        #self.block_width=settings.block_width
        #self.block_height=settings.block_height

class Button():
    def __init__(self,settings,screen,msg,rect_x,rect_y):
        self.screen=screen
        self.screen_rect=screen.get_rect()

        self.width=settings.button_width
        self.height=settings.button_height
        self.bg_color=settings.button_color
        self.text_color=settings.text_color
        self.font=settings.font

        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.centerx=rect_x
        self.rect.centery=rect_y

        self.prep_msg(msg,rect_x,rect_y)

    def prep_msg(self,msg,rect_x,rect_y):
        self.msg_image=self.font.render(msg,True,self.text_color,self.bg_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.centerx=rect_x
        self.msg_image_rect.centery=rect_y

    def draw_button(self):
        self.screen.fill(self.bg_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)



class Block(Sprite):
    def __init__(self,screen,settings):
        super(Block,self).__init__()
        self.screen=screen
        self.screen_rect=self.screen.get_rect()

        self.rect=pygame.Rect(0,0,settings.block_width,settings.block_height)
        self.rect.right=self.screen_rect.right
        self.rect.centery=self.screen_rect.centery
        self.centery=float(self.rect.centery)


    def draw_block(self,settings):
        self.rect=pygame.Rect(self.rect.x,self.rect.y,settings.block_width,settings.block_height)
        
        self.screen.fill(settings.block_color,self.rect)

    def update_block(self,settings,screen):
        #更新矩形块位置,让矩形块上下移动
        if self.rect.bottom>=settings.screen_height or self.rect.top<=0:
             settings.block_direction=-settings.block_direction
        self.centery+=settings.block_speed*settings.block_direction
        self.rect.centery=self.centery



class Ship(Sprite):
    def __init__(self,screen,settings):
        super(Ship,self).__init__()
        self.screen=screen
        self.screen_rect=self.screen.get_rect()

        self.image=pygame.image.load(settings.ship_image_file)
        self.rect=self.image.get_rect()

        self.rect.left=self.screen_rect.left
        self.rect.centery=self.screen_rect.centery

        self.ship_up=False
        self.ship_down=False


    def draw_ship(self):
        self.screen.blit(self.image,self.rect)

    def update_ship(self,settings):
        if self.ship_up==True and self.rect.top>0:
            self.rect.centery-=settings.ship_speed
        elif self.ship_down==True and self.rect.bottom<settings.screen_height:
            self.rect.centery+=settings.ship_speed

        

class Bullet(Sprite):

    def __init__(self,screen,settings,ship):
        super(Bullet,self).__init__()
        self.screen=screen
        self.screen_rect=self.screen.get_rect()
        
        self.rect=pygame.Rect(0,0,settings.bullet_width,settings.bullet_height)
        self.rect.center=ship.rect.center

        
    def draw_bullet(self,screen,settings):
        pygame.draw.rect(self.screen,settings.bullet_color,self.rect)

    def update(self,settings):
        self.rect.centerx+=settings.bullet_speed

        
def update_screen(settings,screen,block,ship,bullets,game_stats,play_button,score_button,hearts):
    #更新屏幕
    screen.fill(settings.bg_color)
    if game_stats.game_active==False:
        play_button.draw_button()
    ship.draw_ship()
    for bullet in bullets:
        bullet.draw_bullet(screen,settings)
    for heart in hearts:
        heart.draw_heart()
    block.draw_block(settings)
    score_button.draw_button()
    pygame.display.flip()

def check_events(screen,settings,ship,bullets,play_button,game_stats,shoot_sound,hearts,block):
    #检查用户操作事件
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            key_down_events(event,screen,settings,ship,bullets,shoot_sound)
        elif event.type==pygame.KEYUP:
            key_up_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
            if button_clicked and game_stats.game_active==False:
                game_stats.game_active=True
                settings.initialize_dynamic_settings()
                block.rect.right=settings.block_rect_right
                block.rect.y=settings.block_rect_y
                game_stats.game_reset(settings)
                create_heart_group(settings,screen,hearts,game_stats)
            
def key_down_events(event,screen,settings,ship,bullets,shoot_sound):
    #响应按键事件
    if event.key==pygame.K_UP:
        ship.ship_up=True
    elif event.key==pygame.K_DOWN:
        ship.ship_down=True
    elif event.key==pygame.K_SPACE:
        bullet=Bullet(screen,settings,ship)
        bullets.add(bullet)
        shoot_sound.play()

def key_up_events(event,ship):
    #响应松键事件
    if event.key==pygame.K_UP:
        ship.ship_up=False
    elif event.key==pygame.K_DOWN:
        ship.ship_down=False

def update_bullet_group(settings,screen,bullets,block,game_stats,fire_sound,hearts):
    hearts.clear()
    bullets.update(settings)
    for bullet in bullets.copy():
        if bullet.rect.left>settings.screen_width:
            bullets.remove(bullet)#飞出屏幕的子弹删除
            game_stats.bullet_left-=1
            

    if pygame.sprite.spritecollideany(block,bullets):
        fire_sound.play()
        settings.increase_speed()
        #game_stats.block_color=((randint(0,255),randint(0,255),randint(0,255)))
        #game_stats.block_width=game_stats.block_width
        #game_stats.block_height=game_stats.block_height*0.8
        game_stats.shot_number+=1
        game_stats.bullet_left+=1#击中后增加一次发射机会

    create_heart_group(settings,screen,hearts,game_stats)

    if game_stats.bullet_left<=0:
        game_stats.game_active=False

def create_heart_group(settings,screen,hearts,game_stats):
    for number in range(game_stats.bullet_left):
        heart=Heart(settings,screen)
        heart.rect.x=heart.rect.width+2*heart.rect.width*number
        hearts.append(heart)

    
    

def run_game():
    #屏幕初始化
    pygame.init()
    pygame.mixer.init()
    settings=Settings()
    screen=pygame.display.set_mode((settings.screen_width,settings.screen_height))
    pygame.display.set_caption('Shooting The Box')

    game_stats=GameStats(settings)

    
    music=pygame.mixer.Sound(settings.bg_music_file)#加载背景音
    shoot_sound=pygame.mixer.Sound('shoot.wav')#加载子弹发射音
    fire_sound=pygame.mixer.Sound('fire.wav')#加载击中音

    #建立一个矩形
    block=Block(screen,settings)

    #建立一个飞船
    ship=Ship(screen,settings)

    #建立子弹群
    bullets=Group()

    #建立play按钮
    play_button=Button(settings,screen,'PLAY',settings.play_button_centerx,settings.play_button_centery)

    #播放背景音乐
    music.play(-1)

    #建立子弹数量群
    hearts=[]
    

    

    while True:
        check_events(screen,settings,ship,bullets,play_button,game_stats,shoot_sound,hearts,block)
        
        score_button=Button(settings,screen,str(game_stats.shot_number),settings.score_button_centerx,settings.score_button_centery)
        if game_stats.game_active!=False:

            block.update_block(settings,screen)
            ship.update_ship(settings)
            update_bullet_group(settings,screen,bullets,block,game_stats,fire_sound,hearts)
        update_screen(settings,screen,block,ship,bullets,game_stats,play_button,score_button,hearts)

run_game()
