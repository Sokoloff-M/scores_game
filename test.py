import unittest
from account_management import get_score

class TestGetScore(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.game_stamps = [
            {"offset": 0, "score": {"home": 1, "away": 2}},
            {"offset": 1, "score": {"home": 3, "away": 4}},
            {"offset": 2, "score": {"home": 5, "away": 6}}
        ]

    def test_get_score_with_offset_zero(self):
        # Проверяем функцию get_score() при смещении (offset) равном нулю
        expected_score = {"home": 9, "away": 12}
        self.assertEqual(get_score(self.game_stamps, 0), expected_score)

    def test_get_score_with_positive_offset(self):
        # Проверяем функцию get_score() при положительном смещении (offset)
        expected_score = {"home": 8, "away": 10}
        self.assertEqual(get_score(self.game_stamps, 1), expected_score)

    def test_get_score_with_large_positive_offset(self):
        # Проверяем функцию get_score() при большом положительном смещении (offset)
        expected_score = {"home": 5, "away": 6}
        self.assertEqual(get_score(self.game_stamps, 2), expected_score)

    def test_get_score_with_negative_offset(self):
        # Проверяем функцию get_score() при отрицательном смещении (offset)
        expected_score = {"home": 15, "away": 18}
        self.assertEqual(get_score(self.game_stamps, -1), expected_score)

    def test_get_score_with_zero_offset_for_empty_game_stamps(self):
        # Проверяем функцию get_score() при смещении (offset) равном нулю для пустого списка game_stamps
        empty_game_stamps = []
        expected_score = {"home": 0, "away": 0}
        self.assertEqual(get_score(empty_game_stamps, 0), expected_score)

    def test_get_score_with_large_negative_offset(self):
        # Проверяем функцию get_score() при большом отрицательном смещении (offset)
        expected_score = {"home": 0, "away": 0}
        self.assertEqual(get_score(self.game_stamps, -100), expected_score)

if __name__ == "__main__":
    unittest.main()
