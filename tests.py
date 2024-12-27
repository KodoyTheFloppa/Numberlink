import unittest
from solver import solve_puzzle


class TestSolver(unittest.TestCase):
    def test_solve_simple_puzzle(self):
        rows, cols = 3, 3
        grid_numbers = [
            [1, 0, 2],
            [0, 0, 0],
            [1, 0, 2]
        ]
        walls = {}
        solution = solve_puzzle(rows, cols, grid_numbers, walls)
        self.assertIsNotNone(solution)
        self.assertIn(1, solution)
        self.assertIn(2, solution)
        self.assertEqual(len(solution[1]), 3)
        self.assertEqual(len(solution[2]), 3)

    def test_unsolvable_puzzle_due_to_walls(self):
        rows, cols = 2, 2
        grid_numbers = [
            [1, 0],
            [0, 1]
        ]
        walls = {
            ((0, 0), (0, 1)): True,
            ((0, 0), (1, 0)): True,
            ((1, 0), (1, 1)): True,
            ((0, 1), (1, 1)): True
        }
        solution = solve_puzzle(rows, cols, grid_numbers, walls)
        self.assertIsNone(solution)

    def test_invalid_number_pairs(self):
        rows, cols = 2, 2
        grid_numbers = [
            [1, 1],
            [1, 0]
        ]
        walls = {}
        solution = solve_puzzle(rows, cols, grid_numbers, walls)
        self.assertIsNone(solution)  # More than two instances of number 1

    def test_solve_normal_puzzle(self):
        rows, cols = 5, 5
        grid_numbers = [
            [1, 0, 2, 0, 0],
            [0, 0, 1, 0, 0],
            [2, 0, 0, 0, 0],
            [3, 0, 0, 0, 0],
            [0, 0, 0, 0, 3]
        ]
        walls = {}
        solution = solve_puzzle(rows, cols, grid_numbers, walls)
        self.assertIsNotNone(solution)
        self.assertIn(1, solution)
        self.assertIn(2, solution)
        self.assertIn(3, solution)
        self.assertEqual(len(solution[1]), 4)
        self.assertEqual(len(solution[2]), 7)
        self.assertEqual(len(solution[3]), 6)

    def test_solve_hard_puzzle(self):
        rows, cols = 7, 7
        grid_numbers = [
            [0, 0, 0, 4, 0, 0, 0],
            [0, 3, 0, 0, 2, 5, 0],
            [0, 0, 0, 3, 1, 0, 0],
            [0, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [2, 0, 0, 0, 4, 0, 0],
        ]
        walls = {}
        solution = solve_puzzle(rows, cols, grid_numbers, walls)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution[1]), 6)
        self.assertEqual(len(solution[2]), 12)
        self.assertEqual(len(solution[3]), 4)
        self.assertEqual(len(solution[4]), 12)
        self.assertEqual(len(solution[5]), 15)


if __name__ == '__main__':
    unittest.main()
