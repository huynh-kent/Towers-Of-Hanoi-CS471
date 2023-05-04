
import copy

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
        temp = copy.deepcopy(self.towers)
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
    # game = Game(3, 5)
    # print(game)
    # game.move(0,1)
    # print(game)
    # valid_moves = game.get_valid_moves()
    # print(valid_moves)
    game = Game(3,5)
    print(game)
    frontier = [copy.deepcopy(game.towers)]
    # print(frontier)
    # print(game.get_valid_moves())
    while not game.is_finished():
        valid_moves = game.get_valid_moves()
        #print(valid_moves)
        #print(f'frontier {frontier}')
        while len(valid_moves) == 0:
            #print(f'frontier before pop {frontier}')
            #print(f'prev moves {game.prev_moves.pop()}')
            game.towers = frontier.pop()
            #print(f'pop frontier {frontier} game {game.towers}')
            valid_moves = game.get_valid_moves()
            
        next_move = valid_moves[0]

        game.move(next_move[0], next_move[1])
        frontier.append(copy.deepcopy(game.towers))
        print(game)
        print(game.prev_moves)