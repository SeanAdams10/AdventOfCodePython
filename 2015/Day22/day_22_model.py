def find_min_mana_to_win(player_hp, player_mana, boss_hp, boss_damage, hard_mode=False):
    # Define spells with their costs and effects
    spells = {
        "Magic Missile": {"cost": 53,  "damage": 4, "heal": 0, "duration": 0, "effect_damage": 0, "effect_mana": 0, "armor": 0},
        "Drain":         {"cost": 73,  "damage": 2, "heal": 2, "duration": 0, "effect_damage": 0, "effect_mana": 0, "armor": 0},
        "Shield":        {"cost": 113, "damage": 0, "heal": 0, "duration": 6, "effect_damage": 0, "effect_mana": 0, "armor": 7},
        "Poison":        {"cost": 173, "damage": 0, "heal": 0, "duration": 6, "effect_damage": 3, "effect_mana": 0, "armor": 0},
        "Recharge":      {"cost": 229, "damage": 0, "heal": 0, "duration": 5, "effect_damage": 0, "effect_mana": 101, "armor": 0},
    }
    # Global best mana found
    best_mana = float('inf')
    # Memoization for visited states: {(player_hp, boss_hp, player_mana, shield_timer, poison_timer, recharge_timer): min_mana_spent}
    seen = {}
    
    def dfs(player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer, mana_spent):
        nonlocal best_mana
        # Prune branch if mana spent so far exceeds known best
        if mana_spent >= best_mana:
            return
        # Hard mode: subtract 1 HP at start of player's turn
        if hard_mode:
            player_hp -= 1
            if player_hp <= 0:
                return  # player dies before doing anything
        # Apply effects at start of player turn
        armor = 0
        if shield_timer > 0:   # Shield effect active
            armor = 7
            shield_timer -= 1
        if poison_timer > 0:   # Poison effect active
            boss_hp -= 3
            poison_timer -= 1
        if recharge_timer > 0: # Recharge effect active
            player_mana += 101
            recharge_timer -= 1
        # Check if boss died from effects
        if boss_hp <= 0:
            best_mana = min(best_mana, mana_spent)
            return
        # State key after applying effects (start of player's action)
        state = (player_hp, boss_hp, player_mana, shield_timer, poison_timer, recharge_timer)
        if state in seen and seen[state] <= mana_spent:
            return  # already visited this state with equal or lower mana cost
        seen[state] = mana_spent
        # Try all possible spells
        for name, spell in spells.items():
            # Skip if not enough mana to cast
            if player_mana < spell["cost"]:
                continue
            # Skip if spell's effect is already active
            if spell["duration"] > 0:
                if (name == "Shield" and shield_timer > 0) or \
                   (name == "Poison" and poison_timer > 0) or \
                   (name == "Recharge" and recharge_timer > 0):
                    continue
            # Simulate casting this spell
            new_player_hp = player_hp
            new_player_mana = player_mana - spell["cost"]
            new_boss_hp = boss_hp
            new_shield_timer = shield_timer
            new_poison_timer = poison_timer
            new_recharge_timer = recharge_timer
            new_mana_spent = mana_spent + spell["cost"]
            # Apply immediate effects of the spell
            new_boss_hp -= spell["damage"]
            new_player_hp += spell["heal"]
            if spell["duration"] > 0:
                # Start a new effect (set its timer)
                if name == "Shield":
                    new_shield_timer = spell["duration"]
                elif name == "Poison":
                    new_poison_timer = spell["duration"]
                elif name == "Recharge":
                    new_recharge_timer = spell["duration"]
            # After player's spell, check if boss is dead
            if new_boss_hp <= 0:
                best_mana = min(best_mana, new_mana_spent)
                continue  # boss defeated, try next spell option
            # Boss's turn begins – apply effects
            armor_effect = 0
            if new_shield_timer > 0:
                armor_effect = 7
                new_shield_timer -= 1
            if new_poison_timer > 0:
                new_boss_hp -= 3
                new_poison_timer -= 1
            if new_recharge_timer > 0:
                new_player_mana += 101
                new_recharge_timer -= 1
            # Check if boss died from effects at start of boss turn
            if new_boss_hp <= 0:
                best_mana = min(best_mana, new_mana_spent)
                continue
            # Boss attacks the player
            damage = boss_damage - armor_effect
            if damage < 1:
                damage = 1  # boss attack always deals at least 1
            new_player_hp -= damage
            # Check if player survives the attack
            if new_player_hp > 0:
                # Continue with next round (player's turn)
                dfs(new_player_hp, new_player_mana, new_boss_hp,
                    new_shield_timer, new_poison_timer, new_recharge_timer,
                    new_mana_spent)
            # (If player_hp <= 0, the branch ends in failure, no recursive call)
    
    # Start DFS from the initial state (player's turn before any actions)
    dfs(player_hp, player_mana, boss_hp, 0, 0, 0, 0)
    return best_mana



# Example usage:
boss_hit_points = 58
boss_damage = 9
print(find_min_mana_to_win(50, 500, boss_hit_points, boss_damage, hard_mode=False))  # Normal mode result
print(find_min_mana_to_win(50, 500, boss_hit_points, boss_damage, hard_mode=True))   # Hard mode result


# #Case 1
# print ('Example case 1')
# boss_hit_points = 13
# boss_damage = 8
# print(find_min_mana_to_win(10, 250, boss_hit_points, boss_damage, hard_mode=False))  # Normal mode result

# #Case 1
# print ('Example case 2')
# boss_hit_points = 14
# boss_damage = 8
# print(find_min_mana_to_win(10, 250, boss_hit_points, boss_damage, hard_mode=False))  # Normal mode result



