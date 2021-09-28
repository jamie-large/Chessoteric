from pieces import *

turn = 'w'
FILES = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
RANKS = ('1', '2', '3', '4', '5', '6', '7', '8')

def print_board(pieces):
	print()
	print('  ', end='')
	print([x + ' ' for x in FILES])
	for i in range(7, -1, -1):
		print(i+1, end=' ')
		print(Board[i])
	if (turn == 'w'):
		print('White\'s turn')
	else:
		print('Black\'s turn')

pieces = [Rook("wR", 0, 0), Rook("wR", 0, 7), 
		  Bishop("wB", 0, 2), Bishop("wB", 0, 5),
		  Rook("bR", 7, 0), Rook("bR", 7, 7), 
		  Bishop("bB", 7, 2), Bishop("wB", 7, 5),]

for piece in pieces:
	Board[piece.row][piece.column] = piece.name


test_piece = pieces[2]
print_board(pieces)
for i in range(8):
	for j in range(8):
		if i != test_piece.row or j != test_piece.column:
			if test_piece.can_move(i, j):
				print(f"Can move to {i}, {j}")
			else:
				print(f"Can NOT move to {i}, {j}")