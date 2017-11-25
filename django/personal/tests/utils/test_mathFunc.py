from personal.utils.mathFunc import *


def test_sigmoid():
	assert sigmoid(0) == 0.5


def test_sigmoid_prime():
	assert sigmoid_prime(0) == 0.25


def test_base_10_to_n_str():
	assert int(base10ToNStr(10, 3)) == 101


def test_base_10_to_n():
	assert base10ToN(140, 3) == 12012

