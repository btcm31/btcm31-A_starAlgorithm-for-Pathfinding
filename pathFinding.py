import pygame
from random import randrange
from spot import Spot
import os
from astar_algorithm import A_starAlgorithm
#os.environ['SDL_VIDEODRIVER']='windib'
#os.putenv('SDL_VIDEODRIVER', 'fbcon')
#os.environ["SDL_VIDEODRIVER"] = "dummy"

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BEIGE = (250,250,250)


''' create surface to simulate algorithm'''
WIDTH = 800
pygame.init()
WIN = pygame.display.set_mode((WIDTH,WIDTH))#create window to display path
pygame.display.set_caption("A* Path Finding Algorithm")

'''get clicked position'''
def get_clicked_pos(pos,width,rows):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x//gap
    return row,col

''' reset min path from start point to end point '''
def reset_path(grid):
    rows = len(grid)
    for i in range(rows):
        for j in range(rows):
            spot = grid[i][j]
            if not spot.is_startPoint() and not spot.is_endPoint() and not spot.is_barrier():
                spot.reset()
    return grid

''' create initial state for algorithm '''
def initial_State(width,rows):
    gap = width // rows
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid


def draw_grid(win,width,rows):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))

def draw(win,grid,width,rows):
    win.fill(BEIGE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,width,rows)
    pygame.display.update()

''' random barriers on map '''
def random_barrier(grid):
    i=0
    rows = len(grid)
    while i<len(grid)**2//4:
        row = randrange(0,rows)
        col = randrange(0,rows)
        spot = grid[row][col]
        if not spot.is_startPoint() and not spot.is_endPoint() and not spot.is_barrier():
            grid[row][col].make_barriers()
        i+=1
    return grid

def goal_State(path,start,end):
    for curr in path:
        if curr != start and curr !=end:
            curr.make_path()

def run_Algorithm(win,width):
    rows = 50
    run = True
    startPoint = None
    endPoint = None
    barriers = []
    started = False
    grid = initial_State(width,rows)
    minpath = []
    while run:
        draw(win,grid,width,rows)
        for event in pygame.event.get():
            spot = None
            if event.type == pygame.QUIT:
                run = False
            '''event when click left mouse'''
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,width,rows)
                spot = grid[row][col]
                if not startPoint and spot!=endPoint:
                    startPoint = spot
                    startPoint.make_startPoint()
                elif not endPoint and startPoint and spot != startPoint:
                    endPoint = spot
                    endPoint.make_endPoint()
                elif not spot.is_endPoint() and not spot.is_startPoint():
                    spot.make_barriers()
                    barriers.append(spot)
                    if spot in minpath:
                        grid = reset_path(grid)
                started = False
            '''event when click right mouse'''
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,width,rows)
                spot = grid[row][col]
                spot.reset()
                if spot == startPoint: #remove starting point
                    startPoint = None
                    started = False
                    grid = reset_path(grid)
                if spot == endPoint: #remove end point
                    endPoint = None
                    started = False
                    grid = reset_path(grid)
                if spot in barriers: #remove barrier point
                    barriers.remove(spot)
                    started = False
            for row in grid: #update neighbor points of all spot on map
                for spot in row:
                    spot.update_neighbors(grid)
            if event.type == pygame.KEYDOWN:#event if type 1 key on keyboard
                ''' press the spacebar on keyboard'''
                if event.key == pygame.K_SPACE: #Run algorithm
                    if startPoint and endPoint and not started:
                        grid = reset_path(grid)
                        started = True
                        minpath = A_starAlgorithm(startPoint,endPoint,grid,lambda: draw(win,grid,width,rows),win)
                        goal_State(minpath,startPoint,endPoint)
                if event.key == pygame.K_c: #press C button on keyboard ==> clear map
                    startPoint = None
                    endPoint = None
                    grid = initial_State(width,rows)
                if event.key == pygame.K_r:#press C button on keyboard ==> random barrier spots on map
                    grid = random_barrier(grid)
                    started = False
                    grid = reset_path(grid)
    pygame.quit()
if __name__== '__main__':
    run_Algorithm(WIN,WIDTH)
