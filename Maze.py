import pygame;
import math;
import random;
WIDTH: int = 600;
HEIGHT: int = 600;
AMT: int = 20;
LIGHT_PINK = (255,204,255);
BLACK = (0,0,0);
BLUE = (0,0,255);
GREEN = (0,255,0);
WHITE = (255,255,255);

rows: int = math.floor(WIDTH/AMT);
cols: int = math.floor(HEIGHT/AMT);
visitedCells = [];
cells = [None] * (rows*cols);

class Cell:
	def __init__(self, x : int, y : int):
		self.x: int = x;
		self.y: int = y;
		self.walls = [True, True, True, True];
		self.visited: bool = False;
		self.gScore: float = float('inf');
		self.fScore: float = float('inf');
		self.i: int = self.x*AMT;
		self.j: int = self.y*AMT;
		
	def __str__(self):
		return (str(self.x) + " "+ str( self.y));
		
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y;
		
	def __hash__(self):
		return (53 + (self.x)) * 53 +(self.y);
	
	def highlight(self, screen, color):
		rectangle: Rect = pygame.Rect(self.i, self.j,  AMT, AMT);
		pygame.draw.rect(screen, color, rectangle);
	
	def draw(self, screen):
		rectangle = pygame.Rect(self.i, self.j,  AMT, AMT);
		pygame.draw.rect(screen, WHITE, rectangle);
		if (self.walls[0]): # top
			pygame.draw.line(screen,BLACK, (self.i, self.j), (self.i + AMT, self.j));
		if (self.walls[1]): # left
			pygame.draw.line(screen,BLACK, (self.i + AMT, self.j), (self.i + AMT, self.j + AMT));
		if (self.walls[2]): # bottom
			pygame.draw.line(screen,BLACK, (self.i +AMT, self.j + AMT), (self.i, self.j + AMT));
		if (self.walls[3]): # right
			pygame.draw.line(screen,BLACK, (self.i, self.j + AMT), (self.i, self.j));
			
	def getRandomNeighbor(self,cells):
		neighbors = self.getNeighbors(cells);
		visitedNeighbors = [cell for cell in neighbors if cell.visited == False];
		if (len(visitedNeighbors) == 0): 
			return 0;
		else:
			return random.choice(visitedNeighbors);
	
	def getNeighbors(self, cells):
		neighbors = [];
		top = getIndex(self.x, self.y + 1);
		left = getIndex(self.x - 1, self.y);
		bottom = getIndex(self.x, self.y - 1);
		right = getIndex(self.x + 1, self.y);
		if (self.y < cols - 1):
			neighbors.append(cells[top]);
		if (self.x > 0):
			neighbors.append(cells[left]);
		if (self.y > 0) :
			neighbors.append(cells[bottom]);
		if (self.x < rows - 1):
			neighbors.append(cells[right]);
		if (len(neighbors) == 0): 
			return 0;
		else:
			return neighbors;

def getIndex(x: int, y: int): 
	return cols * y + x;
	
def removeWalls(current, neighbor):
	x = current.x - neighbor.x;
	if x == 1:
		return (3,1); 
	elif x == -1:
		return (1,3); 
	y = current.y - neighbor.y;
	if y == 1:
		return (0,2); 
	elif y == -1:
		return (2,0); 

def notBlocked(current, neighbor):
	x = current.x - neighbor.x;
	if x == 1:
		if current.walls[3] == False and neighbor.walls[1] == False:
			return True;
	elif x == -1:
		if current.walls[1] == False and neighbor.walls[3] == False:
			return True;
	y = current.y - neighbor.y;
	if y == 1:
		if current.walls[0] == False and neighbor.walls[2] == False:
			return True;
		
	elif y == -1:
		if current.walls[2] == False and neighbor.walls[0] == False:
			return True;
	return False;	

def generateMaze():
	cells[0].visited = True;
	visitedCells.append(cells[0]);   # initializing
	current = cells[0];
	while True:	
		for i in range(len(cells)):
			cells[i].draw(screen);	
			pygame.event.pump()
		neighbor = current.getRandomNeighbor(cells);
		current.highlight(screen, GREEN);
		pygame.display.update();	
		current.draw(screen);
		pygame.event.pump();
		if isinstance(neighbor, Cell):
			neighborIndex = cells.index(neighbor);
			currentIndex = cells.index(current);
			wallsToClose = removeWalls(current,neighbor);
			if len(wallsToClose) != 0:
				cells[currentIndex].walls[wallsToClose[0]] = False;
				cells[neighborIndex].walls[wallsToClose[1]] = False;
			visitedCells.append(current);	
			cells[neighborIndex].visited = True;
			current = neighbor;
		elif (len(visitedCells) != 0):
			current = visitedCells.pop();
			current.draw(screen);
		if (len(visitedCells) == 0):
			print("Done!");
			pygame.image.save(screen,'maze.jpeg');
			break;
	
def distanceBetween(source: Cell, point: Cell):
	return math.sqrt((source.x - point.x)**2 + (source.y - point.y)**2);
	
def trace(path, current,screen):
	clock = pygame.time.Clock();
	total_path = [current];
	while current in path.keys():
		current = path[current];
		total_path.append(current);
	total_path.reverse();
	for i in range(len(total_path)):	
		total_path[i].highlight(screen, GREEN);
		clock.tick(30);
		pygame.event.pump();
		pygame.display.update();	
	pygame.image.save(screen,'solvedmaze.jpeg');

def solveMaze(maze):
	cellList = [0] * (rows*cols);
	path = {};
	startPoint: Cell = maze[0];
	endPoint: Cell = maze[cols*rows -1];
	startPoint.gScore: float = 0;
	startPoint.fScore: float = startPoint.gScore + distanceBetween(startPoint, endPoint);
	cellList.append(startPoint);
	while len(cellList) != 0:
		current: Cell = cellList.pop();
		current.highlight(screen, GREEN);
		pygame.display.update();
		current.draw(screen);		
		pygame.event.pump();
		if (current == endPoint):
			print("end");
			trace(path, current,screen);
			break;
		if (not (isinstance(current.getNeighbors(cells), int))):
			for neighbor in current.getNeighbors(cells):
				tentGScore = current.gScore + 1;
				if (tentGScore < neighbor.gScore and notBlocked(current, neighbor)):
					pygame.display.update();
					path[neighbor] = current;
					neighbor.gScore = tentGScore;
					neighbor.fScore = neighbor.gScore + distanceBetween(neighbor, endPoint);
					if (neighbor not in [cell for cell in cellList if isinstance(cell, Cell)]):
						cellList.append(neighbor);
						[cell for cell in cellList if isinstance(cell, Cell)].sort(key=lambda x: x.gScore, reverse=True);
						
for col in range(cols):
	for row in range(rows):
		index: int = getIndex(row,col);
		cells[index] = Cell(row,col);
screen = pygame.display.set_mode((WIDTH,HEIGHT));
screen.fill(WHITE);
generateMaze();
solveMaze(cells);