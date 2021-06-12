import pygame


RED = (255, 0, 0)
LIGHTGRAY = (200,200,200)
BLACK = (0, 0, 0)
ORANGE = (255, 165 ,0)
TURQUOISE = (64, 224, 208)
BEIGE = (250,250,250)
class Spot:#object show 1 vertex in graph
    def __init__(self,row,col,width,total_rows):
        self.color = BEIGE
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.total_rows = total_rows
        self.width = width
        self.neighbors = []
    def get_pos(self): #get position of spot on map
        return self.row, self.col
    def reset(self):
        self.color = BEIGE
    def is_barrier(self): #check whether spot is barrier or not
        return self.color == BLACK
    def is_startPoint(self): #check whether spot is start point or not
        return self.color == ORANGE
    def is_endPoint(self): #check whether spot is end point or not
        return self.color == TURQUOISE
    def make_startPoint(self): #pick a spot on map as starting point
        self.color = ORANGE
    def make_endPoint(self): #pick a spot on map as end point
        self.color = TURQUOISE
    def make_barriers(self): #pick a spot on map as barrier point
        self.color = BLACK
    def make_neighbor(self): #pick a spot on map as neighbor point of self.point
        self.color = LIGHTGRAY
    def make_path(self):
        self.color = RED #draw min path
    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])
        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row+1][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col+1])
        if self.row > 0 and self.col > 0 and not grid[self.row-1][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col-1])
        if self.col < self.total_rows - 1 and self.row > 0 and not grid[self.row-1][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col+1])
        if self.col > 0 and self.row < self.total_rows - 1 and not grid[self.row+1][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col-1]) 
    def draw(self,win):#draw rectangle
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    def __lt__(self, other):
        return False