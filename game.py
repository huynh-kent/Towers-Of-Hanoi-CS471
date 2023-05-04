
from copy import deepcopy

class Game:
    def __init__(self, towers, disks):
        self.towers = [[] for tower in range(towers)]   # create towers
        self.prev_moves = []
        self.num_disks = disks
        
        # add disks to first tower
        for i in range(disks):
            #self.towers[0].append(chr(ord('A') + i))
            self.towers[0].append(str(i+1))

    def move(self, old_tower, new_tower):
        if not self.towers[old_tower]:
            print("No disks in old_tower")
            return False
        elif self.towers[new_tower] and self.towers[old_tower][0] > self.towers[new_tower][0]:
            print("Disk in new_tower is smaller than old_tower")
            return False
        else:
            self.towers[new_tower].insert(0, self.towers[old_tower].pop(0))
            move_hash = self.compute_hash(new_tower,old_tower)
            self.prev_moves.append(move_hash)
            return True
        
    # get valid moves from current state
    def get_valid_moves(self):
        valid_moves = []
        for i, old_tower in enumerate(self.towers):
            if not old_tower:   # if tower is empty skip
                continue
            for j, new_tower in enumerate(self.towers): # other towers
                if not new_tower or old_tower[0] < new_tower[0]: # if new tower is empty or top disk is smaller, valid move
                    key = self.compute_hash(i,j)
                    if key not in self.prev_moves:
                        valid_moves.append((i,j))
                    #self.prev_moves.append(key)
        return valid_moves
    
    def compute_hash(self, old_tower=None, new_tower=None):
        temp = deepcopy(self.towers)
        #print(f'temp copy {temp}')
        if old_tower:
            temp[new_tower].insert(0, temp[old_tower].pop(0))
        key = []
        for i, tower in enumerate(temp):
            key.append(''.join(temp[i]))
            #if not tower: key.append('x')
        return '|'.join(key)
    
    def is_finished(self):
        if len(self.towers[-1]) == self.num_disks:
            return True

        
    def __repr__(self):
        return str(self.towers)
    

if __name__ == '__main__':
    game = Game(3, 5)
    print(game)
    game.move(0,1)
    print(game)
    valid_moves = game.get_valid_moves()
    print(valid_moves)

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

"""
a* notes
f(n) = g(n) + h(n)
g is measure of cost to reach node n
h is estimate of cost to reach goal from n
f(x) = g(x) + h(x)
hx = number of disks in wrong tower in state X
gx = depth of node X in search tree

initialize open list
initialize closed list
put start node on open list (leave f at zero)
while open list is not empty
    find node with least f on open list, call it q
    pop q off the open list
    generate q's 8 successors and set their parents to q
    for each successor
        if successor is the goal, stop search
        else compute g and h for successor
            successor.g = q.g + distance between successor and q
            successor.h = distance from goal to successor
            successor.f = successor.g + successor.h
        if a node with the same position as successor is in the OPEN list
            which has a lower f than successor, skip this successor
        if a node with the same position as successor is in the CLOSED list
            which has a lower f than successor, skip this successor
        else add the node to the open list
    end for loop
    push q on the closed list
end while loop
"""