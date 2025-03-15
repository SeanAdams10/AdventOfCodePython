from time import perf_counter
from utils import get_input_data, timing_decorator
from collections import namedtuple
from itertools import combinations, product

Item = namedtuple('Item', ['name', 'cost', 'damage', 'armor'])

Weapons = [
    Item('Dagger', 8, 4, 0),
    Item('Shortsword', 10, 5, 0),
    Item('Warhammer', 25, 6, 0),
    Item('Longsword', 40, 7, 0),
    Item('Greataxe', 74, 8, 0)
]

Armors = [
    Item('Leather', 13, 0, 1),
    Item('Chainmail', 31, 0, 2),
    Item('Splintmail', 53, 0, 3),
    Item('Bandedmail', 75, 0, 4),
    Item('Platemail', 102, 0, 5)
]

Rings = [
    Item('Damage +1', 25, 1, 0),
    Item('Damage +2', 50, 2, 0),
    Item('Damage +3', 100, 3, 0),
    Item('Defense +1', 20, 0, 1),
    Item('Defense +2', 40, 0, 2),
    Item('Defense +3', 80, 0, 3)
]

def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    hp = int(data[0].split(": ")[1])
    damage = int(data[1].split(": ")[1])
    armor = int(data[2].split(": ")[1])

    return [hp, damage, armor]

def part_1_battle(boss, player):
    # 0 is HP, 1 is damage, 2 is armor
    while True:
        # Player's turn
        damage = player[1] - boss[2]
        boss[0] -= damage
        if boss[0] <= 0:
            return True

        # Boss's turn
        damage = boss[1] - player[2]
        player[0] -= damage
        if player[0] <= 0:
            return False


def part_1_equipment():
    all_combinations = []
    for weapon in Weapons:
        for armor in [None] + Armors:
            for ring_count in range(3):  # 0, 1, or 2 rings
                for rings in combinations(Rings, ring_count):
                    equipment = [weapon]
                    if armor:
                        equipment.append(armor)
                    equipment.extend(rings)
                    all_combinations.append(equipment)

    return all_combinations

def part_1_sumcombos(all_combinations):
    kit_sum = []
    for kit in all_combinations:
        cost = sum(x.cost for x in kit)
        damage = sum(x.damage for x in kit)
        armor = sum(x.armor for x in kit)
        kit_descr = '; '.join(x.name for x in kit)
        kit_sum.append((cost, damage, armor, kit_descr))

    kit_sum = sorted(kit_sum, key=lambda x: x[0])
    return kit_sum



def main():
    data = get_input_data(2015, 21, sample=0)
    boss_orig = read_input(data)
    # boss = [12,7,2]
    # player = [100,5,1]
    # if part_1_battle(boss, player):
    #     print("Player wins")
    # else:
    #     print("Player loses")

    print('starting the run now')

    combinations = part_1_equipment()
    kit_sum = part_1_sumcombos(combinations)
    for kit in kit_sum:
        boss = boss_orig.copy()
        player = [100, kit[1], kit[2]]
        if part_1_battle(boss, player):
            print("Part 1: Player wins with cost", kit[0])
            break
        # else:
        #     print("Player loses with cost", kit[0])

    kit_sum = sorted(kit_sum, key=lambda x: x[0], reverse=True)
    for kit in kit_sum:
        boss = boss_orig.copy()
        player = [100, kit[1], kit[2]]
        if not part_1_battle(boss, player):
            print("Part 2: Player loses with cost", kit[0])
            break
        # else:
        #     print("Player wins with cost", kit[0])

if __name__ == "__main__":
    main()
