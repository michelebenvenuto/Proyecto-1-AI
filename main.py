from gamelogic.Board import Board
from AI.minimax import minimax

negativeInfinity = float('-inf')
positiveInfinity = float('inf')
#Game set up 
print("""Hoppers:
        Escoja una modalidad de juego:
        1) Jugador VS AI
        2) AI VS AI
            """)
game_mode = input("Numero de la opcion que desea: ")
ai_depth = int(input("Ingrese la profundidad de analisis del AI\n NOTA: entre mayor sea la profundida mejor jugara el AI pero se tomara más tiempo en las movidas:"))

#Game_loop
def game_loop():
    run = True
    game = Board()
    
    while run:
        if game_mode == "1":
            if game.isRedsTurn and run:
                value , new_board = minimax(game, ai_depth, True, negativeInfinity, positiveInfinity)
                game.ai_update_board(new_board.board)
                game.isRedsTurn = False
                print("Movida del Jugador Rojo")
                print(game)
                if game.winner() == "r":
                    print("El ganador es el jugador rojo")
                    run = False
                
            if game.isRedsTurn ==False and run:
                xtoMove= int(input("ingrese la posicion x de la ficha a mover: "))
                ytoMove= int(input("ingrese la posicion y de la ficha a mover: "))
                piece = game.get_pice_at(xtoMove, ytoMove)
                print("movidas posibles:")
                posible_moves = game.get_all_moves(piece)
                print(posible_moves)
                destinyX= int(input("ingrese la posicion x de destino de la ficha: "))
                destinyY= int(input("ingrese la posicion y de destino de la ficha: "))
                
                if (destinyX, destinyY) in posible_moves:
                    game.move(piece, destinyX, destinyY)
                    game.isRedsTurn = True
                    print("Movida del Jugador Azul")
                    print(game)
                else:
                    print("move not valid")

                if game.winner() == "b":
                    print("El ganador es el jugador azul")
                    run = False
    
        if game_mode == "2":
            if game.isRedsTurn and run:
                value , new_board = minimax(game, ai_depth, True, negativeInfinity, positiveInfinity)
                game.ai_update_board(new_board.board)
                game.isRedsTurn = False
                print("Movida del Jugador Rojo")
                print(game)
                if game.winner() == "r":
                    print("El ganador es el jugador Rojo ")
                    run = False
                
            if game.isRedsTurn ==False and run:
                value , new_board = minimax(game, ai_depth, False, negativeInfinity, positiveInfinity)
                game.ai_update_board(new_board.board)
                game.isRedsTurn = True
                print("Movida del Jugador Azul")
                print(game)
                if game.winner() == "b":
                    print("El ganador es el jugador Azul")
                    run = False
        
game_loop()