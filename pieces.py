# Given proper chess notation (PGN), will simulate the chess game
# For use with the chessoteric programming language
# Created by Jamie Large in 2021

Board = [['  ' for x in range(8)] for y in range(8)]

class Piece:
	def __init__(self, name, row, column):
		self.name = name
		self.row = row
		self.column = column

	# Move piece to destination_row, destination_column
	def move(self, destination_row, destination_column):
		self.row = destination_row
		self.column = destination_column

	# Check if piece can move
	def can_move(self, destination_row, destination_column):
		if self.row == destination_row and self.column == destination_column:
			raise ValueError(f"Piece {self.name} already at {self.row}, {self.column}")

		# Make sure that there is no piece of the same color in this space already
		if Board[destination_row][destination_column][0] == self.name[0]:
			return False
		return True

class Rook(Piece):
	def can_move(self, destination_row, destination_column):
		if not super().can_move(destination_row, destination_column):
			return False

		if self.row != destination_row and self.column != destination_column:
			return False
		
		end = abs(self.row - destination_row) if self.row != destination_row else abs(self.column - destination_column)
		row_increment = int((destination_row - self.row) / end)
		column_increment = int((destination_column - self.column) / end)
		row_counter = row_increment
		column_counter = column_increment

		for i in range(end - 1):
			if Board[self.row + row_counter][self.column + column_counter] != '  ':
				return False
			row_counter += row_increment
			column_counter += column_increment

		return True

class Bishop(Piece):
	def can_move(self, destination_row, destination_column):
		if not super().can_move(destination_row, destination_column):
			return False

		if abs(self.row - destination_row) != abs(self.column - destination_column):
			return False

		end = abs(self.row - destination_row)
		row_increment = int((destination_row - self.row) / end)
		column_increment = int((destination_column - self.column) / end)
		row_counter = row_increment
		column_counter = column_increment
		
		for i in range(end - 1):
			if Board[self.row + row_counter][self.column + column_counter] != '  ':
				return False
			row_counter += row_increment
			column_counter += column_increment
		
		return True

def Knight(Piece):
	def can_move(self, destination_row, destination_column):
		if not super().can_move(destination_row, destination_column):
			return False

		if abs(self.row - destination_row) == abs(self.column - destination_column):
			end = abs(self.row - destination_row)
			row_increment = int((destination_row - self.row) / end)
			column_increment = int((destination_column - self.column) / end)
			row_counter = row_increment
			column_counter = column_increment
			
			for i in range(end):
				if Board[self.row + row_counter][self.column + column_counter] != '  ':
					return False
				row_counter += row_increment
				column_counter += column_increment
			
			return True

		return False
