from copy import deepcopy

def parse_board(input_str: str) -> list:
    return [list(row) for row in input_str.split('\n')]

def open_board(filename: str = "board.txt") -> list:
    with open(filename, 'r') as f:
        return parse_board(f.read())
    
def calculate_all_moves(board: list, colour: str = "white"):
    possible_moves = []
    for y in range(5):
        for x in range(5):
            possible_moves.extend(calculate_one_piece_moves(board, x, y, colour))
    return possible_moves

def calculate_one_piece_moves(board: list, x_pos: int, y_pos: int, colour: str):
    possible_moves = []

    if colour == "white" and board[y_pos][x_pos].islower():
        if board[y_pos][x_pos] == 'p':
            possible_moves.extend(calculate_pawn_moves(board, x_pos, y_pos, colour))
        elif board[y_pos][x_pos] in ('b', 'r', 'q'):
            possible_moves.extend(calculate_slider_moves(board, x_pos, y_pos, colour))
        elif board[y_pos][x_pos] in ('n', 'k'):
            possible_moves.extend(calculate_king_or_knight_moves(board, x_pos, y_pos, colour))
    elif colour == "black" and board[y_pos][x_pos].isupper():
        if board[y_pos][x_pos] == 'P':
            possible_moves.extend(calculate_pawn_moves(board, x_pos, y_pos, colour))
        elif board[y_pos][x_pos] in ('B', 'R', 'Q'):
            possible_moves.extend(calculate_slider_moves(board, x_pos, y_pos, colour))
        elif board[y_pos][x_pos] in ('N', 'K'):
            possible_moves.extend(calculate_king_or_knight_moves(board, x_pos, y_pos, colour))

    return possible_moves

def calculate_pawn_moves(board: list, x_pos: int, y_pos: int, colour: str):
    possible_moves = []

    if colour == "white" and y_pos != 0:
        if board[y_pos-1][x_pos] == '0':
            possible_moves.append((x_pos, y_pos, x_pos, y_pos-1))
        if x_pos != 0:
            if board[y_pos-1][x_pos-1].isupper():
                possible_moves.append((x_pos, y_pos, x_pos-1, y_pos-1))
        if x_pos != 4:
            if board[y_pos-1][x_pos+1].isupper():
                possible_moves.append((x_pos, y_pos, x_pos+1, y_pos-1))
    
    elif colour == "black" and y_pos != 4:
        if board[y_pos+1][x_pos] == '0':
            possible_moves.append((x_pos, y_pos, x_pos, y_pos-1))
        if x_pos != 0:
            if board[y_pos+1][x_pos-1].islower():
                possible_moves.append((x_pos, y_pos, x_pos-1, y_pos+1))
        if x_pos != 4:
            if board[y_pos+1][x_pos+1].islower():
                possible_moves.append((x_pos, y_pos, x_pos+1, y_pos+1))

    return possible_moves

def calculate_king_or_knight_moves(board: list, x_pos: int, y_pos: int, colour: str):
    king_moves = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    knight_moves = [(2, 1), (1, 2), (2, -1), (-1, 2), (1, -2), (-2, 1), (-1, -2), (-2, -1)]
    possible_moves = []

    if board[y_pos][x_pos] in ('k', 'K'):
        moves = king_moves
    else:
        moves = knight_moves

    for move in moves:
        x_check = x_pos + move[0]
        y_check = y_pos + move[1]

        if 0 <= x_check <= 4 and 0 <= y_check <= 4:
            if board[y_check][x_check] == '0':
                possible_moves.append((x_pos, y_pos, x_check, y_check))
            elif (colour == "white" and board[y_check][x_check].isupper()) or (colour == "black" and board[y_check][x_check].islower()):
                possible_moves.append((x_pos, y_pos, x_check, y_check))
    return possible_moves

def calculate_slider_moves(board: list, x_pos: int, y_pos: int, colour: str):
    rook_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    bishop_directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    possible_moves = []

    if board[y_pos][x_pos] in ('b', 'B'):
        directions = bishop_directions
    elif board[y_pos][x_pos] in ('r', 'R'):
        directions = rook_directions
    else:
        directions = rook_directions + bishop_directions

    for direction in directions:
        x_check = x_pos
        y_check = y_pos

        while True:
            x_check += direction[0]
            y_check += direction[1]
            if 0 <= x_check <= 4 and 0 <= y_check <= 4:
                if board[y_check][x_check] == '0':
                    possible_moves.append((x_pos, y_pos, x_check, y_check))
                    continue
                elif (colour == "white" and board[y_check][x_check].isupper()) or (colour == "black" and board[y_check][x_check].islower()):
                    possible_moves.append((x_pos, y_pos, x_check, y_check))
                    break
                elif (colour == "white" and board[y_check][x_check].islower()) or (colour == "black" and board[y_check][x_check].isupper()):
                    break
                else: 
                    break
            else:
                break
    
    return possible_moves

def print_board(board: list) -> None:
    print("\n".join([''.join(row) for row in board]))

def check_check(board: list, colour: str) -> bool:
    for move in calculate_all_moves(board, colour = "black" if colour == "white" else "white"):
        if board[move[3]][move[2]] == ('k' if colour == "white" else 'K'):
            return True
    return False
    
def make_move(board: list, move: tuple) -> bool:
    new_board = deepcopy(board)
    new_board[move[3]][move[2]] = new_board[move[1]][move[0]]
    new_board[move[1]][move[0]] = '0'
    return new_board


def filter_possible_moves(board: list, moves: list, colour: str) -> list:
    return list(filter(lambda move: not check_check(make_move(board, move), colour), moves))

if __name__ == "__main__":
    piece_names = {'k': 'King', 'q': 'Queen', 'n': 'Knight', 'r': 'Rook', 'b': 'Bishop', 'p': 'Pawn'}

    board = open_board()
    print_board(board)
    all_moves = calculate_all_moves(board, "white")
    filtered_moves = filter_possible_moves(board, all_moves, "white")

    check_possible = False
    for move in filtered_moves:
        if check_check(make_move(board, move), "black"):
            check_possible = True
            print(f"If you move the {piece_names[board[move[1]][move[0]].lower()]} on position ({move[0]+1}, {5-move[1]}) to ({move[2]+1}, {5-move[3]}), it will be check!")
    if not check_possible:
        print("No checks found ):")
