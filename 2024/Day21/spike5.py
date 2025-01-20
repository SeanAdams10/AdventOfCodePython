#!/usr/bin/env python3

from collections import deque
from functools import lru_cache
from keypad import Keypad, Dir_Pad

###############################################################################
# 1) DEFINE KEYPAD LAYOUTS
###############################################################################

# Numeric keypad valid positions:
#   (r, c):
#      7(0,0) 8(0,1) 9(0,2)
#      4(1,0) 5(1,1) 6(1,2)
#      1(2,0) 2(2,1) 3(2,2)
#          0(3,1)  A(3,2)
#
pos_to_key_num = {
    (0,0): '7', (0,1): '8', (0,2): '9',
    (1,0): '4', (1,1): '5', (1,2): '6',
    (2,0): '1', (2,1): '2', (2,2): '3',
    (3,1): '0', (3,2): 'A',
}
key_to_pos_num = {k: p for p, k in pos_to_key_num.items()}

# Directional keypad valid positions:
#   (0,1): '^'
#   (0,2): 'A'
#   (1,0): '<'
#   (1,1): 'v'
#   (1,2): '>'
#
pos_to_key_dir = {
    (0,1): '^',
    (0,2): 'A',
    (1,0): '<',
    (1,1): 'v',
    (1,2): '>',
}
key_to_pos_dir = {k: p for p, k in pos_to_key_dir.items()}


###############################################################################
# 2) BUILD BFS DISTANCES AND CANONICAL SHORTEST PATHS
#    For each layout, we'll get:
#       dist_layout[start_key][end_key] = # of steps
#       path_layout[start_key][end_key] = list of moves in {^,<,>,v}
###############################################################################

def build_bfs_and_paths(key_to_pos):
    """
    Given a dict key->(r,c) for a keypad layout, build:
      dist[k1][k2] = minimal # of up/down/left/right moves from k1 to k2
      path[k1][k2] = a canonical minimal path from k1 to k2, as a list of moves in {'^','v','<','>'}
    """
    keys = list(key_to_pos.keys())
    dist = {k: {} for k in keys}
    path = {k: {} for k in keys}

    # reverse mapping (r,c)->key
    pos_to_key = {pos: k for k, pos in key_to_pos.items()}

    valid_positions = set(pos_to_key.keys())

    moves = [(-1,0,'^'), (1,0,'v'), (0,-1,'<'), (0,1,'>')]

    from collections import deque

    for start_key in keys:
        start_pos = key_to_pos[start_key]
        start_r, start_c = start_pos

        # We'll do BFS from (start_r, start_c)
        queue = deque()
        # Enqueue (row, col, distance_so_far, path_so_far)
        queue.append((start_r, start_c, 0, []))
        visited = {(start_r, start_c)}
        found = {}

        while queue:
            r, c, d, path_so_far = queue.popleft()

            # If (r,c) is a valid key => record
            if (r, c) in pos_to_key:
                k2 = pos_to_key[(r, c)]
                # record distance and path
                found[k2] = (d, path_so_far)

            # Explore neighbors
            for (dr, dc, sym) in moves:
                rr, cc = r + dr, c + dc
                if (rr, cc) in valid_positions and (rr, cc) not in visited:
                    visited.add((rr, cc))
                    queue.append((rr, cc, d+1, path_so_far + [sym]))

        # fill in dist[start_key][k2] and path[start_key][k2]
        for k2, (dval, pval) in found.items():
            dist[start_key][k2] = dval
            path[start_key][k2] = pval

    return dist, path

dist_num, path_num = build_bfs_and_paths(key_to_pos_num)
dist_dir, path_dir = build_bfs_and_paths(key_to_pos_dir)


###############################################################################
# 3) TYPE A CODE ON THE NUMERIC KEYPAD (LOWEST LEVEL)
#    Returns the list of lower-level "direction symbols" that represent
#    the minimal pointer-movement + press to type the code.  Each character in
#    the output is one of {'^','v','<','>'} for "move" or 'A' for "press".
###############################################################################

def type_code_on_numeric(code: str) -> list:
    """
    Given a code like '029A', return a list of symbols in {^,v,<,>,A}
    that the numeric keypad's pointer would execute (starting from 'A')
    to produce that code with minimal moves.
    """
    result = []
    pointer = 'A'  # numeric keypad pointer starts on 'A'

    for ch in code:
        # 1) move pointer from pointer -> ch
        move_seq = path_num[pointer][ch]   # list of ^,<,>,v
        result.extend(move_seq)
        # 2) press 'A' to activate that key
        result.append('A')
        pointer = ch

    return result

###############################################################################
# 4) LIFTING A SEQUENCE THROUGH ONE DIRECTIONAL KEYPAD LEVEL
#    Instead of expanding into a huge new sequence, we simply COUNT how many
#    top-level presses it would take to produce the entire sequence `seq_lower`.
#    We'll do a pointer-based DP with memo to avoid O(len(seq)^2) overhead.
#
#    "seq_lower" is a list of symbols from {^,v,<,>,A}.
#    We want the minimal # of button-presses on the controlling keypad
#    to produce that exact sequence of commands.  Each symbol s in seq_lower
#    requires:
#        (dist_dir[current_pointer][s]) moves + 1 press
#    but we must track "current_pointer" on the controlling keypad.
###############################################################################

@lru_cache(None)
def lift_sequence_count_dp(seq_lower_tuple, start_ptr, index):
    """
    DP subroutine for 'lift_sequence_count(seq_lower, start_ptr="A")'.
    seq_lower_tuple: an *immutable* version (tuple) of the lower-level sequence.
    start_ptr: the controlling keypad pointer (one of '^','v','<','>','A').
    index: which symbol in seq_lower_tuple we're about to produce.
    Returns the minimal # of controlling-keypad commands to produce seq_lower_tuple[index:].
    """
    if index == len(seq_lower_tuple):
        return 0

    s = seq_lower_tuple[index]
    # cost to produce symbol s from pointer 'start_ptr' = dist_dir[start_ptr][s] + 1
    # then pointer becomes s
    cost_here = dist_dir[start_ptr][s] + 1
    return cost_here + lift_sequence_count_dp(seq_lower_tuple, s, index+1)

def lift_sequence_count(seq_lower: list) -> int:
    """
    Returns how many button-presses on the controlling directional keypad
    are needed to produce the entire sequence `seq_lower` (list of symbols).
    We use a pointer-based DP (memoized).
    """
    if not seq_lower:
        return 0
    return lift_sequence_count_dp(tuple(seq_lower), 'A', 0)


###############################################################################
# 5) FINAL RECURSIVE LIFT FOR 25 LAYERS
#
#    We'll do it layer by layer:
#      layer 0 (lowest): numeric keypad => produce "code" => a short sequence seq0
#      layer 1: directional keypad => produce seq0 => cost1
#      layer 2: directional keypad => produce a sequence of length cost1 => cost2
#      ...
#      layer 25 => final cost25
#
#    But we do NOT want to build the new sequence at each stage. We'll do a
#    pointer-based summation approach. The simplest way:
#    1) Get seq0 = type_code_on_numeric(...)  (small, maybe ~20 symbols)
#    2) cost1 = lift_sequence_count(seq0)
#    3) cost2 = lift_sequence_of_length(cost1) ...
#
#    However, step (3) "lift_sequence_of_length(cost1)" needs the actual order
#    of those cost1 symbols. The function above requires the actual list, not
#    just its length, because pointer-based cost depends on *which* symbol is next.
#
#    In a purely canonical BFS approach, "move up" or "move left" can be chosen
#    in any order if distance is 2. That can lead to different pointer paths.
#
#    We'll do a simplified approach:
#       - We treat each "move up" in seq0 as the single symbol '^', etc.
#       - Summarily, for the next layer, we do pointer-based DP over that entire list.
#         That yields cost1 and a pointer progression. But if the resulting
#         controlling-layer sequence had length cost1, we do the next layer the same
#         way. We *do* need the exact symbols from the first-lift to feed the second-lift,
#         unless we do the big expansions. That is enormous for 25 layers!
#
#    The trick: for each symbol in seq0, we do "dist_dir[p][symbol] + 1" but that
#    physically means a sub-path of moves. If there's more than 1 BFS path of the
#    same distance, we pick a canonical one (lexicographically).
#
#    That yields an expanded sequence for the next layer. We'll *not* store it in memory.
#    Instead, we feed each symbol on the fly into a second pointer-based DP that counts
#    how many commands *that symbol* costs at the next layer, etc. This can be done with
#    a 2-level DP or a generator approach. Then we keep nesting for 25 layers in a
#    top-down manner. Below is a more direct "recursive-lift" function that does it
#    from top to bottom in one shot, caching intermediate states.
###############################################################################

def compute_nested_cost_25layers(code, itercount):
    """
    Return the total number of actual (top-level) button presses
    required to cause the bottom-level (numeric) keypad to type `code`,
    when there are 25 directional keypads in front of it.

    We'll do:
      seq_numeric = type_code_on_numeric(code)   # e.g. 10-20 symbols in {^,<,>,v,A}
      cost = nest(seq_numeric, 25)  # how many top-level commands?

    where nest(...) is a function that lifts a sequence through N directional layers
    *without* fully expanding each intermediate.  Instead, we do multi-layer pointer-based DP.
    """

    # Step 1: produce the numeric-level sequence (short enough to store directly).
    seq_numeric = type_code_on_numeric(code)

    # Step 2: define a function that, given a sequence of directions (like seq_numeric),
    #         lifts it through 'n' layers of directional keypads.
    #
    # We'll implement `lift_through_n_layers(seq, n)` as a DP that returns
    # how many top-level commands are needed.  If n == 0, there's nothing to lift;
    # the cost is simply len(seq).  Actually if n=0, that would mean "we're at your own
    # real keypad," so each symbol in seq is one real press.  So cost = len(seq).
    #
    # If n>0, each symbol in seq is typed by "dist_dir[pointer][symbol] + 1" commands,
    # but each of those "commands" is itself a symbol at the next level of controlling keypad.
    # So we must recursively call `lift_through_n_layers(...)` on that sub-sequence.
    #
    # That is a big recursion, but we can memoize on (id(seq), n, pointer, index_in_seq).

    @lru_cache(None)
    def lift_through_n_layers(seq_tuple, n, pointer, idx):
        """
        Return how many top-level presses it takes to produce seq_tuple[idx:]
        on n layers of directional keypads, starting with pointer `pointer`
        in the current layer.

        Each symbol is in {^,<,>,v,A}.
        If n == 0, that means "this layer is the actual real keypad," so
        each symbol is exactly 1 press => cost = length of the remainder of seq.
        (Because there's no further 'pointer movement' needed; pressing '^' at
         the top-level is just one real button press, etc.)

        If n > 0, we do pointer-based moves on the current layer:
            cost_for_symbol = dist_dir[pointer][symbol] + 1
         but each of those cost_for_symbol "commands" is itself a symbol in
         {^,<,>,v,A}, which the layer above must produce. So we recursively call
         `lift_through_n_layers(...)` on that sub-sequence. We'll build that
         sub-sequence in a canonical way using path_dir.
        """
        if idx == len(seq_tuple):
            return 0

        if n == 0:
            # No more nesting: each symbol => 1 press
            return len(seq_tuple) - idx

        s = seq_tuple[idx]
        # cost to produce symbol s *at this layer*:
        #   pointer moves: path_dir[pointer][s] (list of moves),
        #   length_of_that_path = dist_dir[pointer][s],
        #   plus 1 for pressing 'A' at the end => total commands_for_symbol
        moves_for_symbol = path_dir[pointer][s]  # e.g. ['^','<']
        # We'll produce that sub-sequence for the next layer:
        #   each item in moves_for_symbol is one symbol in {^,<,>,v}
        # then 1 symbol 'A' for the press.
        sub_seq_for_symbol = moves_for_symbol + ['A']

        # Now we need to recursively "lift" that sub_seq_for_symbol through
        # (n-1) more layers to get how many top-level presses that sub-sequence
        # costs. Then we continue with the rest of seq_tuple (idx+1) in the current layer
        # but pointer is now s.

        # 1) cost to produce sub_seq_for_symbol at the next-larger layer:
        sub_cost = lift_through_n_layers(tuple(sub_seq_for_symbol), n-1, 'A', 0)

        # 2) plus the cost to produce the remainder of seq_tuple (idx+1..end)
        #    from the new pointer = s
        rest_cost = lift_through_n_layers(seq_tuple, n, s, idx+1)

        return sub_cost + rest_cost

    # Finally:
    seq_tuple = tuple(seq_numeric)
    # We have 25 directional layers above it:
    total_cost = lift_through_n_layers(seq_tuple, itercount, 'A', 0)
    return total_cost


###############################################################################
# 6) SOLVE FOR THE 5 CODES, SUM COMPLEXITIES
###############################################################################

def solve_codes_25layers(codes, iter_count):
    """
    codes: list of 5 strings like ['029A','980A','179A','456A','379A'].
    We'll compute, for each code:
       real_life_presses = compute_nested_cost_25layers(code)
       numeric_value = int(code.rstrip('A')) ignoring leading zeros
       complexity = real_life_presses * numeric_value
    and sum them up.
    """
    total_sum = 0
    for code_str in codes:
        # parse numeric portion
        num_part = code_str.rstrip('A')  # e.g. '029'
        if num_part == '':
            # in case the code is just 'A'? Then numeric part is 0
            numeric_val = 0
        else:
            numeric_val = int(num_part)

        # compute real-life presses
        presses = compute_nested_cost_25layers(code_str, iter_count)

        complexity = presses * numeric_val
        total_sum += complexity

        print(f"Code={code_str}, Presses={presses}, NumericVal={numeric_val}, Complexity={complexity}")

    return total_sum


###############################################################################
# 7) EXAMPLE USAGE
###############################################################################

if __name__ == "__main__":
    # Example codes from the puzzle statement:
    puzzle_codes = ["029A", "980A", "179A", "456A", "379A"]


    kp = Keypad()
    dp = Dir_Pad()

    kp_paths = kp.keypad_moves
    dp_paths = dp.keypad_moves

    dist_num, path_num = build_bfs_and_paths(key_to_pos_num)
    dist_dir, path_dir = build_bfs_and_paths(key_to_pos_dir)

    answer = solve_codes_25layers(puzzle_codes,2)
    print("Sum of complexities =", answer)
