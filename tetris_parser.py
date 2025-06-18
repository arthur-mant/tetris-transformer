from tetris_game import definitions
from copy import deepcopy

def get_afterstate(original_board, piece, action):
    board = deepcopy(original_board)
    for block in definitions.pieces[piece][action[2]]:
        i = block//4
        j = block%4

        board[action[0]+i][action[1]+j] = 1
    lines = 0
    for i in range(action[0], min(action[0]+4, 20)):
        is_complete = True
        for j in range(len(board[i])):
            if board[i][j] == 0:
                is_complete = False
                break
        if is_complete:
            lines += 1
            for k in range(i, 0, -1):
                for l in range(len(board[i])):
                    board[k][l] = board[k-1][l]

    return board, lines

def get_possible_actions(board, piece):
    actions = []
    for x in range(len(board)):
        for y in range(-2, len(board[x])):
            for rot in range(len(definitions.pieces[piece])):
                is_floating = True
                is_invalid = False
                for block in definitions.pieces[piece][rot]:
                    i = block//4
                    j = block%4
                    if (x+i < 0) or (x+i >= len(board)) or (y+j < 0) or (y+j >= len(board[x])):
                        is_invalid = True
                        break
                    if board[x+i][y+j] == 1:
                        is_invalid = True
                        break
                    if (x+i+1 >= len(board)) or (board[x+i+1][y+j] == 1):
                        is_floating = False
                if not is_invalid and not is_floating:
                    actions.append([x, y, rot])
    return actions


def slice_board(board):
    slices = []
    for i in range(len(board)-3):
        for j in range(len(board[i])-3):
            aux = []
            for k in range(4):
                for l in range(4):
                    aux.append(board[i+k][j+l])
            slices.append(aux)
    return slices

def encode_state(board, piece, next_piece, action):
    afterstate, lines = get_afterstate(board, piece, action)
    slices = slice_board(afterstate)
    state = [next_piece]
    for sl in slices:
        multiplier = 1
        cumsum = 0
        for elem in sl:
            cumsum += elem*multiplier
            multiplier *= 2
        state.append(cumsum)
    return state, lines

def get_all_afterstates_encodings(board, piece, next_piece):
    afterstate_encodings = []
    actions = get_possible_actions(board, piece)
    for action in actions:
        afterstate_encodings.append(encode_state(board, piece, next_piece, action))
    return afterstate_encodings

#for testing only
if __name__ == '__main__':
    import pickle
    import sys
    import random

    cols = 10
    def print_board(board):
        for i in range(len(board)):
            aux = str(i)+"|"
            if len(str(i)) < 2:
                aux = "0"+aux
            for elem in board[i]:
                aux += str(elem)
            print(aux, "|")
        aux = ""
        for _ in range(cols+5):
            aux += "-"
        print(aux)
        aux = "   "
        for j in range(cols):
            aux += str(j)
        print(aux)

    filename = sys.argv[1]
    f = open(filename, "rb")
    plays = pickle.load(f)
    play = random.choice(plays)

    print_board(play["board"])
    print("Piece: ", definitions.piece_vector[play["piece"]])
    print("Next Piece: ", definitions.piece_vector[play["next_piece"]])
    print("Action: ", play["action"])
    print("Lines Cleared: ", play["lines_cleared"])

    new_board = get_afterstate(play["board"], play["piece"], play["action"])[0]
    print_board(new_board)

    possible_actions = get_possible_actions(play["board"], play["piece"])

    #print(possible_actions)
    #for a in possible_actions:
    #    print_board(get_afterstate(play["board"], play["piece"], a)[0])

    slices = slice_board(new_board)
    encodes = encode_state(play["board"], play["piece"], play["next_piece"], play["action"])
    print("encode[0]: ", encodes[0][0])

    for s in range(len(slices)):
        print("\n", s//7, s%7, encodes[0][1+s])
        for i in range(4):
            cum_str = ""
            for j in range(4):
                cum_str += str(slices[s][4*i+j])
            print(cum_str)
        


    encodings = get_all_afterstates_encodings(play["board"], play["piece"], play["next_piece"])
    print(encodings)    




