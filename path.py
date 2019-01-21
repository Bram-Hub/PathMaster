# A Pathfinding algorithm for Intro to Cognitive Science
# Written by Corey McClymonds

from heapq import heappush, heappop
import math

class Grid:
    """A Grid that can hold a value for each cell."""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def new_grid(self, val=0):
        """Empty Grid"""
        self.grid = []
        row_grid = []
        for column in range(self.height):
            for row in range(self.width):
                row_grid.append(val)
            self.grid.append(row_grid)
            row_grid = []
        return self.grid

    def set_grid(self, list):
        """uses a 2D list to quickly set the grid."""
        self.grid = list

    def pprint(self):
        for row in range(self.height):
            for column in range(self.width):
                print self.grid[row][column],
            print

class Maze:
    """Loads a maze and then solves it.
    
    The map format is rather simple:
    S stands for a starting point of the maze
    G stands for a goal
    X stands for a wall
    0 stands for open, will be replaced with other data
    """

    def __init__(self, width, height, list=[]):
        """The list contains a 2D list which is the maze."""
        self.maze = Grid(width, height)
        self.maze.new_grid() if list == [] else self.maze.set_grid(list)
        self.state = []
        self.goals = []
        self.pathlen = -1
        self.h = None

    def pprint(self):
        self.maze.pprint()
        print

    def start_solve(self, h):
        self.h = h
        for column in range(self.maze.height):
            for row in range(self.maze.width):
                if self.maze.grid[column][row] == 'S':
                    heappush(self.state, (self.h(column, row), 0, column, row))
                if self.maze.grid[column][row] == 'G':
                    self.goals.append((column, row))

    def continue_solve(self):
        """Continues stepping through AStar.

        returns 0 on reaching a goal state
        returns 1 on not being finished"""
        temp_state = []
        # Get the best (lowest distance) open node
        c, len, x, y = heappop(self.state)
        neighbors = self.getneighbors(x,y)
        # Test all open neighbors
        for nx, ny in neighbors:
            if self.maze.grid[nx][ny] == 'G':
                # Reached goal
                self.pathlen = len+1
                return 0
            if self.maze.grid[nx][ny] == 0:
                # Pushes the neighbor to the heap with a scaled cost
                heappush(self.state, (len+1+self.h(nx, ny)*1.001, len+1, nx, ny))
                self.maze.grid[nx][ny] = len+1
        return 1

    def getneighbors(self, x,y):
        neighbors = []
        if x-1 >= 0: neighbors.append((x-1,y))
        if x+1 < self.maze.height: neighbors.append((x+1,y))
        if y-1 >= 0: neighbors.append((x,y-1))
        if y+1 < self.maze.width: neighbors.append((x,y+1))
        return neighbors

    def dijkstra(self, x, y):
        return 0

    def manhattan(self, x, y):
        # This is the farthest away it could possibly be
        mindist = self.maze.width + self.maze.height + 1
        for gx, gy in self.goals:
            tx = x - gx if x > gx else gx - x
            ty = y - gy if y > gy else gy - y
            if tx + ty < mindist:
                mindist = tx + ty
        return mindist

    def perfect(self, x, y):
        # Creates a copy and runs dijkstra's on it, returning an exact h(x,y)
        tempmaze = Maze(self.maze.width, self.maze.height)
        for row in range(self.maze.height):
            for column in range(self.maze.width):
                if self.maze.grid[row][column] == 'X':
                    tempmaze.maze.grid[row][column] = 'X'
                elif self.maze.grid[row][column] == 'G':
                    tempmaze.maze.grid[row][column] = 'G'
        tempmaze.maze.grid[x][y] = 'S'
        tempmaze.start_solve(tempmaze.dijkstra)
        try:
            while tempmaze.continue_solve() == 1: pass
        except IndexError:
            return 0
        return tempmaze.pathlen

if __name__ == "__main__":
    maze = Maze(9,8,
           [[ 0 , 0 , 0 ,'X','X', 0 ,'X', 0 ,'S'],
            [ 0 ,'X', 0 , 0 ,'X', 0 , 0 , 0 , 0 ],
            [ 0 ,'X','X', 0 , 0 , 0 ,'X','X','X'],
            [ 0 ,'X', 0 , 0 ,'X', 0 , 0 , 0 , 0 ],
            [ 0 , 0 , 0 ,'X','X', 0 ,'X', 0 ,'X'],
            [ 0 ,'X', 0 , 0 ,'X', 0 ,'X', 0 , 0 ],
            [ 0 ,'X','X', 0 , 0 , 0 ,'X','X', 0 ],
            [ 0 ,'G', 0 , 0 ,'X', 0 , 0 , 0 , 0 ]])
    maze.pprint()
    maze.start_solve(maze.dijkstra)
    import time
    while maze.continue_solve() == 1:
        maze.pprint()
        time.sleep(1)
    maze.pprint()
