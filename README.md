# MazeSolver
Generates a maze and finds the most efficient path to the end using the A* pathfinding algorithm. Uses pygame to generate animations.
Uses a class "Cell" to represent a point in the grid. The Cell class has a list with 4 boolean values that indicates whether it has a wall or not. Using recursive backtracking, we can generate a maze. Then using A* we can solve the generated maze. Outputs two files: maze.jpeg, containing a picture of the generated maze, and solvedmaze.jpeg, containing the solved version of the maze. 
