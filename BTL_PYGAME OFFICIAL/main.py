from random import choice, randint
import pygame
from sys import exit

class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1=pygame.image.load('graphic\Player\player_walk_1.png').convert_alpha()
        player_walk_2=pygame.image.load('graphic\Player\player_walk_2.png').convert_alpha()
        self.player_jump=pygame.image.load('graphic\Player\jump.png').convert_alpha()
        self.player_walk=[player_walk_1,player_walk_2]
        
        self.player_index=0
        self.image=self.player_walk[self.player_index]
        self.rect=self.image.get_rect(midbottom =(90,300))
        self.gravity=0
        self.jump_sound=pygame.mixer.Sound('audio/jump.mp3')
    def player_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom==300:
            self.jump_sound.play()
            self.gravity=-20
            
    def apply_gravity(self):
        self.gravity+=1
        self.rect.y+=self.gravity
        if self.rect.bottom>300: self.rect.bottom=300
    def animation_state(self):
        if self.rect.bottom <300:
            self.image=self.player_jump
        else:
            self.player_index+=0.1
            self.image=self.player_walk[int(self.player_index)%2]
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
            
class obstancle(pygame.sprite.Sprite):
    def __init__(self,type) :
        super().__init__()
        if type=='fly':
            fly1=pygame.image.load('graphic/Fly/Fly1.png').convert_alpha()
            fly2=pygame.image.load('graphic/Fly/Fly2.png').convert_alpha()
            self.frame=[fly1,fly2]
            
            
            self.y_pos=210
            self.speed=6
        if type=='snail':
            snail1=pygame.image.load('graphic\Snail\snail1.png').convert_alpha()
            snail2=pygame.image.load('graphic\Snail\snail2.png').convert_alpha()
            self.frame=[snail1,snail2]
            
            
            self.y_pos=300
            self.speed=5
        self.animation_index=0
            
        self.image=self.frame[self.animation_index]
        self.rect=self.image.get_rect(bottomleft=(randint(900,1100),self.y_pos))
    def animation_state(self):
        self.animation_index+=0.1
        self.image=self.frame[int(self.animation_index)%2]
    def update(self) :
        self.animation_state()
        self.rect.x-=self.speed


def display_score():
    current_time=round(pygame.time.get_ticks()/1000)-start_time
    score_surf=test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect=score_surf.get_rect(center=(400,80))
    screen.blit(score_surf,score_rect)
    return current_time
    

def  collision():
    if pygame.sprite.spritecollide(player.sprite,obstancle_group,False):
        return False
    else:
        return True



pygame.init()
screen=pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock=pygame.time.Clock()
test_font=pygame.font.Font('font\Pixeltype.ttf',50) 
game_active= False
start_time=0
score=0
game_sound=pygame.mixer.Sound('audio/music.wav')
game_sound.play()
obstacle_timer=pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1500)
snail_animation=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation,500)
fly_animation=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation,50)


#back ground
sky_surface=pygame.image.load('graphic\Sky.png').convert()
ground_surface=pygame.image.load('graphic\ground.png').convert()#convert sang 1 thứ gì đó giúp pygame chạy nhanh hơn 




#group
player=pygame.sprite.GroupSingle()
player.add(Player()) 

obstancle_group=pygame.sprite.Group()

#intro 
player_stand=pygame.image.load('graphic/Player/player_stand.png').convert_alpha()
player_stand=pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect=player_stand.get_rect(center=(400,200))
game_name=test_font.render('Runner game',False,(111,196,169))
game_name_rect=game_name.get_rect(center=(400,50))
game_mes=test_font.render('Press space to run',False,(111,196,169))
game_mes_rect=game_mes.get_rect(center=(400,350))

#game over
game_over=test_font.render('You loss',False,(111,196,169))
game_over_rect=game_over.get_rect(center=(400,50))


#timer

while True:#có thể hiểu mỗi vòng lặp là 1 khung hình 
    
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            
            
            exit()
        if game_active:    
            
            if event.type== obstacle_timer:
                obstancle_group.add(obstancle(choice(['fly','snail'])))
                
            
        
        else:
            if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_SPACE:
                        game_active=True
                        player_gravity=0
                        obstancle_group.empty()
                        start_time=round(pygame.time.get_ticks()/1000) 
                             
        
    if game_active:
        #draw all element
        #update everything
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score=display_score()
        player.draw(screen)
        player.update()
        
        
        obstancle_group.draw(screen)
        obstancle_group.update()
        game_active=collision()
        
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        
        score_mes=test_font.render(f'Your score: {score}',False,(111,196,169))
        score_mes_rect=score_mes.get_rect(center=(400,350))
        if score==0:
            screen.blit(game_name,game_name_rect)
            screen.blit(game_mes,game_mes_rect)
        else:
            screen.blit(game_over,game_over_rect)
            screen.blit(score_mes,score_mes_rect)
       
        
    pygame.display.update() 
    clock.tick(60)
    
    