from personal.utils.mathFunc import *


def test_base10ToNStr():
	assert int(base10ToNStr(10, 3)) == 101


def test_base10ToN():
	assert base10ToN(140, 3) == 12012
