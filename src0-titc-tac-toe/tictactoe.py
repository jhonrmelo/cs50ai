"""
Tic Tac Toe Player
"""
import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty_counter = 0
    x_counter = 0
    o_counter = 0
    for row in board:
        for column in row:
            if column == EMPTY:
                empty_counter +=1
            elif column == X:
                x_counter += 1
            else:
                o_counter += 1


    if x_counter == o_counter:
        return X
    elif x_counter > o_counter:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()

    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                actions_set.add((row, column))
        
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_to_update = copy.deepcopy(board) 

    row, column = action

    if row < 0 or column < 0 or row > 2 or column > 2:
        raise Exception("this action is not allowed")

    current_player = player(board)

    if board_to_update[row][column] != EMPTY:
        raise Exception("this action is not allowed")
    
    board_to_update[row][column] = current_player

    return board_to_update


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # validating rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
    # validating columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] != EMPTY:
            return board[0][j]
        
    if board[2][0] == board[1][1] == board[0][2] and board[0][2] != EMPTY:
        return board[2][0]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY: 
        return board[0][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    board_winner = winner(board)

    if board_winner != None:
        return True

    if not has_empty_spaces(board):
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    board_winner = winner(board)

    if board_winner is None:
        return 0
    
    if board_winner == X:
        return 1
    
    return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if board == initial_state():
        return (0,0)
    if terminal(board):
        return None
    
    current_player = player(board)

    if current_player == X:
        _, action = max_value(board)
        return action
    else:
        _, action = min_value(board)
        return action

def min_value(board):
    if terminal(board):
        return [utility(board), None]
    value = float('inf')
    for action in actions(board):
        max_value_result, _ = max_value(result(board,action))
        if(max_value_result < value):
            value = max_value_result
            best_action = action
    return [value, best_action]


def max_value(board):
    if terminal(board):
        return [utility(board), None]
    value = float('-inf')
    best_action = tuple[int, int]
    for action in actions(board):
        min_value_result, _ = min_value(result(board,action))
        if(min_value_result > value):
            value = min_value_result
            best_action = action
    return [value, best_action]


def has_empty_spaces(board):
    empty_counter = 0
    for row in board:
        for column in row:
            if column == EMPTY:
                empty_counter +=1
    
    return empty_counter > 0