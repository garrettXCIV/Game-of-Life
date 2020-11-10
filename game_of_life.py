from random import getrandbits
from time import sleep

def main():
    print("Conway's Game of Life\n\n")

    grid = Grid()
    # Print initial state
    grid.print()


    if grid.iterations == '':
        while True:
            grid.run_generation()
            if grid.final_state():
                break
            grid.print()
            sleep(.008)
    else:
        for i in range(grid.iterations):
            grid.run_generation()
            if grid.final_state():
                break
            grid.print()
            sleep(.008)

    print('Final cell state reached.')


class Cell:
    def __init__(self):
        self.state = 'dead'
        self.char = '□'

    def set_alive(self):
        self.state = 'alive'
        self.char = '■'

    def set_dead(self):
        self.state = 'dead'
        self.char = '□'

    def is_alive(self):
        if self.state == 'alive':
            return True
        return False


class Grid:
    def __init__(self, preset=None):
        # Set grid length
        while True:
            try:
                self.length = int(input("Choose grid length (min 3): "))
                if self.length < 3:
                    continue
                break
            except ValueError:
                print("Grid length must be an integer > 3.")

        # Set grid width
        while True:
            try:
                self.width = int(input("Choose grid width (min 3): "))
                if self.width < 3:
                    continue
                break
            except ValueError:
                print("Grid width must be an integer > 3.")

        self.grid = [[Cell() for x in range(self.length)] for y in range(self.width)]

        while True:
            try:
                self.iterations = input('Enter total iterations or leave blank to run infinitely: ')
                if self.iterations == '':
                    break
                if int(self.iterations) < 1:
                    print('Iterations must be greater than 1.')
                    continue
                self.iterations = int(self.iterations)
                break
            except ValueError:
                print('Iterations must be an integer or left blank.')


        self.prev_grid_state = None
        self.grid_state = None

        # Check if user wants to set cells randomly
        while True:
            randomize_cells = input(
                "Choose cells randomly? (Y/N)"
                ).upper()
            if randomize_cells == 'Y':
                randomize_cells = True
                break
            if randomize_cells == 'N':
                randomize_cells = False
                break
            print('Invalid choice.')


        if randomize_cells:
        # Loop through cells, setting them randomly
            for x in range(self.length):
                for y in range(self.width):
                    cell_alive = getrandbits(1)
                    if cell_alive:
                        self.grid[x][y].set_alive()
                    else:
                        self.grid[x][y].set_dead()
        else:
            cells_input = None
            while True:
                try:
                    raw_cells_input = input('Enter comma separated sets of cells to mark alive, '
                                            'e.g. "(1, 1), (1, 2), (1, 3)": ')

                    # Convert input to list of cell coordinates
                    cells_input = raw_cells_input.replace('(', '').split('), ')
                    cells_input = [cell.replace(')', '').split(', ') for cell in cells_input]

                    # Convert all values in list to ints
                    for i in range(len(cells_input)):
                        cells_input[i][0] = int(cells_input[i][0]) - 1
                        cells_input[i][1] = int(cells_input[i][1]) - 1

                    # Check that list is valid
                    for x, y in cells_input:
                        if x not in range(self.length) or y not in range(self.width):
                            raise ValueError

                except Exception as e:
                    print(f'{e}: Invalid input.')
                    continue

                break

            for x, y in cells_input:
                self.grid[x][y].set_alive()


    def check_neighbors(self):
        """Check the 8 cells surrounding each cell to tally living neighbors"""
        dying_cells = []
        new_cells = []
        for x in range(self.length):
            for y in range(self.width):
                # Check cell for living neighbors
                neighbor_tally = 0
                # Check top left
                if x > 0 and y > 0:
                    if self.grid[x - 1][y - 1].is_alive():
                        neighbor_tally += 1
                # Check top
                if x > 0:
                    if self.grid[x - 1][y].is_alive():
                        neighbor_tally += 1
                # Check top right
                if x > 0 and y < self.width - 1:
                    if self.grid[x - 1][y + 1].is_alive():
                        neighbor_tally += 1
                # Check left
                if y > 0:
                    if self.grid[x][y - 1].is_alive():
                        neighbor_tally += 1
                # Check right
                if y < self.width - 1:
                    if self.grid[x][y + 1].is_alive():
                        neighbor_tally += 1
                # Check bottom left
                if x < self.length - 1 and y > 0:
                    if self.grid[x + 1][y - 1].is_alive():
                        neighbor_tally += 1
                # Check bottom
                if x < self.length - 1:
                    if self.grid[x + 1][y].is_alive():
                        neighbor_tally += 1
                # Check bottom right
                if x < self.length - 1 and y < self.width - 1:
                    if self.grid[x + 1][y + 1].is_alive():
                        neighbor_tally += 1


                # Make cell live if currently dead with 3 living neighbors
                if not self.grid[x][y].is_alive() and neighbor_tally == 3:
                    new_cells.append(self.grid[x][y])
                # Add cell to dying cells list if live neighbors != 2 or 3
                if self.grid[x][y].is_alive() and neighbor_tally not in {2, 3}:
                    dying_cells.append(self.grid[x][y])

        return dying_cells, new_cells

    def run_generation(self):
        """Run a single generation simulation."""
        dying_cells, new_cells = self.check_neighbors()

        # Mark dying cells as dead at end of gen/iteration
        for cell in dying_cells:
            cell.set_dead()

        for cell in new_cells:
            cell.set_alive()

    def print(self):
        """Print grid."""
        board = '\n' * 20
        for x in range(self.length):
            for y in range(self.width):
                if y < self.width - 1:
                    board = f'{board}{self.grid[x][y].char} '
                else:
                    board = f'{board}{self.grid[x][y].char}\n'
        print(board)

    def final_state(self):
        """Check if any cells are still alive."""
        self.grid_state = [[self.grid[x][y].is_alive() for x in range(self.length)] for y in range(self.width)]
        if self.prev_grid_state == self.grid_state and self.prev_grid_state:
            return True
        self.prev_grid_state = self.grid_state
        return False


if __name__ == '__main__':
    main()
