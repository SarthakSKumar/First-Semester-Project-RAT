 
def MAZE(maze):   #Just an outer function which uses a backtracking function to create a solution maze
    sol=[[0 for j in range(N)]for i in range(N)] #Creates N x N 2D list(only made it for square mazes for now)
     
    if BACKTRACKING_ALGORITHM(maze,0,0,sol) == False: #Returns false if the first block on the maze is invalid
        print("Solution doesn't exist")
        return False
     
    Solution_matrix(sol)
    return True
     
def BACKTRACKING_ALGORITHM(maze,x,y,sol): #Main backtracking algorithm where all the computation takes place

    if x==N-1 and y==N-1: #if (x,y) is the co-ordinate for the last tile, the maze is solved and it returns true
        sol[x][y]=1
        return True
         
    
    if check(maze,x,y) == True: #checks if the rat is still in the maze(valid tile)       
        sol[x][y]=1 #adds the tile to the solution path         
        
        if BACKTRACKING_ALGORITHM(maze,x+1,y,sol) == True: #Move forward in x direction(to the right) and returns true if the move is valid
            return True
             
        if BACKTRACKING_ALGORITHM(maze,x,y+1,sol) == True: #Move forward in y direction(downwards) if x direction is blocked/invalid, 
            return True
         
        sol[x][y]=0 #If both x and y paths are blocked/invalid then it backtracks its movements by unmarking the path to the value '0'
        return False

def check(maze,x,y): #Checks if the given (x,y) values is inside the maze. x value is column number and y value is row number     
    if x>=0 and x<N and y>=0 and y<N and maze[x][y]==1:
        return True

def Solution_matrix(sol): #Creates and Prints the final solution matrix with the correct path tiles displayed with the value '1'
    for i in sol:
        for j in i:
            print(str(j),end =" ")
        print()   
    return False
 
if __name__ == "__main__":
    
    print("Welcome!!!\n")
    maze = [ [1, 0, 0, 0, 1],
             [1, 1, 0, 1, 1],  # Creating the maze to be solved
             [0, 1, 0, 0, 0],
             [1, 1, 1, 0, 1],
             [1, 0, 1, 1, 1] ]
    for i in maze:
        for j in i:
            print(j,end=" ")
        print()
    print("\nThe maze above is the maze to be solved\n")
    N=len(maze) #Calculates the number of rows in the maze           
    MAZE(maze)
    
print("\nThe maze above is the solution maze")
