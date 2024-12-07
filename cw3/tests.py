import unittest
from io import StringIO
from unittest.mock import patch
from game import generate_board, print_board, move_player

class TestGame(unittest.TestCase):

    def test_obstacle_count(self):
        # Utwórz planszę za pomocą funkcji generate_board()
        game_board, _, _, _, _ = generate_board()
        # Zlicz ilość przeszkód na planszy
        obstacle_count = sum(row.count('X') for row in game_board)
        # Sprawdź, czy liczba przeszkód jest równa 3
        self.assertEqual(obstacle_count, 3, "Liczba przeszkód na planszy powinna być równa 3")

    def test_collision_message(self):
        game_board, player_row, player_col, _, _ = generate_board()

        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Umieść przeszkodę na kolejnej pozycji gracza
            while True:
                next_row = player_row + 1
                next_col = player_col
                if next_row < len(game_board) and game_board[next_row][next_col] != 'X':
                    game_board[next_row][next_col] = 'X'
                    break
                else:
                    player_row = (player_row + 1) % len(game_board)

            # Zapamiętaj oryginalny stan planszy jako string
            original_board_str = '\n'.join([' '.join(row) for row in game_board])

            # Wykonaj ruch gracza na przeszkodę
            move_player(game_board, 's', player_row, player_col, player_row, player_col)
            expected_output = "Nie można tam przejść. Jest przeszkoda!\n"

            self.assertEqual(fake_out.getvalue(), expected_output, "Komunikat o kolizji z przeszkodą nie został wyświetlony")

            # Porównaj plansze jako stringi-powinny byc takie same
            updated_board_str = '\n'.join([' '.join(row) for row in game_board])
            self.assertEqual(updated_board_str, original_board_str, "Plansza została zmodyfikowana po kolizji z przeszkodą")

    def test_start_point_on_edge(self):
        _, start_row, start_col, _, _ = generate_board()
        board_size = 5  # Rozmiar planszy (5x5)

        # Sprawdzenie czy punkt startowy jest na brzegu planszy
        is_on_edge = start_row == 0 or start_row == board_size - 1 or start_col == 0 or start_col == board_size - 1
        self.assertTrue(is_on_edge, "Punkt startowy 'S' powinien być na brzegu planszy")

    def test_end_point_on_edge(self):
        _, _, _, end_row, end_col = generate_board()
        board_size = 5  # Rozmiar planszy (5x5)

        # Sprawdzenie czy punkt końcowy jest na brzegu planszy
        is_on_edge = end_row == 0 or end_row == board_size - 1 or end_col == 0 or end_col == board_size - 1
        self.assertTrue(is_on_edge, "Punkt końcowy 'E' powinien być na brzegu planszy")

    def test_player_movement_boundary_top(self):
        game_board, player_row, player_col, _, _ = generate_board()
        print("Test: test_player_movement_boundary_top")
        board_size = 5  # Rozmiar planszy (5x5)
        target_row = 0

        # Szukanie pierwszego wolnego pola na górnym brzegu planszy
        for col in range(board_size - 1):
            if game_board[target_row][col] == '_':
                new_row, new_col, _, _ = move_player(game_board, 'w', target_row, col, target_row, col)
                print_board(game_board)
                self.assertEqual(new_col, col, "Gracz nie powinien móc wyjść poza dolny brzeg planszy")
                break


    def test_player_movement_boundary_bottom(self):
        game_board, player_row, player_col, _, _ = generate_board()
        print("Test: test_player_movement_boundary_bottom")
        board_size = 5  # Rozmiar planszy (5x5)
        target_row = 4

        # Szukanie pierwszego wolnego pola na dolnym brzegu planszy
        for col in range(board_size-1):
            if game_board[target_row][col] == '_':
                new_row, new_col, _, _ = move_player(game_board, 's', target_row, col, target_row, col)
                print_board(game_board)
                self.assertEqual(new_col, col, "Gracz nie powinien móc wyjść poza dolny brzeg planszy")
                break

    def test_player_movement_boundary_left(self):
        game_board, player_row, player_col, _, _ = generate_board()
        print("Test: test_player_movement_boundary_left")
        board_size = 5  # Rozmiar planszy (5x5)
        target_col = 0

        # Szukanie pierwszego wolnego pola na dolnym brzegu planszy
        for row in range(board_size - 1):
            if game_board[target_col][row] == '_':
                new_row, new_col, _, _ = move_player(game_board, 'a', row, target_col, row, target_col)
                print_board(game_board)
                self.assertEqual(new_row, row, "Gracz nie powinien móc wyjść poza lewy brzeg planszy")
                break


    def test_player_movement_boundary_right(self):
        game_board, player_row, player_col, _, _ = generate_board()
        print("Test: test_player_movement_boundary_right")
        board_size = 5  # Rozmiar planszy (5x5)
        target_col = 4

        # Szukanie pierwszego wolnego pola na dolnym brzegu planszy
        for row in range(board_size - 1):
            if game_board[target_col][row] == '_':
                new_row, new_col, _, _ = move_player(game_board, 'd', row, target_col, row, target_col)
                print_board(game_board)
                self.assertEqual(new_row, row, "Gracz nie powinien móc wyjść poza lewy brzeg planszy")
                break

    def test_invalid_movement_direction(self):
        game_board, player_row, player_col, _, _ = generate_board()

        # Sprawdź, czy podanie nieprawidłowego kierunku nie zmienia pozycji gracza
        new_row, new_col = move_player(game_board, 'x', player_row, player_col, player_row, player_col)[0:2]
        self.assertEqual((new_row, new_col), (player_row, player_col), "Nieprawidłowy kierunek ruchu nie powinien zmieniać pozycji gracza")

    def test_movement_without_obstacles_up(self):
        game_board, player_row, player_col, _, _ = generate_board()

        # Ustaw gracza w centrum planszy
        game_board[player_row][player_col] = '_'
        player_row, player_col = 2, 2

        # Ustaw pola wokół gracza na puste pola
        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                new_row = player_row + row_offset
                new_col = player_col + col_offset
                if 0 <= new_row < 5 and 0 <= new_col < 5:
                    game_board[new_row][new_col] = '_'

        # Sprawdź ruch gracza w górę (w)
        new_row, new_col = move_player(game_board, 'w', player_row, player_col, player_row, player_col)[0:2]
        self.assertEqual((new_row, new_col), (player_row - 1, player_col), "Gracz powinien móc poruszać się w górę")

    def test_movement_without_obstacles_down(self):
        game_board, player_row, player_col, _, _ = generate_board()

        # Ustaw gracza w centrum planszy
        game_board[player_row][player_col] = '_'
        player_row, player_col = 2, 2

        # Ustaw pola wokół gracza na puste pola
        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                new_row = player_row + row_offset
                new_col = player_col + col_offset
                if 0 <= new_row < 5 and 0 <= new_col < 5:
                    game_board[new_row][new_col] = '_'

        # Sprawdź ruch gracza w dół (s)
        new_row, new_col = move_player(game_board, 's', player_row, player_col, player_row, player_col)[0:2]
        self.assertEqual((new_row, new_col), (player_row + 1, player_col), "Gracz powinien móc poruszać się w dół")

    def test_movement_without_obstacles_left(self):
        game_board, player_row, player_col, _, _ = generate_board()

        # Ustaw gracza w centrum planszy
        game_board[player_row][player_col] = '_'
        player_row, player_col = 2, 2

        # Ustaw pola wokół gracza na puste pola
        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                new_row = player_row + row_offset
                new_col = player_col + col_offset
                if 0 <= new_row < 5 and 0 <= new_col < 5:
                    game_board[new_row][new_col] = '_'

        # Sprawdź ruch gracza w lewo (a)
        new_row, new_col = move_player(game_board, 'a', player_row, player_col, player_row, player_col)[0:2]
        self.assertEqual((new_row, new_col), (player_row, player_col - 1), "Gracz powinien móc poruszać się w lewo")

    def test_movement_without_obstacles_right(self):
        game_board, player_row, player_col, _, _ = generate_board()

        # Ustaw gracza w centrum planszy
        game_board[player_row][player_col] = '_'
        player_row, player_col = 2, 2

        # Ustaw pola wokół gracza na puste pola
        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                new_row = player_row + row_offset
                new_col = player_col + col_offset
                if 0 <= new_row < 5 and 0 <= new_col < 5:
                    game_board[new_row][new_col] = '_'

        # Sprawdź ruch gracza w prawo (d)
        new_row, new_col = move_player(game_board, 'd', player_row, player_col, player_row, player_col)[0:2]
        self.assertEqual((new_row, new_col), (player_row, player_col + 1), "Gracz powinien móc poruszać się w prawo")

if __name__ == "__main__":
    unittest.main()