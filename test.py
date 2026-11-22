import unittest
from unittest.mock import patch

from logic import GameState


class GameStateTests(unittest.TestCase):
    def setUp(self):
        self.game = GameState()

    def test_board_sizes(self):
        self.assertEqual(self.game.size, 5)

        for size in (3, 5, 7):
            game = GameState(size)
            self.assertEqual(len(game.grid), size)
            for row in game.grid:
                self.assertEqual(len(row), size)
                for light in row:
                    self.assertFalse(light)
            self.assertEqual(game.moves_made, 0)

            game.generate_board()
            solution_move_count = 0
            for row in game.solution:
                for move in row:
                    if move:
                        solution_move_count += 1
            self.assertEqual(solution_move_count, size + 1)

    def test_press(self):
        self.game.press(2, 2)

        expected_lights = {(2, 2), (2, 1), (2, 3), (1, 2), (3, 2)}
        actual_lights = set()
        for row in range(self.game.size):
            for col in range(self.game.size):
                if self.game.grid[row][col]:
                    actual_lights.add((row, col))

        self.assertEqual(actual_lights, expected_lights)
        self.assertEqual(self.game.moves_made, 1)

    def test_flip_bounds(self):
        self.game.press(0, 0)
        self.game.flip(-1, 0)
        self.game.flip(0, self.game.size)

        actual_lights = set()
        for row in range(self.game.size):
            for col in range(self.game.size):
                if self.game.grid[row][col]:
                    actual_lights.add((row, col))

        self.assertEqual(actual_lights, {(0, 0), (0, 1), (1, 0)})

    def test_undo(self):
        self.game.press(1, 3)
        self.game.press(1, 3)
        self.assertTrue(self.game.is_solved())
        self.assertEqual(self.game.moves_made, 2)

        self.game.undo()
        self.assertFalse(self.game.is_solved())
        self.assertEqual(self.game.moves_made, 1)
        self.assertEqual(self.game.move_history, [(1, 3)])
        self.assertTrue(self.game.solution[1][3])

        self.game.undo()
        self.assertTrue(self.game.is_solved())
        self.assertEqual(self.game.moves_made, 0)
        self.assertEqual(self.game.move_history, [])
        self.assertFalse(self.game.solution[1][3])

        self.game.undo()
        self.assertTrue(self.game.is_solved())
        self.assertEqual(self.game.moves_made, 0)

    def test_generated_puzzle(self):
        moves = [(0, 0), (2, 2), (4, 1)]
        with patch("logic.random.sample", return_value=moves):
            self.game.generate_board(num_moves=len(moves))

        starting_grid = []
        starting_solution = []
        for row in self.game.grid:
            starting_grid.append(row[:])
        for row in self.game.solution:
            starting_solution.append(row[:])

        self.assertEqual(self.game.initial_grid, starting_grid)
        self.assertEqual(self.game.moves_made, 0)
        self.assertEqual(self.game.move_history, [])
        self.assertIn(self.game.hint(), moves)

        for row, col in moves:
            self.game.press(row, col)

        self.assertTrue(self.game.is_solved())
        self.game.reset_puzzle()
        self.assertEqual(self.game.grid, starting_grid)
        self.assertEqual(self.game.solution, starting_solution)
        self.assertEqual(self.game.moves_made, 0)
        self.assertEqual(self.game.move_history, [])

    def test_hint_empty(self):
        self.assertIsNone(self.game.hint())


if __name__ == "__main__":
    unittest.main(verbosity=2)
