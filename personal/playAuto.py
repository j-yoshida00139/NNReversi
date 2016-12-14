import sys, os
import game
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
import network

n_input = 192 #366
n_neutral_neuron = 100
n_output = 64 #12

size = [n_input, n_neutral_neuron, n_output]
net = network.Network(size)

game = game.Game(8,8)
game.initialize()

while game.canPutPieceOnBoard(game.WHITE) or game.canPutPieceOnBoard(game.BLACK):
    arrangeList = game.returnNnInputList(game.arrange, game.nextColor)
    move = net.feedforward(arrangeList) #move[0][0:63]
    index = np.argmax(move[0]*game.getCanPutList(game.nextColor))
    row, col = divmod(index, 8)

    game.storeMove(row, col, game.nextColor)
    game.putPiece(row, col, game.nextColor)

    turnPieceList = game.getTurnPieceList(row, col, game.nextColor)
    game.turnPiece(turnPieceList, game.nextColor)
    game.goNextTurn()

print(game.getWinnersData())
game.storeWinnersData(game.getWinnersData())