"""
Vroom is a 2d programming language with an execution order based on pathfinding algorithms.
The code will look for the shortest path between 0:0 and 0:2 and will wun the code in that order.
The code's executeîon order can only move on spaced, and allways executes the code under if.
As the code want to finish as fast as possible, it won't start if it can't find a path to the end.
Once it reaches the end, it will run the square of code specified at the top value of the stack if it exists.
"""

from os import system, name
system("cls" if name == "nt" else "clear")

class vroom:
	def __init__(self, file_path:str = None) -> None:
		# Interpreter variables
		self.warn_error = False # If true, the code will raise an error instead of a warning
		self.debug_mode = True # If true, the code will print information about the execution
		self.debug_step_mode = True # If true, the code will wait for a keypress between each step
		self.debug_pathfinding = True # If true, the code will print the pathfinding map before executing the code
		self.interpreter_debug_mode = True # If true, the code will print more information but those are not ment to be easy to read

		# define the variables
		self.is_running = True
		self.is_block_running = False
		self.current_block = 0
		self.start_slot = [0,0]
		self.position = self.start_slot.copy()
		self.finish_slot = [0,2]

		try: self.main(file_path)
		except KeyboardInterrupt: self.error("KeyboardInterrupt")
		except BaseException:
			if self.interpreter_debug_mode:raise BaseException(f"\033[95mProgram stopped\033[0m")
			elif self.is_running: self.error()
	
	# Define print function
	def stop(self):
		"""stop the program"""
		self.is_running = False
		from sys import exit
		exit()
	def error(self,message: str = "An unknow error occured") -> None:
		"""print the error message in red and exit the program"""
		print(f"\033[91mError in block {self.current_block} at {self.position[0]}/{self.position[1]} : {message}\033[0m")
		self.stop()
	def warn(self,message: str = "", is_error: bool = None) -> None:
		"""print the warning message in yellow, unless warn_error is True"""
		if is_error == None: is_error = self.warn_error
		if is_error: self.error(message + " (warn -> error)")
		else: print(f"\033[93mWarning  in block {self.current_block} at {self.position[0]}/{self.position[1]} : {message}\033[0m")
	def debug(self,message: str|dict) -> None:
		"""print the debug message in blue, unless debug_mode is False"""
		if self.debug_mode: print(f"\033[94mDebug: {message}\033[0m")
	def iprint(self,message: str) -> None:
		"""print the message in green, used to debug the interpreter"""
		if self.interpreter_debug_mode: print(f"\033[92m{message}\033[0m")
	def tprint(self,message: str) -> None:
		"""print the message in pink, used to debug the interpreter as a temporary print"""
		print(f"\033[95m{repr(message)}\033[0m")
	def table(self,table: list[list[str]], position: list[int]) -> None:
		"""print the table with the position with a green background"""
		out = "|" + "-"*(len(table[0])) + "|\n|"
		for i in range(len(table)):
			for j in range(len(table[i])):
				if [i,j] == position:  out += f"\033[42m{table[i][j]}\033[0m"
				else:  out += str(table[i][j])
			out += "|\n|"
		out += "-"*(len(table[0])) + "|\n"
		print(out)

	# Main code
	def main(self, file_path: str):
		"""Execute code from a .vroom file"""
		if file_path == None: file_path = input("Please enter the file's location: ")
		if not file_path.endswith((".vroom")): self.error("The file needs to be a .vroom file")
		try:
			with open(file_path,"r",encoding="utf-8") as f: code = f.read().split("\n")
		except FileNotFoundError: self.error(f"File {file_path} does not exist")
		self.stack: list[int] = [] # The storage.make_blocks(code)
		blocks = self.make_blocks(code)
		while self.is_running and 0 <= self.current_block < len(blocks):
			# execute the code
			self.map = self.make_map(blocks[self.current_block])
			if self.map[self.start_slot[0]][self.start_slot[1]] in [0,-1]: self.error(f"No path between start and end")
			self.run_block(blocks[self.current_block])
			self.current_block = self.stack[-1]

	# Make the map
	def make_map(self, code: list[str]) -> list[list[int]]:
		pos = self.finish_slot
		length = [len(code), len(code[0])]

		# make the map
		map = []
		for i in range(length[0]):
			map.append([])
			for j in range(length[1]): map[-1].append(0 if code[i][j] == " " else -1)
		
		map = self.calculate_map(map,pos,length)

		# print the map if debug_pathfinding is True
		if self.debug_pathfinding:
			out = "Pathinding Map: \n"
			for i in map: out += str(i).replace("-1","  ") + "\n"
			self.debug(out)

		return map
	def calculate_map(self, map: list[list[int]], pos: list[int], length: list[int], distance:int = 0) -> list[list[int]]:
		"""Calculate the pathfinding map"""
		if pos!= self.finish_slot: map[pos[0]][pos[1]] = distance
		if pos[0] != 0:
			if map[pos[0]-1][pos[1]] == 0: map = self.calculate_map(map,[pos[0]-1,pos[1]],length,distance+1)
			elif map[pos[0]-1][pos[1]] > distance+1: map = self.calculate_map(map,[pos[0]-1,pos[1]],length,distance+1)
		if pos[0] != length[0]-1:
			if map[pos[0]+1][pos[1]] == 0: map = self.calculate_map(map,[pos[0]+1,pos[1]],length,distance+1)
			elif map[pos[0]+1][pos[1]] > distance+1: map = self.calculate_map(map,[pos[0]+1,pos[1]],length,distance+1)
		if pos[1] != 0:
			if map[pos[0]][pos[1]-1] == 0: map = self.calculate_map(map,[pos[0],pos[1]-1],length,distance+1)
			elif map[pos[0]][pos[1]-1] > distance+1: map = self.calculate_map(map,[pos[0],pos[1]-1],length,distance+1)
		if pos[1] != length[1]-1:
			if map[pos[0]][pos[1]+1] == 0: map = self.calculate_map(map,[pos[0],pos[1]+1],length,distance+1)
			elif map[pos[0]][pos[1]+1] > distance+1: map = self.calculate_map(map,[pos[0],pos[1]+1],length,distance+1)
		return map

	# Blocks
	def make_blocks(self,code: list[str]) -> list[list[str]]:
		blocks = [[]]
		for i in code:
			if i == '':
				if blocks[-1] != []: blocks.append([])
				continue
			if blocks[-1] == []: length = len(i)
			elif length != len(i): self.error("All lines need to be the same length inside a block")
			blocks[-1].append(i)
		return blocks
	def run_block(self,code: list[str]) -> None:
		self.position = self.start_slot.copy() # The position of the interpreter in the code
		self.last_command = 0 # Remove the last command executed
		self.is_block_running = True

		while self.is_block_running:
			if self.debug_mode:
				self.table(code,self.position)
			if self.position[0] == len(code)-1: self.error(f"The interpreter can't find next instruction")
			self.execute(code[self.position[0]+1][self.position[1]])
			self.move()
			if self.debug_mode:
				self.debug(f"Stack: {self.stack}")
			if self.debug_step_mode: input("Press enter to continue")
			if self.position == self.finish_slot: self.is_block_running = False
		if self.debug_mode:
			self.table(code,self.position)
		self.execute(code[self.position[0]+1][self.position[1]])
		if self.debug_mode:
			self.debug(f"Stack: {self.stack}")

	# Run
	def move(self) -> None:
		"""Move the interpreter to the next position"""
		if self.position[0] != 0:
			if self.map[self.position[0]-1][self.position[1]] == self.map[self.position[0]][self.position[1]]-1:
				self.position[0] -= 1
				return
		if self.position[0] != len(self.map)-1 and self.map[self.position[0]+1][self.position[1]] == self.map[self.position[0]][self.position[1]]-1:
			self.position[0] += 1
			return
		if self.position[1] != 0 and self.map[self.position[0]][self.position[1]-1] == self.map[self.position[0]][self.position[1]]-1:
			self.position[1] -= 1
			return
		if self.position[1] != len(self.map[0])-1 and self.map[self.position[0]][self.position[1]+1] == self.map[self.position[0]][self.position[1]]-1:
			self.position[1] += 1
			return
		self.error(f"Impossible to find a path to the end")
	def execute(self, char: str) -> None:
		match self.last_command:
			case 0:pass
			# ' '
			case 32: # add a value to the stack
				self.stack.insert(0,ord(char))
			# #
			case 35: # skip next instruction
				pass
			# ?
			case 63: # if the last value of the stack is not 0, skip next instruction
				self.last_command = self.stack[-1] # if it's not 0 it will be set to 0 at the end of the function
			case _: # the last command is unknown
				self.tprint(ord(self.last_command))
				self.last_command = 0
		if self.last_command == 0:
			match ord(char):
				# I/O
				# p
				case 112: # pop the last value of the stack and print it as ascii character
					if len(self.stack) == 0: self.error("The stack is empty")
					print(chr(self.stack[-1]),end="")
					self.stack.pop(-1)
				# i
				case 105: #push a value input by the user at the beginning of the stack (each character a value + the len of the input)
					inp = input()
					for i in inp:
						self.stack.insert(0,ord(i))
					self.stack.insert(0,len(inp))
				
				# Math
				# +
				case 43: # pop the last 2 values of the stack, add them and push the result
					if len(self.stack) < 2: self.error("The stack needs at least 2 values to execute an addition")
					self.stack.append(self.stack[-1]+self.stack[-2])
					self.stack.pop(-2)
					self.stack.pop(-2)
				# -
				case 45: # pop the last 2 values of the stack, substract them and push the result
					if len(self.stack) < 2: self.error("The stack needs at least 2 values to execute a subtraction")
					self.stack.append(self.stack[-1]-self.stack[-2])
					self.stack.pop(-2)
					self.stack.pop(-2)
				# *
				case 42: # pop the last 2 values of the stack, multiply them and push the result
					if len(self.stack) < 2: self.error("The stack needs at least 2 values to execute a multiplication")
					self.stack.append(self.stack[-1]*self.stack[-2])
					self.stack.pop(-2)
					self.stack.pop(-2)
				# /
				case 47: # pop the last 2 values of the stack, divide them and push the result
					if len(self.stack) < 2: self.error("The stack needs at least 2 values to execute a division")
					self.stack.append(self.stack[-1]/self.stack[-2])
					self.stack.pop(-2)
					self.stack.pop(-2)
				# %
				case 37: # pop the last 2 values of the stack, modulo them and push the result
					if len(self.stack) < 2: self.error("The stack needs at least 2 values to execute a modulo")
					self.stack.append(self.stack[-1]%self.stack[-2])
					self.stack.pop(-2)
					self.stack.pop(-2)
				# ^
				case 94: # pop the last 2 values of the stack, power them and push the result
					if len(self.stack) < 2: self.error("The stack needs at least 2 values to execute a power")
					self.stack.append(self.stack[-1]**self.stack[-2])
					self.stack.pop(-2)
					self.stack.pop(-2)
			  		# ¬
				case 172: # pop the last value of the stack, push the opposite
					if len(self.stack) == 0: self.error("The stack is empty")
					self.stack[-1] *= -1

				# Boolean tests
				# >
				case 62: # push 0 to the stack if the last value is positive
					if len(self.stack) == 0: self.error("The stack is empty")
					self.stack.append(0 if self.stack[-1] > 0 else 1)
					self.stack.pop(-2)
				# <
				case 60: # push 0 to the stack if the last value is negative
					if len(self.stack) == 0: self.error("The stack is empty")
					self.stack.append(0 if self.stack[-1] < 0 else 1)
					self.stack.pop(-2)

				# Stack manipulation
			 	# →
				case 8594: # move every value in the stack to the right
					if len(self.stack) == 0: self.error("The stack is empty")
					self.stack.insert(self.stack[-1],0)
					self.stack.pop()
				# ←
				case 8592: # move every value in the stack to the left
					if len(self.stack) == 0: self.error("The stack is empty")
					self.stack.append(self.stack[0])
					self.stack.pop(0)
				# ⇄
				case 8644: # swap the last 2 values of the stack
					if len(self.stack) < 2: self.error("The stack needs at least 2 values to swap")
					self.stack[-1],self.stack[-2] = self.stack[-2],self.stack[-1]
				# 0
				case 48: # pop the last value of the stack
					if len(self.stack) == 0: self.error("The stack is empty")
					self.stack.pop()
				# 2
				case 50: # duplicate the last value of the stack
					if len(self.stack) == 0: self.error("The stack is empty")
					self.stack.append(self.stack[-1])

				# Others
				# §
				case 167: # do nothing
					pass
				case _:
					self.last_command = ord(char)
		else: self.last_command = 0
	pass

if __name__ == "__main__": vroom()