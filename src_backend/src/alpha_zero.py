import sys
sys.path.append('C:\\Users\\Francesco\\Documents\\2_Schule\\HYU\\HYU-software-engineering-AI\\src_backend\\src\\ai_modules\\AlphaZero_Connect4\\src\\')


import os
import json
import torch
import encoder_decoder_c4 as ed
from alpha_net_c4 import ConnectNet
from copy import deepcopy
from connect_board import board as cboard
from MCTS_c4 import UCT_search, do_decode_n_move_pieces, get_policy
import copy
import numpy as np


ROW_COUNT = 6
COLUMN_COUNT = 7

EMPTY = ' '
PLAYER_PIECE = 'O'
AI_PIECE = 'X'


def convert_matrix_to_alpha_zero(inJeu):
	move_count = 0
	data_1 = deepcopy(inJeu)
	for a in range(ROW_COUNT):
		for b in range(COLUMN_COUNT):
			if inJeu[a][b] == 'red':
				move_count += 1
				data_1[a][b] = AI_PIECE
			if inJeu[a][b] == 'black':
				move_count += 1
				data_1[a][b] = PLAYER_PIECE
			if not inJeu[a][b]:
				data_1[a][b] = EMPTY

	return move_count, data_1

def find_which_move_ai_made(gameBefore, gameAfter):
	for a in range(ROW_COUNT):
		for b in range(COLUMN_COUNT):
			if gameBefore[a][b] != gameAfter[a][b]:
				return a, b

	return None, None


def play_ia(game, options):

	made_moves, convertedMatrix = convert_matrix_to_alpha_zero(game)

	print(convertedMatrix)

	#########################################################################
	# AlphaZero
	#########################################################################
	
	best_net="c4_current_net_trained2_iter7.pth.tar"
	best_net_filename = os.path.join("C:\\Users\\Francesco\\Documents\\2_Schule\\HYU\\HYU-software-engineering-AI\\src_backend\\src\\ai_modules\\AlphaZero_Connect4\\src\\model_data\\", best_net)
	best_cnet = ConnectNet()
	cuda = torch.cuda.is_available()
	if cuda:
		best_cnet.cuda()
	best_cnet.eval()
	checkpoint = torch.load(best_net_filename)
	best_cnet.load_state_dict(checkpoint['state_dict'])
	
	net = best_cnet

	white = None
	black = net
	current_board = cboard()
	current_board.current_board = np.array(convertedMatrix)

	checkmate = False
	dataset = []
	value = 0; t = 0.1; moves_count = made_moves

	moves_count += 1
	dataset.append(copy.deepcopy(ed.encode_board(current_board)))

	print("AI is thinking.............")
	root = UCT_search(current_board,777,black,t)
	policy = get_policy(root, t)

	current_board = do_decode_n_move_pieces(current_board, np.random.choice(np.array([0,1,2,3,4,5,6]), p = policy)) # decode move and move piece(s)

	print(current_board.current_board); print(" ")

	return find_which_move_ai_made(convertedMatrix, current_board.current_board)
	