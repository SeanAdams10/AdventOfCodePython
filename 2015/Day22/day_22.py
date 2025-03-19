from functools import cache
from utils import get_input_data

class Player:
    def __init__(self, hp, dmg, armor, mana):
        self.hp = hp
        self.dmg = dmg
        self.armor = armor
        self.mana = mana
        self.mana_spent = 0
        self.shield_timer = 0
        self.poison_timer = 0
        self.recharge_timer = 0


    def copy(self):
        tmp = Player(self.hp, self.dmg, self.armor, self.mana)
        tmp.shield_timer = self.shield_timer
        tmp.poison_timer = self.poison_timer
        tmp.recharge_timer = self.recharge_timer
        tmp.mana_spent = self.mana_spent
        return tmp


    def __str__(self):
        return f"Player: HP: {self.hp}, DMG: {self.dmg}, ARMOR: {self.armor}, MANA: {self.mana}, MANA SPENT: {self.mana_spent}, SHIELD TIMER: {self.shield_timer}, POISON TIMER: {self.poison_timer}, RECHARGE TIMER: {self.recharge_timer}"

    def __repr__(self):
        return self.__str__()

    def attack(self, target):
        target.hp -= self.dmg

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return (
            self.hp == other.hp and
            self.dmg == other.dmg and
            self.armor == other.armor and
            self.mana == other.mana and
            self.mana_spent == other.mana_spent and
            self.shield_timer == other.shield_timer and
            self.poison_timer == other.poison_timer and
            self.recharge_timer == other.recharge_timer 
        )

    def __hash__(self):
        return hash((
            self.hp,
            self.dmg,
            self.armor,
            self.mana,
            self.mana_spent,
            self.shield_timer,
            self.poison_timer,
            self.recharge_timer
        ))

def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    hp = int(data[0].split(": ")[1].strip())
    dmg = int(data[1].split(": ")[1].strip())
    armor = 0
    mana = 0
    return Player(hp, dmg, armor, mana)

@cache
def create_player_moves_2(player, boss, move_type, hard_mode):
    spells = []
    result = []
    if hard_mode:
        player.hp -= 1
        if player.hp <= 0:
            return []
    
    if player.mana >= 53:
        spells.append("missile")
    if player.mana >= 73:
        spells.append("drain")
    if player.mana >= 113 and player.shield_timer <= 1:
        spells.append("shield")
    if player.mana >= 173 and player.poison_timer <=1:
        spells.append("poison")
    if player.mana >= 229 and player.recharge_timer <=1:
        spells.append("recharge")

    for move in spells:
        n_player = player.copy()
        n_boss = boss.copy()
        n_move_type = not move_type

        #Run effects first
        if n_player.poison_timer > 0:
            n_boss.hp -= 3
            n_player.poison_timer -= 1
        if n_player.recharge_timer > 0:
            n_player.mana += 101
            n_player.recharge_timer -= 1
        if n_player.shield_timer > 0:
            n_player.armor = 7
            n_player.shield_timer -= 1

        #Then run the player attack
        if move == "missile":
            n_player.mana -= 53
            n_player.mana_spent += 53
            n_boss.hp -= 4
        elif move == "drain":
            n_player.mana -= 73
            n_player.mana_spent += 73
            n_player.hp += 2
            n_boss.hp -= 2
        elif move == "shield":
            n_player.mana -= 113
            n_player.mana_spent += 113
            n_player.shield_timer = 6
        elif move == "poison":
            n_player.mana -= 173
            n_player.mana_spent += 173
            n_player.poison_timer = 6
        elif move == "recharge":
            n_player.mana -= 229
            n_player.mana_spent += 229
            n_player.recharge_timer = 5
        else:
            print("Unknown move")

        if n_player.hp < 0:
            continue
        result.append((n_player, n_boss,  n_move_type, hard_mode))

    return result


@cache
def create_boss_moves_2(player, boss,move_type, hard_mode):
    result = []
    #boss move

    if hard_mode:
        player.hp -= 1
        if player.hp <= 0:
            return []


    player.armor = 0
    if player.poison_timer > 0:
        boss.hp -= 3
        player.poison_timer -= 1
    if player.recharge_timer > 0:
        player.mana += 101
        player.recharge_timer -= 1
    if player.shield_timer > 0:
        player.armor = 7
        player.shield_timer -= 1

    player.hp -= max(0, boss.dmg - player.armor)

    result.append((player, boss,  not move_type, hard_mode))

    return result


best_score = float("inf")

@cache
def dfs_2(player, boss, move_type, hard_mode):
    # if player.mana_spent > best_score: return float("inf")
    if boss.hp <=0:
        print(f"Player won with {player.mana_spent} mana spent")
        # best_score = player.mana_spent 
        return player.mana_spent
    if player.hp <= 0:
        print(f"Player lost with {player.mana_spent} mana spent") 
        return float("inf")
    if move_type:
        #player move
        new_moves = create_player_moves_2(player, boss, move_type, hard_mode)
        if new_moves:
            return min([dfs_2(*move) for move in new_moves if move])
        else: 
            return float("inf")
    else:
        #boss move
        new_moves = create_boss_moves_2(player,boss,move_type, hard_mode)
        if new_moves:
            return min([dfs_2(*move) for move in new_moves if move])
        else:
            return float("inf")
        

def part_1(player, boss, hard_mode):
    moves = 0
    move_type = 1
    return dfs_2(player, boss, move_type, hard_mode)



def main():
    data = get_input_data(2015, 22, sample=0)
    boss_master = read_input(data)
    player_master =  Player(50, 0, 0, 500)
    best_score = float("inf")

    part_1_result = part_1(player_master, boss_master, False)
    print(f"Part 1: {part_1_result}")
    print('*'*20)


    player_master =  Player(50, 0, 0, 500)
    best_score = float("inf")

    part_1_result = part_1(player_master, boss_master, True)
    print(f"Part 2: {part_1_result}")
    print('*'*20)




    # #case 1
    # boss_master = Player(13,8,0,0)
    # player_master =  Player(10, 0, 0, 250)
    # #Expected result is 226
    # part_1_result = part_1(player_master, boss_master)
    # print(f'example 1: {part_1_result}')
    # assert part_1_result == 226, f"Expected 226, got {part_1_result}"
    
    # #Example case 2
    # #case 1
    # boss_master = Player(14,8,0,0)
    # player_master =  Player(10, 0, 0, 250)
    # #Expected result is 641
    # part_1_result = part_1(player_master, boss_master)
    # print(f'example 2: {part_1_result}')
    # assert part_1_result == 641, f"Expected 641, got {part_1_result}"
    

if __name__ == "__main__":
    main()
