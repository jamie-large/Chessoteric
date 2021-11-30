# Given proper chess notation (PGN), will simulate the chess game
# For use with the chessoteric programming language
# Created by Jamie Large in 2021
import sys

from pieces import *

FILES = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
RANKS = ('1', '2', '3', '4', '5', '6', '7', '8')

def print_board(Board, turn, turn_number):
	t = "White's turn" if turn == 'w' else "Black's turn"
	print()
	print(f"{turn_number}. {t}")
	print('  ', end='')
	print([x + ' ' for x in FILES])
	for i in range(7, -1, -1):
		print(i+1, end=' ')
		print([p.name if p is not None else '  ' for p in Board[i]])

def update_board(pieces):
	Board = [[None for x in range(8)] for y in range(8)]
	for p in pieces.values():
		for piece in p:
			Board[piece.row][piece.column] = piece
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
		"bB": [Bishop("bB", 7, 2), Bishop("bB", 7, 5)],
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
	end_symbol = promotion_piece = ""

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
	if i < len(code) and code[i] == '=':
		i += 1
		if i == len(code) or code[i] not in ('R', 'N', 'B', 'Q'):
			raise SyntaxError(f"Must specify promotion piece: {code}")
		promotion_piece = code[i]
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
			capturing, checking, checkmate, end_symbol, promotion_piece)

def make_move(code, Board, pieces, turn):
	for pawn in pieces[turn + 'P']:
		pawn.en_passant = False

	checking = checkmate = False
	# Check for castle
	if (len(code) >= 3 and code[0:3] == "O-O") or (len(code) >= 5 and code[0:5] == "O-O-O"):
		rook_row = 0 if turn == 'w' else 7
		rook_col = 0 if (len(code) >= 5 and code[0:5] == "O-O-O") else 7
		king = pieces[turn + 'K'][0]
		rooks = [r for r in pieces[turn + 'R'] if r.row == rook_row and r.column == rook_col]
		
		if len(rooks) != 1 or king.has_moved or rooks[0].has_moved or king.is_checked(king.row, king.column, pieces, Board):
			raise SyntaxError(f"Invalid castle: {code}")

		start = min(rook_col, king.column) + 1
		end = max(rook_col, king.column)

		for i in range(start, end):
			if Board[rook_row][i] is not None or king.is_checked(rook_row, i, pieces, Board):
				raise SyntaxError(f"Invalid castle: {code}")

		if (len(code) >= 5 and code[0:5] == "O-O-O"):
			king.move(rook_row, 2)
			rooks[0].move(rook_row, 3)
		else:
			king.move(rook_row, 6)
			rooks[0].move(rook_row, 5)

		i = 5 if (len(code) >= 5 and code[0:5] == "O-O-O") else 3

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

	else:
		piece_name, origin_row, origin_column, destination_row, destination_column, \
		capturing, checking, checkmate, end_symbol, promotion_piece = parse_code(code)

		possible_pieces = [p for p in pieces[turn + piece_name] if p.can_move(destination_row, destination_column, Board)]

		# Resolve ambiguity
		if len(possible_pieces) > 1:
			if origin_row != "":
				possible_pieces = [p for p in possible_pieces if p.row == origin_row]
			if origin_column != "":
				possible_pieces = [p for p in possible_pieces if p.column == origin_column]
			if len(possible_pieces) > 1:
				raise SyntaxError(f"Ambiguity in move: {code}")
		elif len(possible_pieces) == 1 and (origin_row != "" or origin_column != "") and piece_name != 'P':
			raise SyntaxError(f"Over-resolved ambiguity in move: {code}")

		# Make sure at least one piece can move
		if len(possible_pieces) == 0:
			raise SyntaxError(f"Invalid move: {code}")

		# If it's capturing, validate that it says so and make the capture
		opposite_turn = 'w' if turn == 'b' else 'b'
		destination_piece = Board[destination_row][destination_column]
		if destination_piece is not None:
			if destination_piece.name == opposite_turn + 'K':
				raise SyntaxError(f"Cannot capture the king: {code}")
			if destination_piece.name[0] == opposite_turn:
				if not capturing:
					raise SyntaxError(f"Move captures a piece: {code}")
				pieces[destination_piece.name] = [p for p in pieces[destination_piece.name] if p.row != destination_row or p.column != destination_column]
		# En passant capture
		elif possible_pieces[0].name[1] == 'P' and possible_pieces[0].valid_en_passant(destination_row, destination_column, Board):
			direction = 1 if turn == 'w' else -1
			if not capturing:
				raise SyntaxError(f"Move captures a piece: {code}")
			pieces[opposite_turn + 'P'] = [p for p in pieces[opposite_turn + 'P'] if p.row != destination_row - direction or p.column != destination_column]		

		# Move the piece
		possible_pieces[0].move(destination_row, destination_column)
		# Promote a pawn if necessary
		if promotion_piece != "":
			if possible_pieces[0].name[1] != 'P' or destination_row not in (0, 7):
				raise SyntaxError(f"Invalid pawn promotion")
			pieces[possible_pieces[0].name] = [p for p in pieces[possible_pieces[0].name] if p.row != destination_row or p.column != destination_column]
			if promotion_piece == 'Q':
				pieces[turn + 'Q'].append(Queen(turn + 'Q', destination_row, destination_column))
			elif promotion_piece == 'N':
				pieces[turn + 'N'].append(Knight(turn + 'N', destination_row, destination_column))
			elif promotion_piece == 'R':
				pieces[turn + 'R'].append(Rook(turn + 'R', destination_row, destination_column))
			elif promotion_piece == 'B':
				pieces[turn + 'B'].append(Bishop(turn + 'B', destination_row, destination_column))
		elif promotion_piece == "" and possible_pieces[0].name[1] == 'P' and destination_row in (0, 7):
			raise SyntaxError(f"Must specify pawn for promotion")
		Board = update_board(pieces)

		# If the current king is in check
		current_king = pieces[turn + 'K'][0]
		if current_king.is_checked(current_king.row, current_king.column, pieces, Board):
			raise SyntaxError(f"Move places king in check: {code}")

	# Check if the opposite king is put in check correctly
	opposite_turn = 'w' if turn == 'b' else 'b'
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
				if not words[i][:-1].isnumeric() or words[i][-1] != '.' or int(words[i][:-1]) != i / 3 + 1:
					raise SyntaxError(f"Incorrect number: {words[i]}")
		if words[-1] not in ('1-0', '0-1', '1/2-1/2'):
			raise SyntaxError(f"Invalid ending: {words[-1]}")

		moves = [words[i] for i in range(len(words)) if i % 3 != 0][:-1]

		Board, pieces, turn = initialize_game()
		turn_number = 0.5
		print_board(Board, turn, int(turn_number))
		
		for move in moves:
			turn_number += 0.5
			Board = make_move(move, Board, pieces, turn)
			turn = 'w' if turn == 'b' else 'b'
			print_board(Board, turn, int(turn_number))

if len(sys.argv) > 1:
	play_game(sys.argv[1])
else:
	play_game('games/game1.txt')
