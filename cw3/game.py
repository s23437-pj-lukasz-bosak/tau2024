import random

def generate_board():
    board = [['_' for _ in range(5)] for _ in range(5)]  # Tworzenie pustej tablicy 5x5

    # Wybór losowego miejsca dla punktu startowego
    start_row = random.randint(0, 4)
    start_col = random.choice([0, 4])  # Punkt startowy jest na brzegu tablicy
    board[start_row][start_col] = 'S'  # Oznaczenie punktu startowego jako 'S'

    # Wybór losowego miejsca dla punktu końcowego
    end_row = random.choice([0, 4])  # Punkt końcowy jest na brzegu tablicy
    end_col = random.randint(0, 4)
    while board[end_row][end_col] != '_':
        end_row = random.choice([0, 4])
        end_col = random.randint(0, 4)
    board[end_row][end_col] = 'E'  # Oznaczenie punktu końcowego jako 'E'

    # Dodanie trzech przeszkód na losowych miejscach
    obstacles = 0
    while obstacles < 3:
        obstacle_row = random.randint(0, 4)
        obstacle_col = random.randint(0, 4)
        if board[obstacle_row][obstacle_col] == '_':
            board[obstacle_row][obstacle_col] = 'X'  # Oznaczenie przeszkody jako 'X'
            obstacles += 1

    return board, start_row, start_col, end_row, end_col

def print_board(board):
    for row in board:
        print(' '.join(row))

def move_player(board, direction, current_row, current_col, start_row, start_col):
    new_row, new_col = current_row, current_col

    # Aktualizacja pozycji gracza na podstawie wybranej ścieżki
    if direction == 'w' and current_row > 0:
        new_row -= 1
    elif direction == 's' and current_row < len(board) - 1:
        new_row += 1
    elif direction == 'a' and current_col > 0:
        new_col -= 1
    elif direction == 'd' and current_col < len(board[0]) - 1:
        new_col += 1

    if board[new_row][new_col] != 'X':  # Sprawdzenie czy ruch jest możliwy (nie ma przeszkody)
        if board[new_row][new_col] != 'E':  # Jeśli nowa pozycja nie jest punktem końcowym
            board[current_row][current_col] = '_'  # Stara pozycja gracza staje się pustym polem
        else:
            board[current_row][current_col] = 'E'  # Oznaczenie punktu końcowego na planszy
        board[new_row][new_col] = '#'  # Nowa pozycja gracza oznaczona jako '#'

        return new_row, new_col, start_row, start_col
    else:
        print("Nie można tam przejść. Jest przeszkoda!")
        return current_row, current_col, start_row, start_col  # Gracz pozostaje w obecnej pozycji

def main():
    # Generowanie tablicy i wyświetlenie jej oraz punktów startu, końca i przeszkód
    game_board, player_row, player_col, end_row, end_col = generate_board()

    # Zachowanie początkowej pozycji gracza
    start_row, start_col = player_row, player_col

    # Główna pętla gry
    while True:
        print("\nAktualna plansza:")
        print_board(game_board)
        move = input("Podaj kierunek ruchu (W - góra, S - dół, A - lewo, D - prawo): ").lower()

        if move in ['w', 's', 'a', 'd']:
            player_row, player_col, start_row, start_col = move_player(game_board, move, player_row, player_col, start_row, start_col)
            if player_row == end_row and player_col == end_col:
                game_board[player_row][player_col] = '#'  # Oznaczenie punktu końcowego na planszy
                print("\nAktualna plansza:")
                print_board(game_board)
                print("Gratulacje! Dotarłeś do punktu końcowego!")
                break
            else:
                game_board[start_row][start_col] = 'S'  # Przywrócenie pozycji startowej na planszy
        else:
            print("Nieprawidłowy kierunek. Podaj poprawny ruch.")

if __name__ == "__main__":
    main()  # Uruchamianie gry