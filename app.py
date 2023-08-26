import math
import random
import time
import pygame
pygame.init()#intialize pygame

#define width n height of window/display
WIDTH,HEIGHT=800,600
window=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Click Me")#title

target_increment=400 # how long the target wanna grow in milliseconds
target_event=pygame.USEREVENT
target_padding=30 #how far the obj should be on screen.

lives=5#we r setting the lives as 3 and reduce it if misses is greater than lives. 
top_bar_height=50
label_font=pygame.font.SysFont("comicsans",24)#setting font for navbar

bg_color=(0,25,40)

class Target:
    Max_size=30#size of every obj appear on screen .once they hit max size they start to shrink.
    growth_rate=0.2
    color="red"
    color2="white"

    def __init__(self,x,y):#x,y is the position to place targets.
        self.x=x
        self.y=y
        self.size=0 
        self.grow= True #we make it false once max size is reached to shrink its size.
        #size will be increased by growthrate to reach maxsize.once maxsize is reached it start shrinking to reach 0
        # if sze becomes 0 we make the obj disappear from the screen. 

#define method to update target size:
    def update(self):
        #condtn for shrinking if maxsize is reached
        if self.size+self.growth_rate >= self.Max_size:
            self.grow=False
        
        #if target growing
        if self.grow:
            self.size += self.growth_rate
        else:
            self.size -= self.growth_rate #if target shrinking

    # define method to create obj /target
    def draw(self,window):
        #we pass window,color,center position of circle,radius
        #we r going to draw 4 circle to achieve tat ring pattern on our obj
        pygame.draw.circle(window,self.color,(self.x,self.y),self.size)#larger
        pygame.draw.circle(window,self.color2,(self.x,self.y),self.size*0.8)#large
        pygame.draw.circle(window,self.color,(self.x,self.y),self.size*0.6)#medium
        pygame.draw.circle(window,self.color2,(self.x,self.y),self.size*0.4)#small

    #to know if the circle/obj is collidng /overlapping with other target/obj
    def collide(self,x,y):
        distance=math.sqrt((self.x-x)**2+(self.y -y)**2)#distance btwn x and y which gives centr of circle
        #here self.x,self.y is the coordinate of circle whereas x ,y is the coordinate of mouse.
        return distance<=self.size 

#to draw obj on scrn       
def draw(window,targets):
    window.fill(bg_color)#we r setting background color for scrn.
    for target in targets:
        target.draw(window)#the draw functn used here is passed from class.
        #its basically create a obj for every postion in targets list on scrn.
    
def format_time(secs):
    milli_sec=math.floor(int(secs*1000%1000)/100)
    sec=int(round(secs%60,1))
    min=int(secs//60)
    return f"{min:02d}:{sec:02d}:{milli_sec}"
     
def draw_top_bar(window,elapsed_time,target_pressed,misses):
    pygame.draw.rect(window,(252, 157, 3),(0,0,WIDTH,top_bar_height))
    time_label=label_font.render(f"Time:{format_time(elapsed_time)}",1,"white")
    speed=round(target_pressed/elapsed_time,1)#it gves no.of.clicks per sec
    speed_label=label_font.render(f"Speed:{speed} t/s",1,"white")
    hits_label=label_font.render(f"Clicked:{target_pressed}",1,"white")
    lives_label=label_font.render(f"Lives:{lives-misses}",1,"white")

    window.blit(time_label,(5,5))#blit is used to display the text on scrn which take x and y coordinate as args 
    window.blit(speed_label,(200,5))
    window.blit(hits_label,(450,5))
    window.blit(lives_label,(650,5))

def end_game(window,elapsed_time,target_pressed,clicks):
    window.fill(bg_color)

    time_label=label_font.render(f"Time:{format_time(elapsed_time)}",1,"white")
    speed=round(target_pressed/elapsed_time,1)#it gves no.of.clicks per sec
    speed_label=label_font.render(f"Speed:{speed} t/s",1,"white")
    hits_label=label_font.render(f"Clicked:{target_pressed}",1,"white")
    accuracy=round(target_pressed/clicks*100,1)
    accuracy_label=label_font.render(f"Accuracy:{accuracy}%",1,"white")

    window.blit(time_label,(get_middle(time_label),100))#blit is used to display the text on scrn which take x and y coordinate as args 
    window.blit(speed_label,(get_middle(speed_label),200))
    window.blit(hits_label,(get_middle(hits_label),300))
    window.blit(accuracy_label,(get_middle(accuracy_label),400))

    pygame.display.update()

    run=True
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or event.type == pygame.KEYDOWN:#if the event type is  quit we close the window
                quit()
        

def get_middle(surface):#to make end scrn center when the game end
    return WIDTH/2-surface.get_width()/2



def main():#we r going to define evrything insde main functn
    run=True
    targets=[]#to store diff target obj 
    clock=pygame.time.Clock()

    target_pressed=0
    clicks=0
    misses=0 #if no.of.misses we gong to end the game
    start_time=time.time()#start time of game

    #to appear target on scrn
    pygame.time.set_timer(target_event,target_increment)#trigger the event for these milliseconds

    
    while run:
        clock.tick(40)#it slows down the time of obj appear on scrn.
        click=False
        mouse_pos=pygame.mouse.get_pos()#it gives the position of mouse when obj is overlapped/collide
        elapsed_time=time.time()-start_time


        for event in pygame.event.get():#looping through all event in pygame
            #this piece of code is for closing the window when we click on nav "X"
            if event.type==pygame.QUIT:#if the event type is  quit we close the window
                run=False
                break

            #defining a position to draw obj on scrn
            if event.type == target_event:
                x=random.randint(target_padding,WIDTH-target_padding)
                y=random.randint(target_padding,HEIGHT-target_padding)
                target=Target(x,y)#initializing new instance of target class
                targets.append(target)#we append this new instance to tagets list.

            if event.type==pygame.MOUSEBUTTONDOWN:#when we click on target
                click=True
                clicks +=1
                
        for target in targets:#this will increse r decrese the size of obj.
            target.update()
            if target.size<=0:#this remove target from targets list once the size hit 0.
                targets.remove(target)
                misses +=1#which means when size became 0 we failed to click it  so we add it to misses.

            if click and target.collide(*mouse_pos):#mouse_pos return tuple(x,y)we unpack them using * becoz collide functn take x and y as seperate arg.
                targets.remove(target)
                target_pressed+=1

        if misses>=lives:
            end_game(window,elapsed_time,target_pressed,clicks)


        draw(window,targets)#we r clling the fucntn we created to draw obj on scrn.
        draw_top_bar(window,elapsed_time,target_pressed,clicks)
        pygame.display.update()#update functn is called everytym to fill the scrn with obj.

    pygame.quit()#it will trigger this close function.

if __name__=="__main__":
    main()