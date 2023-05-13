from copy import deepcopy

class Game:
    def __init__(self, towers, disks):
        self.towers = [[] for tower in range(towers)]   # create towers
        self.prev_moves = []
        self.num_disks = disks
        self.g = 0
        self.h = 0
        self.f = 0
        
        # add disks to first tower
        for i in range(disks):
            #self.towers[0].append(chr(ord('A') + i))
            self.towers[0].append(str(i+1))

        # add beginning state to prev_moves
        key = []
        for i, tower in enumerate(self.towers):
            key.append(''.join(self.towers[i]))
        self.prev_moves.append('|'.join(key))

    # calculate heuristic h (number of disks in starting tower - number of disks in last tower)
    def calc_h(self):
        h = len(self.towers[0])+(self.num_disks-len(self.towers[-1]))
        return h

    # move disk from old tower to new tower
    def move(self, old_tower, new_tower):
        self.towers[new_tower].insert(0, self.towers[old_tower].pop(0))
        move_hash = self.compute_hash(old_tower,new_tower)
        self.prev_moves.append(move_hash)                       # add move to prev_moves
        
    # get valid moves from current state
    def get_valid_moves(self):
        valid_moves = []
        for i, old_tower in enumerate(self.towers):
            if not old_tower:                                    # if tower is empty skip
                continue
            for j, new_tower in enumerate(self.towers):          # for other towers
                if not new_tower or old_tower[0] < new_tower[0]: # if new tower is empty or top disk is smaller, valid move
                    key = self.compute_hash(i,j)
                    if key not in self.prev_moves:               # if move is a new state, add to valid moves
                        valid_moves.append((i,j))
        return valid_moves
    
    # compute hash for move
    def compute_hash(self, old_tower=None, new_tower=None):
        temp = deepcopy(self.towers)
        if temp[old_tower] and temp[old_tower] < temp[new_tower] or not temp[new_tower]:
             temp[new_tower].insert(0, temp[old_tower].pop(0))
        key = []
        for i, tower in enumerate(temp):
            key.append(''.join(temp[i]))
        return '|'.join(key)
    
    # check if game is finished
    def is_finished(self):
        if len(self.towers[-1]) == self.num_disks:
            return True
        
    # print and write shortest path to output.txt
    def print_path(self):
        print(str(self.prev_moves).replace("'",'').replace(',', ' -->').replace('[','').replace(']',''))
        with open('output.txt', 'w') as f:
            for move in self.prev_moves:
                f.write(move + '\n')

    # print towers    
    def __repr__(self):
        key = []
        for i, tower in enumerate(self.towers):
            key.append(''.join(self.towers[i]))
        return '|'.join(key)
        #return str(self.towers)
    
# get state with lowest f from open list
def get_lowest_f(open_list):
    lowest_f = min(open_list, key=lambda state: state.f)
    return lowest_f

# main
if __name__ == '__main__':
    # ### first valid move algorithm ###
    # game = Game(3,5)
    # print(game)
    # frontier = [deepcopy(game.towers)]
    # # print(frontier)
    # # print(game.get_valid_moves())
    # while not game.is_finished():
    #     valid_moves = game.get_valid_moves()
    #     #print(valid_moves)
    #     #print(f'frontier {frontier}')
    #     while len(valid_moves) == 0:
    #         #print(f'frontier before pop {frontier}')
    #         #print(f'prev moves {game.prev_moves.pop()}')
    #         game.towers = frontier.pop()
    #         #print(f'pop frontier {frontier} game {game.towers}')
    #         valid_moves = game.get_valid_moves()
            
    #     next_move = valid_moves[0]

    #     game.move(next_move[0], next_move[1])
    #     frontier.append(deepcopy(game.towers))
    #     print(game)
    #     print(game.prev_moves)

    ### a* move algorithm ###
    # init game
    game = Game(3,3)
    open_list, closed_list = [], []
    open_list.append(game)
    while open_list:
        print(f'Frontier: {open_list}')
        # find state with lowest f on open list
        main_state = get_lowest_f(open_list)
        print(f'Current State (Lowest F): {main_state} f: {main_state.f}')
        # remove state from open list
        open_list.remove(main_state)

        # generate possible new states from main state
        possible_states = []
        for valid_move in main_state.get_valid_moves():
            new_state = deepcopy(main_state)
            new_state.move(valid_move[0], valid_move[1])
            possible_states.append(new_state)

        # check if possible states have lower f, if so add to open list
        for state in possible_states:
            # if state is goal, stop search
            if state.is_finished():
                print("Finished Search, Shortest Path:")
                state.print_path()
                exit()
                
            # compute f for possible state
            else: 
                state.g = main_state.g + 1
                state.h = state.calc_h()
                state.f = state.g + state.h
                print(f'Next State: {state} g: {state.g} h: {state.h} f: {state.f}')

            skip = False
            # if state with same position as possible state is in open list
            # and has lower f than possible state, skip
            for open_state in open_list:
                if open_state.towers == state.towers and open_state.f < state.f:
                    skip = True
            # if state with same position as possible state is in closed list
            # and has lower f than possible state, skip
            for closed_state in closed_list:
                if closed_state.towers == state.towers and closed_state.f < state.f:
                    skip = True
            if skip: continue
            # add possible state to open list
            else: open_list.append(state)
        # push main state on closed list
        closed_list.append(main_state)
        print()
    # end while loop
                
"""
a* notes
f(n) = g(n) + h(n)
g is measure of cost to reach node n
h is estimate of cost to reach goal from n
f(x) = g(x) + h(x)
hx = number of disks in wrong tower in state X
gx = depth of node X in search tree

# a* pseudocode
# initialize open list
# initialize closed list
# put start node on open list (leave f at zero)
# while open list is not empty
#     find node with least f on open list, call it q
#     pop q off the open list
#     generate q's 8 successors and set their parents to q
#     for each successor
#         if successor is the goal, stop search
#         else compute g and h for successor
#             successor.g = q.g + distance between successor and q
#             successor.h = distance from goal to successor
#             successor.f = successor.g + successor.h
#         if a node with the same position as successor is in the OPEN list
#             which has a lower f than successor, skip this successor
#         if a node with the same position as successor is in the CLOSED list
#             which has a lower f than successor, skip this successor
#         else add the node to the open list
#     end for loop
#     push q on the closed list
# end while loop
"""