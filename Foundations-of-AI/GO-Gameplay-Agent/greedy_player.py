import random
import sys
from read import readInput
from write import writeOutput
from host import GO
from copy import deepcopy

class MyPlayer():
    def __init__(self):
        self.type = 'greedy'
        self.piece_type = None
        self.opponent = None
        
    def get_valid_moves(self, go, piece_type):
        '''
        Get all valid moves for the current player
        '''
        valid_moves = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check=True):
                    valid_moves.append((i,j))
        
        return valid_moves
    
    def evaluate_move(self, go, move, piece_type):
        '''
        Evaluate a move by simulating it and calculating a score
        '''
        # Create a copy to test the move
        test_go = deepcopy(go)
        test_go.place_chess(move[0], move[1], piece_type)
        
        score = 0
        
        # Capture bonus
        captured = test_go.remove_died_pieces(3 - piece_type)
        score += len(captured) * 10    # High value for captured stones
        
        # Liberty score 
        liberties = self.liberty_count(test_go, move[0], move[1])
        score += liberties * 3
        
        # Position value  
        score += self.get_position_value(move[0], move[1])
        
        # Avoid suicide 
        if not test_go.find_liberty(move[0], move[1]):
            score -= 100    # Heavy penalty for suicide
        
        
        return score
    
    def liberty_count(self, go, i, j):
        '''
        Count liberties (empty adjacent points) for a stone
        '''
        if go.board[i][j] == 0:
            return 0
        
        liberties = 0
        neighbors = go.detect_neighbor(i, j)
        for n in neighbors:
            if go.board[n[0]][n[1]] == 0:
                liberties += 1

        return liberties
    
    def get_position_value(self, i, j):
        '''
        Assign values to board positions
        Corners > Edges > Center for a 5x5 Board
        '''
        # Corner positions (best)
        if (i, j) in [(0, 0), (0, 4), (4, 0), (4,4)]:
            return 5
        
        # Near corner positions (good)
        elif (i, j) in [(1, 1), (1, 3), (3, 1), (3, 3)]:
            return 4
        
        # Edge positions (decent)
        elif i == 0 or i == 4 or j == 0 or j == 4:
            return 3
        
        # Center (neutral)
        elif (i, j) == (2, 2):
            return 2
        
        # Other positions
        else: 
            return 1
        
    def get_input(self, go, piece_type):
        '''
        Get the best move for the current board state.
        '''        
        self.piece_type = piece_type
        self.opponent = 3 - piece_type
        
        # Get all valid moves
        valid_moves = self.get_valid_moves(go, piece_type)
        
        if not valid_moves:
            return "PASS"
        
        # Special case for opening moves (similar to chess)
        if go.n_move <= 2:
            good_openings = [(1, 1), (1, 3), (3, 1), (3, 3)]
            for move in good_openings:
                if move in valid_moves:
                    return move
        
        # Evaluate each move and pick the best
        best_move = None
        best_score = float('-inf')
        
        for move in valid_moves:
            score = self.evaluate_move(go, move, piece_type)
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move if best_move else random.choice(valid_moves)

if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = MyPlayer()
    action = player.get_input(go, piece_type)
    writeOutput(action)
