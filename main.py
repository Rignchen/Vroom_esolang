"""
Vroom is a 2d programming language with an execution order based on pathfinding algorithms.
The code will look for the shortest path between 1:1 and 1:3 and will wun the code in that order.
The code's executeîon order can only move on spaced, and allways executes the code under if.
As the code want to finish as fast as possible, it won't start if it can't find a path to the end.
Once it reaches the end, it will run the square of code specified at the top value of the stack if it exists.
"""

class vroom:
	def __init__(self, file_path:str = None, run:bool = True) -> None:
		# Interpreter variables
		self.warn_error = False # If true, the code will raise an error instead of a warning
		self.debug_mode = False # If true, the code will print information about the execution
		self.debug_step_mode = False # If true, the code will wait for a keypress between each step
		self.debug_pathfinding = False # If true, the code will print the pathfinding map before executing the code
		self.interpreter_debug_mode = False # If true, the code will print more information but those are not ment to be easy to read

		# define the variables
		self.is_running = True
		self.is_block_running = False
		self.current_block = 0
		self.start_slot = [0,0]
		self.finish_slot = [0,2]

		if run:self.main(file_path)
	
	# Define print function
	def stop(self):
		"""stop the program"""
		global is_running
		is_running = False
		from sys import exit
		exit()
	def error(self,message: str = None) -> None:
		"""print the error message in red and exit the program"""
		if message == None: message = f"An unknow error occured at {self.position} in block {self.current_block}"
		print("\033[91mError: " + str(message) + "\033[0m")
		self.stop()
	def warn(self,message: str = "", is_error: bool = None) -> None:
		"""print the warning message in yellow, unless warn_error is True"""
		if is_error == None: is_error = self.warn_error
		if is_error: self.error(message + " (warn -> error)")
		else: print("\033[93mWarning: " + str(message) + "\033[0m")
	def debug(self,message: str|dict) -> None:
		"""print the debug message in blue, unless debug_mode is False"""
		if self.debug_mode: print("\033[94mDebug: " + str(message) + "\033[0m")
	def iprint(self,message: str) -> None:
		"""print the message in green, used to debug the interpreter"""
		if self.interpreter_debug_mode: print("\033[92m" + str(message) + "\033[0m")
	def tprint(self,message: str) -> None:
		"""print the message in pink, used to debug the interpreter as a temporary print"""
		print("\033[95m" + repr(message) + "\033[0m")
	def table(self,table: list[list[str]], position: list[int]) -> None:
		"""print the table with the position with a green background"""
		out = "|" + "-"*(len(table[0])) + "|\n|"
		for i in range(len(table)):
			for j in range(len(table[i])):
				if [i,j] == position: 
					out += f"\033[42m{table[i][j]}\033[0m"
				else: 
					self.tprint(f"{i},{j}/{position}")
					out += str(table[i][j])
			out += "|\n|"
		out += "-"*(len(table[0])) + "|\n"
		print(out)

	# Main code
	def main(self, file_path: str):
		"""Execute code from a .vroom file"""
		if file_path == None: file_path = input("Please enter the file's location: ")
		if not file_path.endswith((".vroom")): self.error("The file needs to be a .vroom file")
		try:
			with open(file_path,"r") as f: code = f.read().split("\n")
		except FileNotFoundError: self.error(f"File {file_path} does not exist")
		blocks = self.make_blocks(code)
		while is_running and 0 <= self.current_block < len(blocks):
			# execute the code
			self.map = self.make_map(blocks[self.current_block])
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
			for i in map: self.debug(i)

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
		self.position = self.start_slot # The position of the interpreter in the code
		self.stack: list[int] # The storage
		self.is_block_running = True

		while self.is_block_running:
			if self.debug_step_mode: input("Press enter to continue")
			if self.position[1] == len(code)-1: self.error(f"The interpreter can't find next instruction from {self.position[0]}, {self.position[1]}")
			self.execute(code[self.position[0]-1][self.position[1]])
			self.move()
			if self.position == self.finish_slot: self.is_block_running = False

	# Run
	def move(self) -> None:
		"""Move the interpreter to the next position"""
		if self.position[0] != 0 and self.map[self.position[0]-1][self.position[1]] == self.map[self.position[0]][self.position[1]]-1:
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
		self.error(f"Impossible to find a path to the end from {self.position[0]}, {self.position[1]}")
	def execute(self, char: str) -> None:
			match ord(char):
				# →
				case 8594: 
					if len(self.stack) == 0: self.error("The stack is empty")
					self.stack.insert(self.stack[-1],0)
					self.stack.pop()
				# ←
				case 8592:
					if len(self.stack) == 0: self.error("The stack is empty")
					self.stack.append(self.stack[0])
					self.stack.pop(0)
	pass
