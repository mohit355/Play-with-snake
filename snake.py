import pygame
import random
import os
import sys


pygame.init()               # inilize all the module inside the pygame
pygame.mixer.init()         #  inilze music module of pygame

#Window size
screen_width=700
screen_height=600

#color
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)

'''Creating window for the game '''
window=pygame.display.set_mode((screen_width,screen_height))

'''Title '''
title=pygame.display.set_caption("Play with snake")
pygame.display.update()

'''clock for the movement and velocity ''' 
clock=pygame.time.Clock()

'''creating snake function'''
def plot_snake(window,color,snk_list,snake_size_x,snake_size_y):
    for x,y in snk_list:
        pygame.draw.rect(window,red,[x,y,snake_size_x,snake_size_y])

'''score updating and showing score '''
font=pygame.font.SysFont(None,55)
def text_screen(text,color,x,y):
    screen_text=font.render(text,True,color)
    window.blit(screen_text,[x,y])



'''IMAGE'''

home=pygame.image.load("images//wp.jpg")
home=pygame.transform.scale(home,(screen_width,screen_height))

gameover=pygame.image.load("images//wall.jpeg")
gameover=pygame.transform.scale(gameover,(screen_width,screen_height))

selfs=pygame.image.load("images//self.png")
selfs=pygame.transform.scale(selfs,(screen_width,screen_height))



'''HOME SCREEN FUNCTION  (screen shown before game play)''' 
def home_screen():
    exit_game=False
    while not exit_game:
        window.fill((0,0,0))
        window.blit(home,(0,0))
        text_screen(" Welcome to snake game ",red,100,100)
        text_screen("Press Enter to Play ",red,90,350)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    gameloop()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    




# GAME LOOP
def gameloop():
    
    # game specific variable
    game_over=False
    exit_game=False
    snake_x=45                          # x axis of snake head at starting          
    snake_y=45                          # y axis of snake head at starting
    snake_size_x=10                       # snake head size in x   width
    snake_size_y=10                         # snake head size in y   height
    fps=30                                  #fps- frame per second
    velocity_x=0                            # velocity of snake in x direction
    velocity_y=0                            # velocity of snake in y direction
    initial_v=4                             # initial velocity
    score=0
    snk_list=[]
    snk_length=1             # initially snake length is 1 and list is empty
    food_x=random.randint(40,screen_width-40)     # random coordinates of  food in x axis
    food_y=random.randint(40,screen_height-40)      # random coordinates of  food in y axis
    death_type=-1


    # MAINTAING HIGH SCORE IN A FILE and checking file exits or not
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt","w") as w:
            w.write("0")        
    with open("highscore.txt",'r') as s:
        high_score=s.read()
    
    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as scores:
                scores.write(str(high_score))
            window.fill(black)
            if death_type==0:    
                window.blit(gameover,(0,0))
            if death_type==1:
                window.blit(selfs,(0,0))
            text_screen("Game Over !!!",red,150,150)
            text_screen("Press Enter to restart",red,100,250)
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        #home_screen()
                        gameloop()
        else:
            
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:            # quit the game
                    exit_game=True
                
                # movement on the basis of key
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        #snake_x=snake_x+10
                        velocity_x=initial_v           # velocity set to 4 in x direction
                        velocity_y=0            # y velocity set to 0 because we want o move snake in one direction otherwise it move diagonally
                    if event.key==pygame.K_LEFT:
                        velocity_x=-initial_v
                        velocity_y=0
                        #snake_x=snake_x-10
                    if event.key==pygame.K_UP:
                        #snake_y=snake_y-10
                        velocity_y=-initial_v
                        velocity_x=0
                    if event.key==pygame.K_DOWN:
                        #snake_y=snake_y+10
                        velocity_y=initial_v
                        velocity_x=0                    
            snake_x+=velocity_x
            snake_y+=velocity_y
            
            # changing score and position of food
            if abs(snake_x-food_x)<6 and abs(snake_y - food_y)<6:    # abs absolute value
                score=score+10
                pygame.mixer.music.load("sounds//eat_food.mp3")
                pygame.mixer.music.play()
                food_x=random.randint(40,screen_width-40)     # random coordinates of  food in x axis
                food_y=random.randint(40,screen_height-40)      # random coordinates of  food in y axis 
                snk_length+=4
                if score>int(high_score):
                    high_score=score
            
            
            # change window color to white
            window.fill((0,200,0))
            pygame.draw.line(window,red,(0,0),(screen_width,0))
            
            
            #Creating head
            text_screen("Score :"+str(score)+"  " +"   HighScore : "+str(high_score),red,5,5)
        
            # CALLING PLOT_SNAKE FUNCTION
            plot_snake(window,red,snk_list,snake_size_x,snake_size_y)
            
            # CREATING FOOD FOR SNAKE
            pygame.draw.rect(window,black,[food_x,food_y,snake_size_x,snake_size_y])
        
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
        
            if len(snk_list)>snk_length:
                del snk_list[0]
                
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True
                death_type=0
                pygame.mixer.music.load("sounds//gameover.mp3")
                pygame.mixer.music.play()
                
            if head in snk_list[:-1]:
                game_over=True
                death_type=1
                pygame.mixer.music.load("sounds//gameover.mp3")
                pygame.mixer.music.play()
        
        pygame.display.flip()
        clock.tick(fps)             
    
    pygame.quit()
    sys.exit()


if __name__=="__main__":
    home_screen()