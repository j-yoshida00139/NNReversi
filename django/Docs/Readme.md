Data format

1. Reversi game pieces arrangement

	8 x 8 list: Black = 1, White = 2, None = 0

2. Reversi game pieces arrangement for NN input

	192 list:
	- None = [0, 0, 1]
	- Own piece = [0, 1, 0]
	- Other piece = [1, 0, 0]
	
3. NN arrangement in DB

	2 integer values: Converted from ternary to decimal number
	
