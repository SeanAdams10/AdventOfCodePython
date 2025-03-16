from time import perf_counter
from utils import get_input_data, timing_decorator
from copy import deepcopy

class Player:
    def __init__(self, hp, dmg, armor, mana):
        self.hp = hp
        self.dmg = dmg
        self.armor = armor
        self.mana = mana
        self.effects = []
        self.mana_spent = 0
        self.shield_timer = 0
        self.poison_timer = 0
        self.recharge_timer = 0
        self.victory = False
        self.moves = 0

    def __str__(self):
        return f"Player: HP: {self.hp}, DMG: {self.dmg}, ARMOR: {self.armor}, MANA: {self.mana}"

    def __repr__(self):
        return self.__str__()

    def attack(self, target):
        target.hp -= self.dmg


def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    hp = int(data[0].split(": ")[1].strip())
    dmg = int(data[1].split(": ")[1].strip())
    armor = 0
    mana = 0
    return Player(hp, dmg, armor, mana)

def get_moves(player, boss):
    moves = []
    if player.mana >= 53:
        moves.append("missile")
    if player.mana >= 73:
        moves.append("drain")
    if player.mana >= 113 and player.shield_timer == 0:
        moves.append("shield")
    if player.mana >= 173 and player.poison_timer == 0:
        moves.append("poison")
    if player.mana >= 229 and player.recharge_timer == 0:
        moves.append("recharge")

    new_players = []
    for move in moves:
        n_player = deepcopy(player)
        n_player.armor = 0
        n_boss = Player(boss.hp, boss.dmg, boss.armor, boss.mana)

        if n_player.poison_timer > 0:
            n_boss.hp -= 3
            n_player.poison_timer -= 1
        if n_player.recharge_timer > 0:
            n_player.mana += 101
            n_player.recharge_timer -= 1
        if n_player.shield_timer > 0:
            n_player.armor = 7
            n_player.shield_timer -= 1


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

        n_player.victory = n_boss.hp <= 0

        #boss move
        if n_player.poison_timer > 0:
            n_boss.hp -= 3
            n_player.poison_timer -= 1
        if n_player.recharge_timer > 0:
            n_player.mana += 101
            n_player.recharge_timer -= 1
        if n_player.shield_timer > 0:
            n_player.armor = 7
            n_player.shield_timer -= 1

        n_player.hp -= max(0, n_boss.dmg - n_player.armor)
        n_player.moves += 1

        n_boss.victory = n_player.hp <= 0
        n_player.victory = n_boss.hp <= 0

        new_players.append([n_boss,n_player, n_player.mana_spent, n_boss.hp, n_player.mana_spent + n_boss.hp ])

    return new_players
    


def part_1(boss, player):
    candidates = [[boss, player, 0,0,0],]
    moves = 0
    while candidates:
        candidates = sorted(candidates, key=lambda x: x[4])
        boss, player, mana_spent, boss_hp, score = candidates.pop(0)
        if player.victory:
            return mana_spent
        elif boss.victory:
            #the boss won - no point in carrying on down this route
            continue

        moves += 1
        if moves % 100 == 0:
            print(f"Moves: {moves}, Score: {score}, Mana: {mana_spent}, Boss HP: {boss_hp}, player HP: {player.hp}, player moves: {player.moves}, candidates: {len(candidates)}")
        new_candidates = get_moves(player, boss)
        candidates.extend(new_candidates)


    return None        
        








def main():
    data = get_input_data(2015, 22, sample=0)
    boss_master = read_input(data)
    player_master =  Player(50, 0, 0, 500)

    part_1_result = part_1(boss_master, player_master)
    print(f"Part 1: {part_1_result}")

if __name__ == "__main__":
    main()
