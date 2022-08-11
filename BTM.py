# Interpreter for the version of the Binary Turing Machine!? programming language used by
# the Chessoteric programming language
# Created by Jamie Large in 2022
import sys
from Machine import Machine

def process_code(code):
	m = Machine()
	for line in code:
		m.process_command(line)
	m.process_command("FLUSH")

	m.run_machine()

if len(sys.argv) > 1:
	with open(sys.argv[1], "r") as f:
		process_code([line[:-1] for line in f.readlines()])
else:
	str_buf = []
	for line in sys.stdin:
		str_buf.append(line)
	process_code(str_buf)