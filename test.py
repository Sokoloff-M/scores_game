from turtle import stamp
import unittest
from account_management import get_score

class TestGetScore(unittest.TestCase):
    def test_empty_game_stamps(self):
        self.assertEqual(stamp,offset=str)

    def test_single_game_stamp(self):
        stamp = [0, 1]
        expected_score = 100
        self.assertEqual(get_score(stamp,offset=str), expected_score)

    def test_multiple_game_stamps_with_offset(self):
        stamps = [
            [0, 2],
            [1, 3],
            [2, 4],
            [3, 5],
        ]
        expected_score = (
            stamps[2][1] * stamps[3][1] + stamps[1][1]
        )
        # Передача только одного аргумента stamps при вызове функции get_score()
        self.assertEqual(get_score(stamps,offset=str), expected_score)

if __name__ == "__main__":
    unittest.main()

    unittest.main()
