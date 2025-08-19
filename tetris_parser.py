from tetris_game import definitions
import torch
import time

def print_board(board):
    for i in range(len(board)):
        aux = str(i)+"|"
        if len(str(i)) < 2:
            aux = "0"+aux
        for elem in board[i]:
            aux += str(elem)
        print(aux, "|")
    aux = ""
    for _ in range(definitions.n_cols+5):
        aux += "-"
    print(aux)
    aux = "   "
    for j in range(definitions.n_cols):
        aux += str(j)
    print(aux)

def get_afterstate(original_board, piece, action):
    #board = deepcopy(original_board)
    board = []
    for i in original_board:
        aux = []
        for j in i:
            aux.append(j)
        board.append(aux)
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
    #print(board, piece)
    actions = []
    for y in range(-2, len(board)):
        for x in range(-2, len(board[0])):
            for rot in range(len(definitions.pieces[piece])):
                is_floating = True
                is_invalid = False
                for block in definitions.pieces[piece][rot]:
                    i = block//4
                    j = block%4
                    if (y+i >= len(board)) or (x+j < 0) or (x+j >= len(board[0])):
                        is_invalid = True
                        break
                    if (y+i) >= 0 and board[y+i][x+j] == 1:
                        is_invalid = True
                        break
                    if y+i+1 >= 0 and ((y+i+1 >= len(board)) or (board[y+i+1][x+j] == 1)):
                        is_floating = False
                if not is_invalid and not is_floating:
                    actions.append([y, x, rot])
    return actions


def encode_state(board, piece, next_piece, action):
    afterstate, lines = get_afterstate(board, piece, action)
    state = [next_piece]
    for i in range(len(board)-3):
        for j in range(len(board[i])-3):
            multiplier = 1
            cumsum = 0
            for k in range(4):
                for l in range(4):
                    cumsum += board[i+k][j+l]*multiplier
                    multiplier *= 2
            state.append(cumsum)
    return torch.tensor(state, dtype=torch.float, requires_grad=False), lines

def no_encode_state(board, piece, next_piece, action):
    afterstate, lines = get_afterstate(board, piece, action)
    state = [next_piece]
    for aux in afterstate:
        state += aux
    return torch.tensor(state, dtype=torch.float, requires_grad=False), lines

def generate_afterstate(board, piece, next_piece, action, use_encoding):
    if use_encoding:
        afterstate, lines = encode_state(board, piece, next_piece, action) 
    else:
        afterstate, lines = no_encode_state(board, piece, next_piece, action)
    gameover = False
    for i in range(0, 2):
        for j in range(3, 7):
            if afterstate[i*definitions.n_cols+j] == 1:
                gameover = True
    return afterstate, lines, gameover

def get_all_afterstates(board, piece, next_piece, use_encoding):
    afterstates = []
    compleated_lines = []
    gameovers = []
    actions = get_possible_actions(board, piece)
    for action in actions:
        afterstate, lines, gameover = generate_afterstate(board, piece, next_piece, action, use_encoding)
        afterstates.append(afterstate)
        compleated_lines.append(lines)
        gameovers.append(gameover)
    return actions, torch.stack(afterstates), compleated_lines, gameovers

def intersect(board, piece, y, x, rot):
    for block in definitions.pieces[piece][rot]:
        i = block//4
        j = block%4
        if y <-2:
            return True
        elif y+i < 0:
            pass
        elif x+j < 0 or y+i >= definitions.n_rows or x+j >= definitions.n_cols or board[y+i][x+j] == 1:
            return True
    return False

def simple_move(board, piece, y, x, rot):
    pos = [y, x, rot]
    route = []
    while pos[0] > 0:
        pos[0] -= 1
        if intersect(board, piece, pos[0], pos[1], pos[2]):
            return None
        route.append("B")
    while pos[1] < (definitions.n_cols//2)-2:
        pos[1] += 1
        if intersect(board, piece, pos[0], pos[1], pos[2]):
            return None
        route.append("E")
    while pos[1] > (definitions.n_cols//2)-2:
        pos[1] -= 1
        if intersect(board, piece, pos[0], pos[1], pos[2]):
            return None
        route.append("D")
    while pos[2] > 0:
        pos[2] -= 1
        if intersect(board, piece, pos[0], pos[1], pos[2]):
            return None
        route.append("R")
    while pos[0] > -2:
        pos[0] -= 1
        if intersect(board, piece, pos[0], pos[1], pos[2]):
            return None
        route.append("B")
    return route

def get_route(board, piece, y, x, rot, route, visited):
    if (y, x, rot) in visited or intersect(board, piece, y, x, rot):
        return None
    #print(y, x, rot)
    visited.append((y, x, rot))
    s_move = simple_move(board, piece, y, x, rot)
    if s_move != None:
        return list(reversed(route+s_move))

    new_route = get_route(board, piece, y-1, x, rot, route+["B"], visited)
    if new_route != None:
        return new_route

    is_redundant = False
    for elem in reversed(route):
        if elem == "B" or elem == "E":
            break
        if elem == "D":
            is_redundant = True
    if not is_redundant:
        new_route = get_route(board, piece, y, x+1, rot, route+["E"], visited)
        if new_route != None:
            return new_route

    is_redundant = False
    for elem in reversed(route):
        if elem == "B" or elem == "D":
            break
        if elem == "E":
            is_redundant = True
    if not is_redundant:
        new_route = get_route(board, piece, y, x-1, rot, route+["D"], visited)
        if new_route != None:
            return new_route
    rot_count = 0 
    for elem in reversed(route):
        if elem == "B" or elem == "D" or elem == "E":
            break
        if elem == "R":
            rot_count += 1
    if rot_count+1 < len(definitions.pieces[piece]):
        new_route = get_route(board, piece, y, x, (rot-1)%len(definitions.pieces[piece]), route+["R"], visited)
        if new_route != None:
            return new_route
    return None
    

#for testing only
if __name__ == '__main__':
    import pickle
    import sys
    import random

    filename = sys.argv[1]
    f = open(filename, "rb")
    games = pickle.load(f)
    game = random.choice(games)

    for play in game:
        print("---------------------------------------------------")
        print_board(play["board"])
        print("Piece: ", definitions.piece_vector[play["piece"]])
        print("Next Piece: ", definitions.piece_vector[play["next_piece"]])
        print("Action: ", play["action"])
        print("Lines Cleared: ", play["lines_cleared"])

        new_board = get_afterstate(play["board"], play["piece"], play["action"])[0]
        print_board(new_board)

        print(get_route(play["board"], play["piece"], play["action"][0], play["action"][1], play["action"][2], [], []))

        enc_state = encode_state(play["board"], play["piece"], play["next_piece"], play["action"])
        print(enc_state)
