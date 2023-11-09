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
