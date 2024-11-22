class GameOfLife(object):
    """
    Class for the Game of Life
    """
    def __init__(self, ocean: list[list[int]]) -> None: # Initialize the ocean attribute in__init__

        """
       Initializes the Game of Life with the initial ocean state.
       :param ocean: A 2D list representing the initial state of the ocean.
                     0 = empty cell, 1 = rock, 2 = fish, 3 = shrimp.
        """
        self.ocean = ocean
        self.rows = len(ocean)
        self.cols = len(ocean[0]) if ocean else 0

    def _get_neighbours(self, i: int, j: int) -> list[tuple[int, int]]:
        """
        Returns the coordinates of all valid neighbouring cells.
        :param i: Row index of the current cell.
        :param j: Column index of the current cell.
        :return: A list of tuples representing the coordinates of valid neighbours.
        """
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),
            (1, -1), (1, 0), (1, 1)
        ]
        neighbours = []
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.rows and 0 <= nj < self.cols:
                neighbours.append((ni, nj))
        return neighbours

    def _count_neighbours(self, i: int, j: int, value: int) -> int:
        """
        Counts the number of neighbors of a specific type (fish or shrimp) around a given cell.
        :param i: Row index of the current cell
        :param j: Column index of the current cell
        :param value: The type of cell to count (2 for fish, 3 for shrimp)
        :return: The number of neighbors matching the given type
        """
        neighbour_count = 0

        # Iterate over the 8 neighboring cells around (i, j)
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                # Check if the neighbor is within bounds
                if 0 <= x < self.rows and 0 <= y < self.cols:
                    # Check if it's not the current cell and matches the given value (fish or shrimp)
                    if (x != i or y != j) and self.ocean[x][y] == value:
                        neighbour_count += 1

        return neighbour_count

    def get_next_generation(self) -> list[list[int]]:
        """
        Calculates the next generation of the ocean state based on the rules of the game.
        :return: A 2D list representing the next generation of the ocean.
        """
        # Create a new ocean grid for the next generation
        new_ocean = [[0] * self.cols for _ in range(self.rows)]

        # Iterate through each cell of the ocean grid
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.ocean[i][j]  # Get the current cell value
                fish_count = self._count_neighbours(i, j, value=2)  # Count fish neighbors
                shrimp_count = self._count_neighbours(i, j, value=3)  # Count shrimp neighbors

                # Debug: print the current state
                print(f"Cell ({i}, {j}): Current={cell}, FishCount={fish_count}, ShrimpCount={shrimp_count}")

                # Apply rules for different cell types
                if cell == 1:  # Rock stays unchanged
                    new_ocean[i][j] = 1
                elif cell == 2:  # Fish rules
                    if fish_count < 2 or fish_count >= 4:
                        new_ocean[i][j] = 0  # Fish dies
                    else:
                        new_ocean[i][j] = 2  # Fish survives
                elif cell == 3:  # Shrimp rules
                    if shrimp_count < 2 or shrimp_count >= 4:
                        new_ocean[i][j] = 0  # Shrimp dies
                    else:
                        new_ocean[i][j] = 3  # Shrimp survives
                elif cell == 0:  # Empty cell rules
                    if fish_count == 3:
                        new_ocean[i][j] = 2  # New fish born
                    elif shrimp_count == 3:
                        new_ocean[i][j] = 3  # New shrimp born

                # Debug: print the new value of the cell
                print(f"New Cell ({i}, {j}): NewValue={new_ocean[i][j]}")

        # Debug: print the next generation ocean
        print("Next Generation:")
        for row in new_ocean:
            print(row)

        # Update the ocean to the new generation and return it
        self.ocean = new_ocean
        return self.ocean
