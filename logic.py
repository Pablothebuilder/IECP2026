import random

class GameState:
    def __init__(self, size=5):
        self.size = size
        self.grid = []
        self.initial_grid = []
        self.solution = []
        self.initial_solution = []
        self.moves_made = 0
        self.move_history = []
        self.reset()

    def reset(self):
        self.grid = []
        self.initial_grid = []
        self.solution = []
        self.initial_solution = []
        self.move_history = []

        for row in range(self.size):
            grid_row = []
            initial_grid_row = []
            solution_row = []
            initial_solution_row = []

            for col in range(self.size):
                grid_row.append(False)
                initial_grid_row.append(False)
                solution_row.append(False)
                initial_solution_row.append(False)

            self.grid.append(grid_row)
            self.initial_grid.append(initial_grid_row)
            self.solution.append(solution_row)
            self.initial_solution.append(initial_solution_row)

        self.moves_made = 0

    def reset_puzzle(self):
        self.moves_made = 0
        self.move_history = []
        for row in range(self.size):
            for col in range(self.size):
                self.grid[row][col] = self.initial_grid[row][col]
                self.solution[row][col] = self.initial_solution[row][col]

    def press(self, row, col, record_move=True):
        self.flip(row, col)
        self.flip(row, col - 1)
        self.flip(row, col + 1)
        self.flip(row - 1, col)
        self.flip(row + 1, col)

        if record_move:
            self.moves_made += 1
            self.move_history.append((row, col))
            self.solution[row][col] = not self.solution[row][col]

    def undo(self):
        if len(self.move_history) > 0:
            row, col = self.move_history.pop()
            self.press(row, col, record_move=False)
            self.moves_made -= 1
            self.solution[row][col] = not self.solution[row][col]

    def flip(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            self.grid[row][col] = not self.grid[row][col]

    def generate_board(self, num_moves=None):
        self.reset()

        if num_moves is None:
            num_moves = self.size + 1

        all_positions = []
        for row in range(self.size):
            for col in range(self.size):
                all_positions.append((row, col))

        chosen_moves = random.sample(all_positions, num_moves)

        for row, col in chosen_moves:
            self.press(row, col, record_move=False)
            self.solution[row][col] = True

        for row in range(self.size):
            for col in range(self.size):
                self.initial_grid[row][col] = self.grid[row][col]
                self.initial_solution[row][col] = self.solution[row][col]

    def is_solved(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == True:
                    return False
        return True

    def hint(self):
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.solution[row][col] == True:
                    valid_moves.append((row, col))

        if len(valid_moves) == 0:
            return None

        return random.choice(valid_moves)