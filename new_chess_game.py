from pieces import *

# EN PASSANT
# CASTLING
# PAWN CONVERSION

FILES = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
RANKS = ('1', '2', '3', '4', '5', '6', '7', '8')

def print_board(Board, turn):
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

def update_board(pieces):
	Board = [['  ' for x in range(8)] for y in range(8)]
	for p in pieces.values():
		for piece in p:
			Board[piece.row][piece.column] = piece.name
	return Board

def initialize_game():
	turn = 'w'	
	pieces = {
		"wR": [Rook("wR", 0, 0), Rook("wR", 0, 7)],
		"wN": [Knight("wN", 0, 1), Knight("wN", 0, 6)],
		"wB": [Bishop("wB", 0, 2), Bishop("wB", 0, 5)],
		"wQ": [Queen("wQ", 0, 3)],
		"wK": [King("wK", 0, 4)],
		"wP": [Pawn("wP", 1, i) for i in range(8)],
		"bR": [Rook("bR", 7, 0), Rook("bR", 7, 7)],
		"bN": [Knight("bN", 7, 1), Knight("bN", 7, 6)],
		"bB": [Bishop("bB", 7, 2), Bishop("wB", 7, 5)],
		"bQ": [Queen("bQ", 7, 3)],
		"bK": [King("bK", 7, 4)],
		"bP": [Pawn("bP", 6, i) for i in range(8)]
	}
	Board = update_board(pieces)
	return (Board, pieces, turn)

def parse_code(code):
	piece_name = code[0] if code[0] in ('R', 'N', 'B', 'Q', 'K') else 'P'
	if piece_name == 'P' and code[0] not in FILES:
		raise SyntaxError(f"Invalid chess notation: {code}")

	destination_row = destination_column = ""
	origin_row = origin_column = ""
	capturing = checking = checkmate = False
	end_symbol = ""

	i = 0 if piece_name == 'P' else 1
	
	if i < len(code) and code[i] in FILES:
		destination_column = FILES.index(code[i])
		i += 1
	if i < len(code) and code[i] in RANKS:
		destination_row = RANKS.index(code[i])
		i += 1
	if i < len(code) and code[i] == 'x':
		capturing = True
		i += 1
	if i < len(code) and code[i] in FILES:
		origin_column = destination_column
		destination_column = FILES.index(code[i])
		i += 1
	if i < len(code) and code[i] in RANKS:
		origin_row = destination_row
		destination_row = RANKS.index(code[i])
		i += 1
	if i < len(code) and code[i] == '+':
		checking = True
		i += 1
	elif i < len(code) and code[i] == '#':
		checkmate = True
		i += 1
	if i < len(code) and code[i:] in ('!', '?', '!!', '!?', '?!', '??'):
		end_symbol = code[i:]
		i = len(code)

	if i < len(code):
		raise SyntaxError(f"Invalid chess notation: {code}")

	if destination_row == "" or destination_column == "":
		raise SyntaxError(f"Invalid chess notation: {code}")		

	return (piece_name, origin_row, origin_column, destination_row, destination_column, 
			capturing, checking, checkmate, end_symbol)

def make_move(code, Board, pieces, turn):
	piece_name, origin_row, origin_column, destination_row, destination_column, \
	capturing, checking, checkmate, end_symbol = parse_code(code)

	possible_pieces = [p for p in pieces[turn + piece_name] if p.can_move(destination_row, destination_column, Board)]

	# Resolve ambiguity
	if len(possible_pieces) > 1:
		if origin_row != "":
			possible_pieces = [p for p in possible_pieces if p.row == origin_row]
		if origin_column != "":
			possible_pieces = [p for p in possible_pieces if p.column == origin_column]
		if len(possible_pieces) > 1:
			raise SyntaxError(f"Ambiguity in move: {code}")
	elif len(possible_pieces) == 1 and (origin_row != "" or origin_column != ""):
		raise SyntaxError(f"Over-resolved ambiguity in move: {code}")

	# Make sure at least one piece can move
	if len(possible_pieces) == 0:
		raise SyntaxError(f"Invalid move: {code}")

	# If it's capturing, validate that it says so and make the capture
	opposite_turn = 'w' if turn == 'b' else 'b'
	destination_piece = Board[destination_row][destination_column]
	if destination_piece == opposite_turn + 'K':
		raise SyntaxError(f"Cannot capture the king: {code}")
	if destination_piece[0] == opposite_turn:
		if not capturing:
			raise SyntaxError(f"Move captures a piece: {code}")
		pieces[destination_piece] = [p for p in pieces[destination_piece] if p.row != destination_row or p.column != destination_column]
	
	# Move the piece
	possible_pieces[0].move(destination_row, destination_column)
	Board = update_board(pieces)

	# If the current king is in check
	current_king = pieces[turn + 'K'][0]
	if current_king.is_checked(current_king.row, current_king.column, pieces, Board):
		raise SyntaxError(f"Move places king in check: {code}")

	# Check if the opposite king is put in check correctly
	opposite_king = pieces[opposite_turn + 'K'][0]
	in_check = opposite_king.is_checked(opposite_king.row, opposite_king.column, pieces, Board)
	
	# Check if the opposite king is put in checkmate correctly 
	in_checkmate = True if in_check else False

	possible_spots = ((opposite_king.row + 1, opposite_king.column + 1),
					  (opposite_king.row + 1, opposite_king.column + 0),
					  (opposite_king.row + 1, opposite_king.column - 1),
					  (opposite_king.row + 0, opposite_king.column + 1),
					  (opposite_king.row + 0, opposite_king.column - 1),
					  (opposite_king.row - 1, opposite_king.column + 1),
					  (opposite_king.row - 1, opposite_king.column + 0),
					  (opposite_king.row - 1, opposite_king.column - 1))

	for (possible_row, possible_column) in possible_spots:
		if possible_row < 8 and possible_column < 8 and \
		   possible_row > 0 and possible_column > 0 and \
		   opposite_king.can_move(possible_row, possible_column, Board) and \
		   not opposite_king.is_checked(possible_row, possible_column, pieces, Board):
			in_checkmate = False

	if in_checkmate and not checkmate:
		raise SyntaxError(f"Need checkmate symbol: {code}")
	elif not in_checkmate and checkmate:
		raise SyntaxError(f"Invalid checkmate symbol: {code}")
	
	if in_check and not checking and not checkmate:
		raise SyntaxError(f"Need check symbol: {code}")
	elif not in_check and checking:
		raise SyntaxError(f"Invalid check symbol: {code}")
	
	return Board


def play_game(filename):
	with open(filename, "r") as f:
		full_text = f.read()
		words = full_text.split()
		for i in range(len(words)):
			if i % 3 == 0 and i != len(words) - 1:
				if not words[i:-1].isnumeric() or words[-1] != '.' or int(words[i:-1]) != i / 3 + 1:
					raise SyntaxError(f"Incorrect number: {words[i]}")
		if words[-1] not in ('1-0', '0-1', '1/2-1/2'):
			raise SyntaxError(f"Invalid ending: {words[-1]}")

		Board, pieces, turn = initialize_game()
		print_board(Board, turn)
		
		for move in words:
			Board = make_move(move, Board, pieces, turn)
			turn = 'w' if turn == 'b' else 'b'
			print_board(Board, turn)


play_game('games/game1.txt')
