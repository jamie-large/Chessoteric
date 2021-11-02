# Class definitions for each chess piece
# For use with the chessoteric programming language
# Created by Jamie Large in 2021

class Piece:
	def __init__(self, name, row, column):
		self.name = name
		self.row = row
		self.column = column
		self.has_moved = False

	# Move piece to destination_row, destination_column
	def move(self, destination_row, destination_column):
		self.row = destination_row
		self.column = destination_column
		self.has_moved = True

	# Check if piece can move
	def can_move(self, destination_row, destination_column, Board):
		if destination_row > 7 or destination_row < 0:
			raise ValueError(f"Row must be between 0 and 7")
		if destination_column > 7 or destination_column < 0:
			raise ValueError(f"Column must be between 0 and 7")
		if self.row == destination_row and self.column == destination_column:
			raise ValueError(f"Piece {self.name} already at {self.row}, {self.column}")

		# Make sure that there is no piece of the same color in this space already
		if Board[destination_row][destination_column] is not None and \
		   Board[destination_row][destination_column].name[0] == self.name[0]:
			return False
		return True

class Rook(Piece):
	def can_move(self, destination_row, destination_column, Board):
		if not Piece.can_move(self, destination_row, destination_column, Board):
			return False

		if self.row != destination_row and self.column != destination_column:
			return False
		
		end = abs(self.row - destination_row) if self.row != destination_row else abs(self.column - destination_column)
		row_increment = int((destination_row - self.row) / end)
		column_increment = int((destination_column - self.column) / end)
		row_counter = row_increment
		column_counter = column_increment

		for i in range(end - 1):
			if Board[self.row + row_counter][self.column + column_counter] is not None:
				return False
			row_counter += row_increment
			column_counter += column_increment

		return True

class Bishop(Piece):
	def can_move(self, destination_row, destination_column, Board):
		if not Piece.can_move(self, destination_row, destination_column, Board):
			return False

		if abs(self.row - destination_row) != abs(self.column - destination_column):
			return False

		end = abs(self.row - destination_row)
		row_increment = int((destination_row - self.row) / end)
		column_increment = int((destination_column - self.column) / end)
		row_counter = row_increment
		column_counter = column_increment
		
		for i in range(end - 1):
			if Board[self.row + row_counter][self.column + column_counter] is not None:
				return False
			row_counter += row_increment
			column_counter += column_increment
		
		return True

class Knight(Piece):
	def can_move(self, destination_row, destination_column, Board):
		if not Piece.can_move(self, destination_row, destination_column, Board):
			return False

		return (abs(self.row - destination_row) == 1 and abs(self.column - destination_column) == 2) or \
		       (abs(self.row - destination_row) == 2 and abs(self.column - destination_column) == 1)


class Queen(Rook, Bishop):
	def can_move(self, destination_row, destination_column, Board):
		return Rook.can_move(self, destination_row, destination_column, Board) or \
		       Bishop.can_move(self, destination_row, destination_column, Board)

class King(Piece):
	def is_checked(self, destination_row, destination_column, pieces, Board):
		original_piece = Board[destination_row][destination_column]
		Board[destination_row][destination_column] = self
		for p in pieces.values():
			for piece in p:
				if piece.name[0] != self.name[0] and \
				   (piece.row != destination_row or piece.column != destination_column) and \
				   piece.can_move(destination_row, destination_column, Board):
					Board[destination_row][destination_column] = original_piece
					return True
		Board[destination_row][destination_column] = original_piece
		return False

	def can_move(self, destination_row, destination_column, Board):
		if not Piece.can_move(self, destination_row, destination_column, Board):
			return False

		return (abs(self.row - destination_row) <= 1 and abs(self.column - destination_column) <= 1)

class Pawn(Piece):
	def __init__(self, name, row, column):
		super().__init__(name, row, column)
		self.en_passant = False

	def move(self, destination_row, destination_column):
		if abs(destination_row - self.row) == 2:
			self.en_passant = True
		super().move(destination_row, destination_column)

	def valid_en_passant(self, destination_row, destination_column, Board):
		home_row = 1 if self.name[0] == 'w' else 6
		direction = 1 if self.name[0] == 'w' else -1
		opposite_color = 'w' if self.name[0] == 'b' else 'b'
		return (destination_row == self.row + direction and \
		        abs(destination_column - self.column) == 1 and \
		        self.row == home_row + direction * 3 and \
		        Board[destination_row - direction][destination_column] is not None and \
		        Board[destination_row - direction][destination_column].name == opposite_color + 'P' and \
		        Board[destination_row - direction][destination_column].en_passant)

	def can_move(self, destination_row, destination_column, Board):
		if not Piece.can_move(self, destination_row, destination_column, Board):
			return False

		home_row = 1 if self.name[0] == 'w' else 6
		direction = 1 if self.name[0] == 'w' else -1
		opposite_color = 'w' if self.name[0] == 'b' else 'b'
		capturing = False 
		if Board[destination_row][destination_column] is not None and \
		   Board[destination_row][destination_column].name[0] == opposite_color:
		   capturing = True

		# Basic capturing: move up 1 row and to left or right 1 column
		if capturing and destination_row == self.row + direction and \
		             abs(destination_column - self.column) == 1:
		    return True

		# En passant
		if self.valid_en_passant(destination_row, destination_column, Board):
			return True

		# Not capturing: move on same column to empty space 1 above or 2 above if on home row
		if not capturing:
			if destination_column != self.column:
				return False
			if self.row == home_row:
				if destination_row == self.row + direction * 2 and \
				   Board[self.row + direction][self.column] is None and \
				   Board[self.row + direction * 2][self.column] is None:
					return True
			if destination_row == self.row + direction and Board[self.row + direction][self.column] is None:
				return True

		return False
