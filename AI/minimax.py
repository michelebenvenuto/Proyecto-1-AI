from copy import deepcopy
blue = "b"
red = "r"

def minimax(board, depth, is_max_player, alpha, beta):
    if depth == 0 or board.winner() != None:
        return board.evaluate(), board 
    
    if is_max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves_of_color(board, red):
            evaluation = minimax(move, depth -1, False, alpha, beta)[0]
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves_of_color(board, blue):
            evaluation = minimax(move, depth-1, True, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            if beta <= alpha:
                break
            if minEval == evaluation:
                best_move = move

        return minEval, best_move

def simulate_move(piece, move, board):
    board.move(piece, move[0], move[1])
    return board

def get_all_moves_of_color(board, color):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_all_moves(piece)
        for move in valid_moves:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_pice_at(piece.x, piece.y)
            new_board = simulate_move(temp_piece, move, temp_board)
            moves.append(new_board)
    return moves