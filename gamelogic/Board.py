from .Piece import Piece

class Board:
    def __init__(self):
        self.topCorner = [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(3,0),(3,1),(4,0)]
        self.botCorner = [(9,9),(9,8),(9,7),(9,6),(9,5),(8,9),(8,8),(8,7),(8,6),(7,9),(7,8),(7,7),(6,9),(6,8),(5,9)]
        self.isRedsTurn = True
        self.create_board()
    
    def create_board(self):
        self.board = [
            [Piece(0,0,"r"), Piece(1,0,"r"), Piece(2,0,"r"), Piece(3,0,"r"), Piece(4,0,"r"), 0, 0, 0, 0, 0],
            [Piece(0,1,"r"), Piece(1,1,"r"), Piece(2,1,"r"), Piece(3,1,"r"), 0, 0, 0, 0, 0, 0],
            [Piece(0,2,"r"), Piece(1,2,"r"), Piece(2,2,"r"), 0, 0, 0, 0, 0, 0, 0],
            [Piece(0,3,"r"), Piece(1,3,"r"), 0, 0, 0, 0, 0, 0, 0, 0],
            [Piece(0,4,"r"), 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, Piece(9,5,"b")],
            [0, 0, 0, 0, 0, 0, 0, 0, Piece(8,6,"b"), Piece(9,6,"b")],
            [0, 0, 0, 0, 0, 0, 0, Piece(7,7,"b"), Piece(8,7,"b"), Piece(9,7,"b")],
            [0, 0, 0, 0, 0, 0, Piece(6,8,"b"), Piece(7,8,"b"), Piece(8,8,"b"), Piece(9,8,"b")],
            [0, 0, 0, 0, 0, Piece(5,9,"b"), Piece(6,9,"bl"), Piece(7,9,"b"), Piece(8,9,"b"), Piece(9,9,"b")]
         ]
    def ai_update_board(self, Newboard):
        self.board = Newboard

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for cell in row:
                if cell != 0 and cell.color == color:
                    pieces.append(cell)
        return pieces
    
    def move(self, piece, newX, newY):
        if (newX, newY) in self.get_all_possible_hops(piece, [], []) or (newX, newY) in self.get_all_possible_steps(piece):
            self.board[piece.y][piece.x] = 0
            piece.x = newX
            piece.y = newY
            self.board[piece.y][piece.x] = piece

    def get_pice_at(self, x,y):
        if 0<= x <=9 and 0 <= y <= 9:
            return self.board[y][x]
        else:
            return "Piece index out of bounds"
        
    def check_if_cell_is_empty(self, x,y):
        if self.board[y][x] == 0:
            return True
        else:
            return False
    
    def get_all_possible_steps(self, piece):
        possible_steps = []
        left = piece.x -1
        right = piece.x + 1
        up = piece.y - 1
        down = piece.y + 1

        #check left and right of the piece
        if right <=9 and self.check_if_cell_is_empty(right, piece.y):
            possible_steps.append((right, piece.y))

        if left >=0 and self.check_if_cell_is_empty(left, piece.y):
            possible_steps.append((left, piece.y))

        #check upward and downward of the piece
        if up >= 0 and self.check_if_cell_is_empty(piece.x, up):
            possible_steps.append((piece.x, up))
        
        if down <= 9 and self.check_if_cell_is_empty(piece.x, down):
            possible_steps.append((piece.x, down))

        #check upper left and upper right of the piece
        if up >= 0 and left >=0 and self.check_if_cell_is_empty(left, up):
            possible_steps.append((left, up))
        
        if up >= 0  and right<=9 and self.check_if_cell_is_empty(right, up):
            possible_steps.append((right, up))
        #check downward left and downward right of the piece
        if down <= 9 and left >=0 and self.check_if_cell_is_empty(left, down):
            possible_steps.append((left, down))
        
        if down <= 9 and right<=9 and self.check_if_cell_is_empty(right, down):
            possible_steps.append((right, down))
        
        return possible_steps

    def get_all_possible_hops(self, piece, visited, possible_hops= []):
        xI = piece.x
        yI = piece.y
        surroundings =[-1,0,1]
        for i in surroundings:
            for j in surroundings:
                xF = xI + 2 * i
                yF = yI + 2 * j
                if 0 <= xF <= 9 and 0 <= yF <=9 and self.check_if_cell_is_empty(xI + i, yI + j) == False and self.check_if_cell_is_empty(xF, yF) == True and (xF, yF) not in visited:
                    visited.append((xF, yF))
                    possible_hops.append((xF,yF))
                    self.get_all_possible_hops(Piece(xF,yF, piece.color), visited, possible_hops)   
        return possible_hops
    
    def get_all_moves(self, piece):
        return self.get_all_possible_hops(piece, [], []) + self.get_all_possible_steps(piece)

    def evaluate(self):
        redVerticalPos = 0
        redHorizontalPos = 0
        redAtGoal = self.get_pieces_at_goal("r")

        blueVerticalPos = 0
        blueHorizontalPos = 0
        blueAtGoal = self.get_pieces_at_goal("b")
        for piece in self.get_all_pieces("r"):
            redVerticalPos += piece.y
            redHorizontalPos += piece.x

        for piece in self.get_all_pieces("b"):
            blueVerticalPos += piece.y
            blueHorizontalPos += piece.x

        return (redVerticalPos - (9 - blueVerticalPos)) + (redHorizontalPos - (9 - blueHorizontalPos)) + 1.5 * (redAtGoal - blueAtGoal)

    def get_pieces_at_goal(self, color):
        result = 0   
        for piece in self.get_all_pieces(color):
            if color == "r":
                if (piece.x, piece.y) in self.botCorner:
                    result +=1
            if color == "b":
                if (piece.x, piece.y) in self.topCorner:
                    result +=1
        return result
    
    def winner(self):
        r_top = 0
        b_top = 0
        r_bot = 0
        b_bot = 0
        if self.get_pieces_at_goal("r") == 15:
            return "r"
        if self.get_pieces_at_goal("b") == 15:
            return "b"
        for cell in self.topCorner:
            if self.check_if_cell_is_empty(cell[0], cell[1]) == False:
                piece = self.get_pice_at(cell[0], cell[1])
                if piece.color == "r":
                    r_top += 1
                else:
                    b_top += 1
            if r_top + b_top == 15 and b_top != 0:
                return "b"
        for cell in self.botCorner:
            if self.check_if_cell_is_empty(cell[0], cell[1]) == False:
                piece = self.get_pice_at(cell[0], cell[1])
                if piece.color == "r":
                    r_bot += 1
                else:
                    b_bot += 1
            if r_bot + b_bot == 15 and r_bot != 0:
                return "r"
        else:
            return None

    def __str__(self):
        result = ""
        for i in range(0, 10):
            for j in range(0,10):
               result += str(self.board[i][j]) + " "
            result +="\n"
        return result

