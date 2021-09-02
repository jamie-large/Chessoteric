# Plays chess
# For use with the chessoteric programming language
# Created by Jamie Large in 2021

BOARD_SIZE = 8
Board = [['  ' for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
turn = 'w'

FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANKS = ['1', '2', '3', '4', '5', '6', '7', '8']

# Set the board up
def initialize_board():
	for i in range(BOARD_SIZE):
		for j in range(BOARD_SIZE):
			word = ''
			if i < 2 or i > 5:
				if i < 2:
					word = 'w'
				if i > 5:
					word = 'b'
				if i == 0 or i == 7:
					if j == 0 or j == 7:
						word += 'R'
					if j == 1 or j == 6:
						word += 'N'
					if j == 2 or j == 5:
						word += 'B'
					if j == 3:
						word += 'Q'
					if j == 4:
						word += 'K'
				if i == 1 or i == 6:
					word += 'P'
				Board[i][j] = word
	# Board[4][4] = 'wP'
	# Board[5][5] = 'wP'

def custom_initialization():
	Board[0][0] = 'wR'
	Board[0][7] = 'wR'
	Board[7][0] = 'bR'
	Board[7][7] = 'bR'


# Prints the board (useful for debugging)
def print_board():
	print()
	print('  ', end='')
	print([x + ' ' for x in FILES])
	for i in range(BOARD_SIZE-1, -1, -1):
		print(i+1, end=' ')
		print(Board[i])
	if (turn == 'w'):
		print('White\'s turn')
	else:
		print('Black\'s turn')

# Make a move given the string note, written in chess notation
def make_move(note):
	global turn, destination_row, destination_col, origin_row, origin_col
	# Make sure input is a string of at least 2 characters
	if not isinstance(note, str) or len(note) < 2:
		raise SyntaxError('Invalid chess notation: ' + str(note))

	# If they are moving a pawn
	# TODO: add promotion
	# TODO: add en passant
	if note[0] in FILES:
		piece = turn + 'P'

		# If the pawn is capturing
		if note[1] == 'x':
			if len(note) < 4 or note[2] not in FILES or note[3] not in RANKS:
				raise SyntaxError('Invalid chess notation: ' + str(note))

			origin_row = origin_col = FILES.index(note[0])
			destination_col = FILES.index(note[2])
			destination_row = RANKS.index(note[3])

			if origin_col - destination_col not in (-1, 1):
				raise SyntaxError('Invalid move: ' + str(note))

			# If it is a white pawn
			if turn == 'w':
				# Make sure it's a valid move
				origin_row = destination_row - 1
				if (origin_row < 0 or Board[origin_row][origin_col] != piece or
					Board[destination_row][destination_col][0] != 'b'):
					raise SyntaxError('Invalid move: ' + str(note))

			# If it is a black pawn
			else:
				# Make sure it's a valid move
				origin_row = destination_row + 1
				if (origin_row > 7 or Board[origin_row][origin_col] != piece or
					Board[destination_row][destination_col][0] != 'w'):
					raise SyntaxError('Invalid move: ' + str(note))

			Board[origin_row][origin_col] = '  '
			Board[destination_row][destination_col] = piece

		else:
			if note[1] not in RANKS:
				raise SyntaxError('Invalid chess notation: ' + str(note))

			origin_col = destination_col = FILES.index(note[0])
			origin_row = destination_row = RANKS.index(note[1])

			if Board[destination_row][destination_col] != '  ':
				raise SyntaxError('Invalid move: ' + str(note))

			# If it is a white pawn
			if turn == 'w':
				# Make sure it's a valid move
				origin_row = destination_row - 1
				
				if origin_row < 0:
					raise SyntaxError('Invalid move: ' + str(note))

				if Board[origin_row][origin_col] != piece and destination_row == RANKS.index('4'):
					origin_row -= 1

				if (origin_row < 0 or Board[origin_row][origin_col] != piece or
					Board[origin_row + 1][origin_col] != '  '):
					raise SyntaxError('Invalid move: ' + str(note))

			# If it is a black pawn
			else:
				# Make sure it's a valid move
				origin_row = destination_row + 1
				
				if origin_row > 7:
					raise SyntaxError('Invalid move: ' + str(note))

				if Board[origin_row][origin_col] != piece and destination_row == RANKS.index('5'):
					origin_row += 1

				if (origin_row > 7 or Board[origin_row][origin_col] != piece or
					Board[origin_row - 1][origin_col] != '  '):
					raise SyntaxError('Invalid move: ' + str(note))

			Board[origin_row][origin_col] = '  '
			Board[destination_row][destination_col] = piece

	# If they are moving a rook
	elif note[0] == 'R':
		piece = turn + 'R'
		capturing = False

		if len(note) < 3:
			raise SyntaxError('Invalid chess notation: ' + str(note))

		# If the rook is capturing
		if note[1] == 'x' or (len(note) > 2 and note[2] == 'x'):
			capturing = True
			x_index = 1 if note[1] == 'x' else 2

			if len(note) < 4 or note[x_index + 1] not in FILES or note[x_index + 2] not in RANKS:
				raise SyntaxError('Invalid chess notation: ' + str(note))

			destination_col = FILES.index(note[x_index + 1])
			destination_row = RANKS.index(note[x_index + 2])

		# Otherwise
		else:
			# If there was a clarifier
			if len(note) > 3 and note[3] in RANKS:
				if note[2] not in FILES:
					raise SyntaxError('Invalid chess notation: ' + str(note))
				destination_col = FILES.index(note[2])
				destination_row = RANKS.index(note[3])
			# If there was not a clarifier
			else:
				if note[1] not in FILES or note[2] not in RANKS:
					raise SyntaxError('Invalid chess notation: ' + str(note))
				destination_col = FILES.index(note[1])
				destination_row = RANKS.index(note[2])


		# find the possible rooks
		possible_origins = []
		# check the rows below it on the same column
		for i in range(destination_row - 1, -1, -1):
			if Board[i][destination_col] == piece:
				possible_origins.append((i, destination_col))
				break
			elif Board[i][destination_col] != '  ':
				break
		# check the rows above it on the same column
		for i in range(destination_row + 1, BOARD_SIZE):
			if Board[i][destination_col] == piece:
				possible_origins.append((i, destination_col))
				break
			elif Board[i][destination_col] != '  ':
				break
		# check the columns to the left of it on the same row
		for i in range(destination_col - 1, -1, -1):
			if Board[destination_row][i] == piece:
				possible_origins.append((destination_row, i))
				break
			elif Board[destination_row][i] != '  ':
				break
		# check the columns to the right of it on the same row
		for i in range(destination_col + 1, BOARD_SIZE):
			if Board[destination_row][i] == piece:
				possible_origins.append((destination_row, i))
				break
			elif Board[destination_row][i] != '  ':
				break

		if len(possible_origins) == 0:
			raise SyntaxError('Invalid move: ' + str(note))

		origin_row = possible_origins[0][0]
		origin_col = possible_origins[0][1]

		# if we need to resolve ambiguity
		if len(possible_origins) >= 2:
			if len(note) <= 3 or (note[1] not in RANKS and note[1] not in FILES):
				raise SyntaxError('Ambiguity in move: ' + str(note))

			if note[1] in RANKS:
				resolved = False
				for possibility in possible_origins:
					if possibility[0] == RANKS.index(note[1]):
						origin_row = possibility[0]
						origin_col = possibility[1]
						resolved = True
				
				if not resolved:
					raise SyntaxError('Invalid move: ' + str(note))

			elif note[1] in FILES:
				resolved = False
				for possibility in possible_origins:
					if possibility[1] == FILES.index(note[1]):
						origin_row = possibility[0]
						origin_col = possibility[1]
						resolved = True
				
				if not resolved:
					raise SyntaxError('Invalid move: ' + str(note))

		if (capturing and Board[origin_row][origin_col] == '  ') or \
		   (not capturing and Board[origin_row][origin_col] != '  '):
		   raise SyntaxError('Invalid chess notation: ' + str(note))

		Board[origin_row][origin_col] = '  '
		Board[destination_row][destination_col] = piece

	# If they are moving a knight
	elif note[0] == 'N':
		piece = turn + 'N'

	# If they are moving a bishop
	elif note[0] == 'B':
		piece = turn + 'B'

	# If they are moving a queen
	# Note: ambiguity of 3 queens
	elif note[0] == 'Q':
		piece = turn + 'Q'

	# If they are moving a king
	elif note[0] == 'K':
		piece = turn + 'K'

	# If they are castling
	elif note[0] == 'O':
		pass

	else:
		raise SyntaxError('Invalid chess notation: ' + str(note))
	
	# Change the turn
	if turn == 'w':
		turn = 'b'
	else:
		turn = 'w'


# initialize_board()
custom_initialization()
print_board()
while True:
    move = input('Move: ')
    if len(move) == 0:
        break
    else:
    	make_move(move)
    	print_board()














