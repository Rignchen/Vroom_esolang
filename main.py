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

	def main(self, file_path: str):
		"""Execute code from a .vroom file"""
		if file_path == None: file_path = input("Please enter the file's location: ")
		if not file_path.endswith((".vroom")): self.error("The file needs to be a .vroom file")
		try:
			with open(file_path,"r") as f: code = f.read().split("\n")
		except FileNotFoundError: self.error(f"File {file_path} does not exist")
