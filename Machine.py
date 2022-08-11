# Machine for the chessoteric programming language
# Created by Jamie Large in 2022
BLANK = 0
INITIAL_STATE = 0
INPUT_STATE = 1
OUTPUT_STATE = 2

class Machine:
	def __init__(self):
		self.tape = []
		self.rules = {}
		self.current_rule = []
		self.current_input = None

	def process_command(self, command):
		if command == "FLUSH":
			# flush rule if it is complete
			if len(self.current_rule) == 5:
				self.current_rule[-1] = int(self.current_rule[-1], 2)
				self.rules[(self.current_rule[0], self.current_rule[1])] = (self.current_rule[2], self.current_rule[3], self.current_rule[4])
				self.current_rule = []
			# flush input if it exists
			if self.current_input:
				input_value = int(self.current_input, 2)
				self.tape.append(input_value)
			return

		if len(command) < 1 or command[-1] not in ("?", "!") or (len(command) >= 2 and command[-2] not in ("0", "1", "?", "!")) \
		   or not all(c == "0" or c == "1" for c in command[:-2]):
			raise SyntaxError("Invalid command: " + command);

		i = 0
		# Skip over leading 1s then leading 0s
		while (command[i] == "1"):
			i += 1
		while (command[i] == "0"):
			i += 1
		# Skip over first 1
		if (command[i] == "1"):
			i += 1

		if command[-1] == "!":
			# Continue rule
			if len(command) >= 2 and command[-2] == "!":
				command = command[:-2]
				# make sure there is a part of rule to continue
				if len(self.current_rule) == 0:
					raise SyntaxError("No part of rule to continue")
				self.current_rule[-1] += command[i:]
				
			# New part of rule
			else: 
				command = command[:-1]
				# convert previous part of rule to an int
				if len(self.current_rule) > 0:
					self.current_rule[-1] = int(self.current_rule[-1], 2)
				# if the previous rule is now complete, add it to the rules
				if len(self.current_rule) == 5:
					self.rules[(self.current_rule[0], self.current_rule[1])] = (self.current_rule[2], self.current_rule[3], self.current_rule[4])
					self.current_rule = []
				# Add this to the rule
				self.current_rule.append(command[i:])
		
		elif command[-1] == "?":
			# Continue input
			if len(command) >= 2 and command[-2] == "?":
				command = command[:-2]
				# make sure there is input to continue
				if not self.current_input:
					raise SyntaxError("No input to continue")
				self.current_input += command[i:]

			# New input
			else:
				command = command[:-1]
				# flush input if it exists
				if self.current_input:
					input_value = int(self.current_input, 2)
					self.tape.append(input_value)
				# Set the current input
				self.current_input = command[i:]
				
		
	# Run the Turing Machine on the specified input
	def run_machine(self):
		index = 0
		state = INITIAL_STATE
		if len(self.tape) == 0:
			self.tape.append(BLANK)
		c_symbol = self.tape[index]
		while (state, c_symbol) in self.rules or state in (INPUT_STATE, OUTPUT_STATE):
			# INPUT STATE
			if state == INPUT_STATE:
				user_input = input()
				try:
					int_input = int(user_input)
					self.tape[index] = int_input
				except:
					int_input = 0
					for c in user_input:
						int_input += ord(c)
					self.tape[index] = int_input
				state = INITIAL_STATE
				index += 1

			# OUTPUT STATE
			elif state == OUTPUT_STATE:
				if c_symbol != BLANK:
					try:
						p_symbol = chr(c_symbol)
						print(p_symbol, end='')
					except:
						print(c_symbol, end='')
					index += 1
				else:
					state = INITIAL_STATE
					index += 1
					
			# OTHER STATE
			else:
				state, n_symbol, direction = self.rules[(state, c_symbol)]
				self.tape[index] = n_symbol
				index = max(index + (1 if direction % 2 == 0 else -1), 0)

			if index == len(self.tape):
				self.tape.append(0)
			c_symbol = self.tape[index]
