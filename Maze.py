from __future__ import annotations

from enum import Enum
from typing import NamedTuple
import random

from Stack import *
from Queue import *  
from PriorityQueue import *

################################################################################
class Contents(str, Enum):
    ''' create an enumeration to define what the visual contents of a Cell are;
        using str as a "mixin" (multiple inheritance) forces all the entries to
        be strings; using an Enum means no cell entry can be anything other
        than the options here
    '''
    # if the fancy Unicode versions don't display correctly in your terminal,
    # just use 'S', 'G', 'X', '*' instead
    EMPTY   = ' '
    START   = '⦿' #'S' 
    GOAL    = '◆' #'G'
    BLOCKED = '░' #'X'
    PATH    =  '★' #'*'

    def __str__(self) -> str: return self.value

################################################################################
class Position(NamedTuple):
    ''' just allows us to use .row and .col rather than the less-easy-to-read
        [0] and [1] for accessing values'''
    row: int
    col: int

    def __str__(self) -> str: return f"({self.row},{self.col})"

################################################################################
class SearchOrder(Enum):
    ''' enumeration for neighboring cells search order '''
    NSWE   = 1
    NESW   = 2
    RANDOM = 3
    SEWN = 4
################################################################################
class Cell:
    ''' class that allows us to use Cell as a data type -- an ordered triple 
        of row, column, & cell contents 
        (see Contents class enumeration above) 
    '''
    __slots__ = ('_position', '_contents', '_parent')

    def __init__(self, row: int, col: int, contents: Contents):
        self._position:  Position = Position(row, col)
        self._contents:  Contents = contents
        self._parent:    Cell     = None    # parent of this Cell during exploration
       
    def getPosition(self) -> Position:
        ''' method to return the (row,col) Position of this cell
        Returns:
            a Position object containing the cell's row and column
        '''
        return Position(self._position.row, self._position.col)

    def getParent(self) -> Cell:
        ''' method to return the parent of this Cell object as determined during
            maze exploration
        Returns:
            a Cell object corresponding to the cell that considered this cell
            during the exploration process
        '''
        return self._parent

    def setParent(self, parent: Cell) -> None:
        ''' setter method to update this Cell's parent
        Parameters:
            parent: a different Cell object
        Raises:
            ValueError if self == parent
        '''
        if self == parent: raise ValueError(f"a Cell cannot be its own parent")
        self._parent = parent

    def markOnPath(self) -> None:
        ''' method to identify this cell as being on the path from source
            to goal
        '''
        self._contents = Contents.PATH

    def isBlocked(self) -> bool:
        ''' Boolean method to indicate whether this cell contains a block
        Returns:
            True if the cell is blocked (cannot be explored), False o/w
        '''
        return self._contents == Contents.BLOCKED

    def isGoal(self) -> bool:
        ''' Boolean method to indicate whether this cell is the goal
        Returns:
            True if the cell is the maze goal, False o/w
        '''
        return self._contents == Contents.GOAL

    def __str__(self) -> str:
        ''' creates and returns a string representation of this cell
        Returns:
            a string identifying the cell's row, col, and cell contents
        '''
        contents = "[EMPTY]" if self._contents == Contents.EMPTY else self._contents
        string = f"({self._position.row}, {self._position.col}): {contents} "
        if self._parent is not None:
            string += f"({self._parent._position.row}, {self._parent._position.col})"
        return string

    def __repr__(self) -> str:
        ''' overriding __repr__ so that printing, e.g., a list of Cell objects
            (which will call __repr__ for each) will call __str__ for each, printing
            nicely
        Returns:
            a string identifying the cell's row, col, and cell contents
        '''
        return self.__str__()

    def __eq__(self, other: Cell) -> bool:
        ''' indicates whether a given other Cell is equal to this Cell
        Returns:
            True if this Cell and the other Cell are the same, False o/w
        '''
        return self._position.row == other._position.row and \
               self._position.col == other._position.col and \
               self._contents == other._contents

################################################################################
class Maze:
    ''' class representing a 2D maze of Cell objects '''
    __slots__ = ('_grid', '_num_rows', '_num_cols', '_start', '_goal', '_search_order', '_num_cells_explored', '_path_length')
 
    def __init__(self, rows: int = 10, cols: int = 10,
                       start:        Position = None, \
                       goal:         Position = None, \
                       prop_blocked: float = 0.1, \
                       search_order: SearchOrder = SearchOrder.NESW, \
                       debug: bool = False):
        ''' initializer method for a Maze object
        Parameters:
            rows:          number of rows in the grid
            cols:          number of columns in the grid
            start:         Position object indicating the (row,col) of the start cell
            goal:          Position object indicating the (row,col) of the goal cell
            prop_blocked:  proportion of cells to be blocked (between 0.0 and 1.0)
            debug:         whether to use one of the Maze examples from course slides
        Raises:
            TypeError  if prop_blocked is not a float
            ValueError if prop_blocked is not in (0,1)
            TypeError  if start or goal is not a Position object
            ValueError if row/col of start or goal is out of range
        '''
        msg = "prop_blocked must be a float between 0 and 1"
        try:
            float(prop_blocked)
        except:
            raise TypeError(msg)
        else:
            if prop_blocked < 0 or prop_blocked > 1:
                raise ValueError(msg)

        # if user doesn't specify either start or goal, force them to
        # be respectively in the UL and LR corners
        if start is None or goal is None:
            start = Position(0,0)
            goal  = Position(rows - 1, cols - 1)

        if not isinstance(start, Position) or not isinstance(goal, Position):
            raise TypeError("start and goal must both be Position objects")

        if start.row < 0 or start.row >= rows or \
           start.col < 0 or start.col >= cols:
            raise ValueError("invalid (row,col) given for start cell")
        if goal.row  < 0 or goal.row  >= rows or \
           goal.col  < 0 or goal.col  >= cols:
            raise ValueError("invalid (row,col) given for goal cell")

        if debug: 
            # to match DCS 229 slides example
            rows = 6; cols = 5;
            start = Position(5, 0)
            goal  = Position(0, 4)

        self._num_rows     = rows
        self._num_cols     = cols
        self._start        = Cell(start.row, start.col, Contents.START)
        self._goal         = Cell(goal.row,  goal.col,  Contents.GOAL)
        self._search_order = search_order
        self._num_cells_explored = 0
        self._path_length = 0
        
        # create a rows x cols 2D list of Cell objects, intially all empty
        self._grid: list[list[Cell]] = \
            [ [Cell(r,c, Contents.EMPTY) for c in range(cols)] for r in range(rows) ]

        # set the start and goal cells (overriding two empty Cell objects from above)
        self._grid[start.row][start.col] = self._start
        self._grid[goal.row][goal.col]   = self._goal

        # put blocks at random spots in the grid, using given proportion;  
        # start by creating a collapsed 1D version of the grid, then
        #   remove the start and goal, and then randomly pick cells to block;
        # note that we are using identical object references in both 
        #   options and self._grid so that updates to options will be seen
        #   in self._grid (i.e., options is not a deep copy of cells);
        if not debug: 
            options = [cell for row in self._grid for cell in row]
            options.remove(self._start)
            options.remove(self._goal)
            blocked = random.sample(options, k = round((rows * cols - 2) * prop_blocked))
            for b in blocked: 
                b._contents = Contents.BLOCKED  # this is changing self._grid!
        else:
            # for example from slides
            pos = [(1,0),(1,3),(2,1),(2,4),(3,2),(5,1),(5,3),(5,4)]
            for p in pos:
                self._grid[p[0]][p[1]]._contents = Contents.BLOCKED

    def __str__(self) -> str:
        ''' creates a str version of the Maze, showing contents, with cells
            delimited by vertical pipes 
        Returns:
            a str representation of the Maze
        '''
        maze_str = ""
        for row in self._grid:  # row : list[Cell] 
            maze_str += "|" + "|".join([cell._contents for cell in row]) + "|\n"
        return maze_str[:-1]  # remove the final \n

    def getStart(self) -> Cell: 
        ''' accessor method to return the Cell object corresponding to the Maze start
        Returns:
            the Cell object at the Maze start location
        '''
        return self._start

    def getGoal(self) -> Cell:
        ''' accessor method to return the Cell object corresponding to the Maze goal
        Returns:
            the Cell object at the Maze goal location
        '''
        return self._goal

    def getSearchLocations(self, cell: Cell) -> list[Cell]:
        ''' method to return a list of Cell objects of valid places to explore
            (i.e., not blocked and within the grid)
        Parameters:
            cell:  the current Cell being explored
            order: SearchOrder enum -- one of NSWE, NESW, or RANDOM
        Returns:
            a list of valid Cell objects (in N/S/W/E exploration) for further
            consideration
        '''
        validNeigh = []
        if self._search_order == SearchOrder.NSWE:
            searchDirections =  [(-1, 0), (1, 0), (0, -1), (0, 1)]
        elif self._search_order == SearchOrder.NESW:
            searchDirections =  [(-1, 0),(0, 1), (1, 0), (0, -1)]
        elif self._search_order == SearchOrder.SEWN:
            searchDirections = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        elif self._search_order == SearchOrder.RANDOM:
            searchDirections = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(searchDirections)  
        
         
        currentRow, currentCol = cell.getPosition()
        for nextRow, nextCol in searchDirections:
            newRow = currentRow + nextRow
            newCol = currentCol + nextCol
            if newRow >= 0 and newRow < self._num_rows and newCol >= 0 and newCol < self._num_cols:
                neighCell = self._grid[newRow][newCol]
                if not neighCell.isBlocked():
                    validNeigh.append(neighCell)

        return validNeigh   


    def dfs(self) -> Cell | None:
        ''' method to perform DFS (using a stack) to implement maze searching
        Returns:
            a Cell object corresponding to the Maze goal, or None if no goal
            can be found
        ''' 
        #Use DFS + stack:
        #    stack: push new Cell objects to be explored
        #            (which should also keep track of the parent)
        #    list:  cells already explored

        pathStack = Stack()
        pathStack.push(self._start)
        visitedCells = [self._start.getPosition()]
        
        while not pathStack.is_empty():
            currentCell = pathStack.pop()

            if currentCell.isGoal():
                return currentCell
            
            validNeighbors = self.getSearchLocations(currentCell)
            for neighbor in validNeighbors:
                if neighbor.getPosition() not in visitedCells:
                    visitedCells.append(neighbor.getPosition())
                    neighbor.setParent(currentCell)
                    pathStack.push(neighbor)
                    self._num_cells_explored+=1


        print(f"Goal not attainable and number cells explroed is {self._num_cells_explored}")
        return None
            

    def bfs(self) -> Cell | None:
        ''' method to perform BFS (using a queue) to implement maze searching
        Returns:
            a Cell object corresponding to the Maze goal, or None if no goal
            can be found
        ''' 
        #Use BFS + queue:
        #    queue: push new Cell objects to be explored
        #            (which should also keep track of the parent)
        #    list:  cells already explored
        pathQueue = Queue()
        pathQueue.push(self._start)
        visitedCells = [self._start.getPosition()]
        while not pathQueue.isEmpty():
            currentCell = pathQueue.pop()

            if currentCell.isGoal():
                return currentCell
            
            validNeighbors = self.getSearchLocations(currentCell)
            for neighbor in validNeighbors:
                if neighbor.getPosition() not in visitedCells:
                    visitedCells.append(neighbor.getPosition())
                    neighbor.setParent(currentCell)
                    pathQueue.push(neighbor)            
                    self._num_cells_explored+=1



        print(f"Goal not attainable and number cells explored is {self._num_cells_explored}")
        return None
    
    def aStar(self) -> Cell | None:
        to_explore: PriorityQueue[float, Cell] = PriorityQueue()
        explored: dict[Position, float] = {}

        n = self.getStart()
        g_n = 0
        h_n = abs(n.getPosition().col - self.getGoal().getPosition().col) + abs(n.getPosition().row - self.getGoal().getPosition().row)
        f_n = g_n + h_n

        to_explore.insert(f_n, n)
        explored[n.getPosition()] = g_n

        while not to_explore.isEmpty():
            e = to_explore.removeMin()
            n = e.value

            if n.isGoal():
                return n
            
            for m in self.getSearchLocations(n):
                updated_m_cost = explored[n.getPosition()] + 1
                if m.getPosition() not in explored or updated_m_cost < explored[m.getPosition()]:
                    g_m = updated_m_cost
                    explored[m.getPosition()] = g_m
                    h_m = abs(m.getPosition().col -self.getGoal().getPosition().col) + abs(m.getPosition().row - self.getGoal().getPosition().row)
                    f_m = g_m + h_m
                    to_explore.insert(f_m, m)
                    self._num_cells_explored+=1
                    m.setParent(n)

            

        print(f"Goal not attainable and number cells explored is {self._num_cells_explored}")
        return None

    def calculatePathLength(self, goal: Cell)->None:
        """method to calculate the path length without printing the maze

        Args:
            goal (Cell): the finish cell
        """

        cell = goal
        if cell is None or cell._parent is None:
            print("Goal not reachable or not set.")
            self._path_length = 0
            return 
        
        while cell._parent:
            cell = cell._parent
            self._path_length+=1
        

    def showPath(self, goal: Cell) -> None:
        ''' method to update the path from start to goal, identifying the steps
            along the way as belonging to the path (updating the cell via
            .markOnPath, which will change that cell's ._contents to
            Contents.PATH), printing the final resulting solutions
        Parameters:
            goal: a Cell object corresponding to the goal location
        Returns:
            nothing -- just updates the cells in the grid to identify those on the path
        '''

        path = []
        cell = goal
        while cell._parent is not None:
            path.append(cell)
            cell = cell._parent
        path.append(cell)  # should be the start
        assert(cell == self._start)

        path.reverse()  # reverse the list

        for cell in path:
            if cell != self._start and cell != self._goal:
                cell.markOnPath()

        # print the maze, i.e., using __str__ which will show the solved maze
        print(self)

##############################################################################################################################################################################
def main() -> None:
    mazeSize = 10
    floatBlocked = 0.1
    #testing get search locations
    random.seed(54321)
    m = Maze(mazeSize,mazeSize, start = Position(0,0), goal = Position(mazeSize-1,mazeSize-1), prop_blocked = floatBlocked)
    cell1 = Cell(0,0,' ')
    cell2 = Cell(1,1,' ')
    print(f"Valid search locations from 0,0 of this maze are {m.getSearchLocations(cell1)}")
    print(f"Valid search locations from 1,1 of this maze are {m.getSearchLocations(cell2)}")
    print('\n')

    #testing dfs 
    result_1_dfs = m.dfs()
    m.showPath(result_1_dfs)
    print('\n')
    mazeSize = 30 #resize the maze to test dfs again
    m2 = Maze(mazeSize,mazeSize, start = Position(0,0), goal = Position(mazeSize-1,mazeSize-1), prop_blocked = floatBlocked)
    result_2_dfs = m2.dfs()
    m2.showPath(result_2_dfs)
    print('\n')
    mazeSize = 50 #resize for third test
    m3 = Maze(mazeSize,mazeSize, start = Position(0,0), goal = Position(mazeSize-1,mazeSize-1), prop_blocked = floatBlocked)
    result_3_dfs = m3.dfs()
    m3.showPath(result_3_dfs)
    print('\n')

     #tests bfs
    mazeSize = 10
    random.seed(54321)
    l = Maze(mazeSize,mazeSize, start = Position(0,0), goal = Position(mazeSize-1,mazeSize-1), prop_blocked = floatBlocked)
    result_1_bfs = l.bfs()
    l.showPath(result_1_bfs)
    print('\n')
    mazeSize = 30 #resize the maze to test dfs again
    l2 = Maze(mazeSize,mazeSize, start = Position(0,0), goal = Position(mazeSize-1,mazeSize-1), prop_blocked = floatBlocked)
    result_2_bfs = l2.bfs()
    l2.showPath(result_2_bfs)
    print('\n')
    mazeSize = 50 #resize for third test
    l3 = Maze(mazeSize,mazeSize, start = Position(0,0), goal = Position(mazeSize-1,mazeSize-1), prop_blocked = floatBlocked)
    result_3_bfs = l3.bfs()
    l3.showPath(result_3_bfs)
    print('\n')

    #testing a star
    mazeSize = 10
    random.seed(54321)
    d = Maze(mazeSize,mazeSize, start = Position(0,0), goal = Position(mazeSize-1,mazeSize-1), prop_blocked = floatBlocked)
    result_1_astar = d.aStar()
    d.showPath(result_1_astar)
    print('\n')
    mazeSize = 30 #resize the maze to test dfs again
    d2 = Maze(mazeSize,mazeSize, start = Position(0,0), goal = Position(mazeSize-1,mazeSize-1), prop_blocked = floatBlocked)
    result_2_astar = d2.aStar()
    d2.showPath(result_2_astar)
    print('\n')
    mazeSize = 50 #resize for third test
    d3 = Maze(mazeSize,mazeSize, start = Position(0,0), goal = Position(mazeSize-1,mazeSize-1), prop_blocked = floatBlocked)
    result_3_astar =d3.aStar()
    d3.showPath(result_3_astar)
    print('\n')


def word()->None:
    order = SearchOrder.NSWE
    if order == SearchOrder.NSWE:
        print(order.value)
    elif order == SearchOrder.NESW:
        print(order.value)
    elif order == SearchOrder.RANDOM:
        print(order.value)

    location = Position(9,10)
    print(f"Row is {location.row}")
    print(f"col is {location.col}")

    cell = Cell(3,3, Contents.BLOCKED)
    start = Cell(0,0, Contents.START)
    goal = Cell(9,9, Contents.GOAL)
    new_cell = Cell(9,8,Contents.EMPTY)
    print(cell)
    print(start)
    print(goal)
    print(new_cell)
    goal.setParent(new_cell)
    print(f"parent of {goal} is {goal.getParent()}")
    new_cell.markOnPath()
    print(new_cell)


def checkingCases()->None:
    random.seed(3520051)
    m = Maze(50,50, prop_blocked=0.25, search_order=SearchOrder.NSWE)
    goal = m.bfs()
    m.calculatePathLength(goal)
    m.showPath(goal)
    print(f"BFS: cells explored = {m._num_cells_explored} and path length = {m._path_length}")

    random.seed(3520051)
    a = Maze(50,50, prop_blocked=0.25, search_order=SearchOrder.NSWE)
    goal = a.dfs()
    a.calculatePathLength(goal)
    a.showPath(goal)

    d = Maze(50,50, prop_blocked=0.25, search_order=SearchOrder.NSWE)
    goal = d.aStar()
    d.calculatePathLength(goal)
    print(f"aStar: cells explored = {d._num_cells_explored} and path length = {d._path_length}")

if __name__ == "__main__":
    main()