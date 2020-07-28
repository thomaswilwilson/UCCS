'''
THomas Wilson, Tyson Miller
Schelling Model of Housing Segregation

Program for simulating of a variant of Schelling's model of
housing segregation.  This program takes five parameters:

    filename -- name of a file containing a sample city grid

    R - The radius of the neighborhood: home at Location (i, j) is in
        the neighborhood of the home at Location (k,l)
        if k-R <= i <= k+R and l-R <= j <= l+R

    M threshold - minimum acceptable threshold for ratio of the number
                of similar neighbors to the number of occupied homes
                in a neighborhood for maroon homeowners.

    B threshold - minimum acceptable threshold for ratio of the number
                of similar neighbors to the number of occupied homes
                in a neighborhood for blue homeowners.

    max_steps - the maximum number of passes to make over the city
                during a simulation.

Sample:
  python3 schelling.py --grid_file=tests/a18-sample-grid.txt --r=1 --m_threshold=0.44 --b_threshold=0.70 --max_steps=2
'''

import os
import sys
import click
import utility


def neighbor_count(grid, R, l1):
    '''
    This function counts the number and types of neighbors a given person has.

    Intputs:
        grid: the grid
        location: a tuple specifying where you are in the grid
        R: The radius of the neighborhood: home at Location (i, j) is in
        the neighborhood of the home at Location (k,l)

    Returns: The number of "M' type neighbors, "B" type neighbors and total neighbors.
    '''
    grid_size = len(grid)
    m_neighbors = 0
    b_neighbors = 0
    t_neighbors = 0
    (x,y) = l1

    for i in range(len(grid)):
        for j in range(len(grid)):
            if (x >= 0 and x < grid_size) \
            and (x >= i - R and x <= i + R) \
            and (y >= 0 and y < grid_size) \
            and (y >= j - R and y <= j + R):
                if grid[i][j] == "M":
                    m_neighbors += 1
                    t_neighbors += 1
                elif grid[i][j] == "B":
                    b_neighbors += 1
                    t_neighbors += 1


    return m_neighbors, b_neighbors, t_neighbors

def is_satisfied(grid, R, l1, M_threshold, B_threshold):
    '''
    This function evaluates whether or not a person is satisfied at a given location.

    Inputs:
        grid - a list of lists of strings representing the format of the city.

        R - The radius of the neighborhood: home at Location (i, j) is in
        the neighborhood of the home at Location (k,l)
        if k-R <= i <= k+R and l-R <= j <= l+R

        l1 - a tuple representing a specific location of a resident in the city

        M threshold - minimum acceptable threshold for ratio of the number
                    of similar neighbors to the number of occupied homes
                    in a neighborhood for maroon homeowners.

        B threshold - minimum acceptable threshold for ratio of the number
                    of similar neighbors to the number of occupied homes
                    in a neighborhood for blue homeowners.


    Returns:
        A Boolean taking a value of True if the homeowner is satisfied and False if the homeowner is not satisfied
    '''
    # not contain an open (unoccupied) home.

    # YOUR CODE HERE

    m = neighbor_count(grid, R, l1)[0]
    b = neighbor_count(grid, R, l1)[1]
    t = neighbor_count(grid, R, l1)[2]
    x = l1[0]
    y = l1[1]
    similarity_score = 0
    if grid[x][y] == "M":
        similarity_score = m / t
        return similarity_score >= M_threshold
    if grid[x][y] == "B":
        similarity_score = b / t
        return similarity_score >= B_threshold


def dist(l1, l2):
    ''''
    This function calculates the distance between two points

    Inputs:
        l1: tuple
        l2: tuple

     Returns:
        d: Euclidean distance
    '''
    x1 = l1[0]
    x2 = l2[0]
    y1 = l1[1]
    y2 = l2[1]

    x_square = (x2-x1) * (x2-x1)
    y_square = (y2-y1) * (y2-y1)
    d = (x_square + y_square)**0.5
    return d


def find_opens(grid):
    '''
    Find locations of the open locations (pairs) in the grid.

    Inputs:
        grid: the grid

    Returns a list with the open locations.
    '''

    grid_size = len(grid)
    open_locations = []

    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == "O":
                open_locations.append((i, j))

    return open_locations

def swap_locations(grid, l1, l2):
    '''
    Swap the location of two people

    Inputs:
        grid: the grid
        l1: tuple
        l2: tuple

    Returns
        grid: returns a grid in which the locations of l1 and l2 have been swapped
    '''
    grid[l1[0]][l1[1]], grid[l2[0]][l2[1]] = grid[l2[0]][l2[1]], grid[l1[0]][l1[1]]


    return grid


def evaluate_open(grid, R, l1, M_threshold, B_threshold, opens):
    '''
       This function evaluates whether or not a resident would be satisfied at each of the open locations within the city.

       Inputs:
           grid - a list of lists of strings representing the city

           R- The radius of the neighborhood: home at Location (i, j) is in
         the neighborhood of the home at Location (k,l)
         if k-R <= i <= k+R and l-R <= j <= l+R

         l1 - a tuple representing a specific location of a resident in the city

         M threshold - minimum acceptable threshold for ratio of the number
                     of similar neighbors to the number of occupied homes
                     in a neighborhood for maroon homeowners.

         B threshold - minimum acceptable threshold for ratio of the number
                     of similar neighbors to the number of occupied homes
                     in a neighborhood for blue homeowners.

         Returns:
             viable_locations - a list of open locations in which the resident would be satisfied
    '''
    viable_locations = []
    open_locations = opens
    for i in range(len(open_locations)):
        swap_locations(grid, l1, open_locations[i])
        if is_satisfied(grid, R, open_locations[i], M_threshold, B_threshold) == True:
            viable_locations.append(open_locations[i])
            swap_locations(grid, l1, open_locations[i])
        else:
            swap_locations(grid, l1, open_locations[i])
    return viable_locations


def vibrancy(grid, R, l1):
    '''
    This function computes the vibrancy of a neighborhood or how many R-1 neighbors a location has

    Inputs:
        grid - a list of lists of strings representing the city

        1 - a neighborhood radius of 1

        l1 - a tuple representing a specific location of a resident in the city

    Returns:
        Vibrance - the number of R-1 neighbors at a given location
    '''
    vibrance = []
    vibrance = neighbor_count(grid, 1, l1)

    return vibrance[2]



def relocate(grid, R, l1, M_threshold, B_threshold, opens):
    '''
    This function takes one location and moves it into the optimal open space based on satisfaction, distance, vibrancy, and time on the market.

    Inputs:
        grid - a list of lists of strings representing the city

        R- The radius of the neighborhood: home at Location (i, j) is in
        the neighborhood of the home at Location (k,l)
        if k-R <= i <= k+R and l-R <= j <= l+R

        l1 - a tuple representing a specific location of a resident in the city

        M threshold - minimum acceptable threshold for ratio of the number
                    of similar neighbors to the number of occupied homes
                    in a neighborhood for maroon homeowners.

        B threshold - minimum acceptable threshold for ratio of the number
                    of similar neighbors to the number of occupied homes
                    in a neighborhood for blue homeowners.

    Returns:
        grid - the new grid after the location

        opens - the list of open locations within the city
    '''
    viable_locations = evaluate_open(grid, R, l1, M_threshold, B_threshold, opens)

    if len(viable_locations) == 0:
        return grid, 0, opens
    best_home = viable_locations[0]

    for i in range(len(viable_locations)):

        if i != 0:

            if dist(l1, viable_locations[i]) < dist(l1, best_home):
                best_home = viable_locations[i]
            elif dist(l1, viable_locations[i]) == dist(l1, best_home):
                if vibrancy(grid, R, viable_locations[i]) >= vibrancy(grid, R, best_home):
                    best_home = viable_locations[i]


    swap_locations(grid, l1, best_home)
    opens.append(l1)
    opens.remove(best_home)

    return grid, 1, opens




def one_step(grid, R, M_threshold, B_threshold, opens):
    '''
     This function simulates one step of the relocation for the entire city.

     Inputs:
         grid - a list of lists of strings representing the city

         R- The radius of the neighborhood: home at Location (i, j) is in
         the neighborhood of the home at Location (k,l)
         if k-R <= i <= k+R and l-R <= j <= l+R

         M threshold - minimum acceptable threshold for ratio of the number
                     of similar neighbors to the number of occupied homes
                     in a neighborhood for maroon homeowners.

         B threshold - minimum acceptable threshold for ratio of the number
                     of similar neighbors to the number of occupied homes
                     in a neighborhood for blue homeowners.

         opens - the list of open locations in the city
    '''
    relocations = 0
    grid_size = len(grid)
    for i in range(grid_size):
        for j in range(grid_size):
            l1 = (i,j)
            if is_satisfied(grid, R, l1, M_threshold, B_threshold) == False:
                grid, relocated, opens = relocate(grid, R, l1, M_threshold, B_threshold, opens)
                relocations += relocated
    return grid, relocations, opens








# DO NOT REMOVE THE COMMENT BELOW
#pylint: disable-msg=too-many-arguments
def do_simulation(grid, R, M_threshold, B_threshold, max_steps, opens):
    '''
    Do a full simulation.

    Inputs:
        grid: (list of lists of strings) the grid
        R: (int) radius for the neighborhood
        M_threshold: (float) satisfaction threshold for maroon homeowners
        B_threshold: (float) satisfaction threshold for blue homeowners
        max_steps: (int) maximum number of steps to do
        opens: (list of tuples) a list of open locations

    Returns:
        The total number of relocations completed.
    '''

    assert utility.is_grid(grid), ("The grid argument has the wrong type.  "
                                   "It should be a list of lists of strings "
                                   "with the same number of rows and columns")

    # YOUR CODE HERE
    # REPLACE -1 with an appropriate return value
    num_relocations = 0
    relocations = 1
    steps = 0
    while relocations > 0 and steps < max_steps:
        grid, relocations, opens = one_step(grid, R, M_threshold, B_threshold, opens)
        steps += 1
        num_relocations += relocations

    return num_relocations


@click.command(name="schelling")
@click.option('--grid_file', type=click.Path(exists=True))
@click.option('--r', type=int, default=1, help="neighborhood radius")
@click.option('--m_threshold', type=float, default=0.44, help="M threshold")
@click.option('--b_threshold', type=float, default=0.70, help="B threshold")
@click.option('--max_steps', type=int, default=1)
def run(grid_file, r, m_threshold, b_threshold, max_steps):
    '''
    Put it all together: do the simulation and process the results.
    '''

    if grid_file is None:
        print("No parameters specified...just loading the code")
        return

    grid = utility.read_grid(grid_file)

    if len(grid) < 20:
        print("Initial state of city:")
        for row in grid:
            print(row)
        print()

    opens = utility.find_opens(grid)
    num_relocations = do_simulation(grid, r, m_threshold, b_threshold,
                                    max_steps, opens)
    print("Number of relocations done: " + str(num_relocations))

    if len(grid) < 20:
        print()
        print("Final state of the city:")
        for row in grid:
            print(row)

if __name__ == "__main__":
    run() # pylint: disable=no-value-for-parameter
