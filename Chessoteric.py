# Interpreter for the chessoteric programming language
# Created by Jamie Large in 2022
import sys
from chess_game import *
from Machine import Machine

def play_game(code):
	words = code.split()
	for i in range(len(words)):
		if i % 3 == 0 and i != len(words) - 1:
			if not words[i][:-1].isnumeric() or words[i][-1] != '.' or int(words[i][:-1]) != i / 3 + 1:
				raise SyntaxError(f"Incorrect number: {words[i]}")
	if words[-1] not in ('1-0', '0-1', '1/2-1/2'):
		raise SyntaxError(f"Invalid ending: {words[-1]}")

	moves = [words[i] for i in range(len(words)) if i % 3 != 0]
	if moves[-1] in ('1-0', '0-1', '1/2-1/2'):
		moves = moves[:-1]

	Board, pieces, turn = initialize_game()
	# turn_number = 0.5

	mach = Machine()

	for move in moves:
		# turn_number += 0.5
		Board, end_symbol, mate = make_move(move, Board, pieces, turn)
		if end_symbol != "":
			mach.process_command(board_to_string(Board) + end_symbol)
			
		turn = 'w' if turn == 'b' else 'b'
		# print_board(Board, turn, int(turn_number))

	mach.process_command("FLUSH")
	mach.run_machine()

def board_to_string(Board):
	output = ""
	for i in range(8):
		for j in range(8):
			if Board[i][j] is not None:
				output += '1' if Board[i][j].name[0] == 'w' else '0'
	return output


if len(sys.argv) > 1:
	with open(sys.argv[1], "r") as f:
		play_game(f.read())
else:
	str_buf = []
	for line in sys.stdin:
		str_buf.append(line)
	play_game(''.join(str_buf))