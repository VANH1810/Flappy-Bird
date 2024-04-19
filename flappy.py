import pygame, sys, random

from pygame.transform import rotate
#Tạo Hàm
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos + 432,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect( midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect( midtop = (500,random_pipe_pos - hard_mode))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes: 
        if pipe.bottom >= 600:   
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False, True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            die_sound.play()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom>= 650:
            die_sound.play()
            return False
    return True
def rotate_bird(birds):
    new_bird = pygame.transform.rotozoom(birds,bird_movement*2,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery)) 
    return new_bird, new_bird_rect
def score_display(game_state):
    if(game_state) == 'main_game':
        score_surface = game_font_score.render(str(int(score)),True, (139,0,139))
        score_rect = score_surface.get_rect(center = (216,50))
        screen.blit(score_surface,score_rect)
    if(game_state) == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True, (139,0,139))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True, (139,0,139))
        high_score_rect = high_score_surface.get_rect(center = (216,610))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
#screen
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()

#Tạo Biến
gravity = 0.25
bird_movement = 0
game_active = True
game_font = pygame.font.Font('font/04B_18.ttf',60)
game_font_score = pygame.font.Font('font/04B_19.ttf',40)
score = 0
high_score = 0
hard_mode = 1000
score_hard = 0
clock_tick_mode = 90
spawnpipe_timer = 1400

#background
bg = pygame.image.load('assets/bg2.png').convert()

#floor
floor = pygame.image.load('assets/floor2.jpg').convert()
floor = pygame.transform.scale2x(floor) 
floor_x_pos = 0

#bird
bird_mid = pygame.image.load('assets/camplayer2.png').convert_alpha()
#bird_mid = pygame.transform.scale2x(bird_mid)
bird_down = pygame.image.load('assets/camplayer2.png').convert_alpha()
#bird_down = pygame.transform.scale2x(bird_down)
bird_up = pygame.image.load('assets/camplayer2.png').convert_alpha()
#bird_up = pygame.transform.scale2x(bird_up)
bird_list = [bird_mid, bird_up, bird_down]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,384))
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)

#Pipe
pipe_surface = pygame.image.load('assets/pipe-fanta.png').convert_alpha()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

#TimerPipe
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,spawnpipe_timer)
pipe_height = [300,310,320,330,340,350,360,370,380,390,400,410,420]
pipe_height_nor = [270,280,290,430,440,450,460,470,480,490,500]
pipe_height_hard = [200,250,510,530,550,600,610,650,700]
#GameOverSurface
game_over_surface = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (216,384))

#Sound
flap_sound = pygame.mixer.Sound('sound/sfx_swooshing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
die_sound = pygame.mixer.Sound('sound/sfx_die.wav')
score_sound_countdown = 100
#Game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                score = 0
                score_hard = 0
                hardmode_mode= 1000
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
            if hard_mode >= 700:
                hard_mode -= 10
            if clock_tick_mode <= 150:
                clock_tick_mode+=1.5
            if hard_mode > 900:
                spawnpipe_timer == 1400
            if hard_mode == 900:
                pipe_height.extend(pipe_height_nor)
                spawnpipe_timer = 1250
            if hard_mode == 800:
                spawnpipe_timer = 1100
            if hard_mode == 700:
                pipe_height.extend(pipe_height_hard)
                spawnpipe_timer = 1050
            
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index +=1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    screen.blit(bg,(0,0))
    if game_active:
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)
        #pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main_game')
        
        score_sound_countdown -= 1
        if score_sound_countdown <= -1:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        hard_mode = 1000
        pipe_height = [300,310,320,330,340,350,360,370,380,390,400,410,420]
        clock_tick_mode = 90
        spawnpipe_timer = 1400
        high_score = update_score(score,high_score)
        score_display('game_over')


    #floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(clock_tick_mode)
