import random
import itertools
from collections import deque

# -----------------------------------------------------
# Parsing, Simulation, and Helper Functions
# -----------------------------------------------------

def parse_input(input_text):
    """
    Parse the input text into an initial assignment dictionary (for wires with given values)
    and a list of gate instructions.
    """
    initial = {}
    gates = []
    for line in input_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if ':' in line and '->' not in line:
            # e.g. "x00: 1"
            name, val = line.split(':')
            initial[name.strip()] = int(val.strip())
        elif '->' in line:
            # e.g. "x00 AND y00 -> z00"
            expr, out_wire = line.split("->")
            out_wire = out_wire.strip()
            tokens = expr.split()
            if len(tokens) != 3:
                raise ValueError("Unexpected format in line: " + line)
            in1, op, in2 = tokens
            gates.append((in1, op, in2, out_wire))
    return initial, gates

def eval_gate(val1, op, val2):
    if op == "AND":
        return val1 & val2
    elif op == "OR":
        return val1 | val2
    elif op == "XOR":
        return val1 ^ val2
    else:
        raise ValueError("Unknown operator: " + op)

def simulate(initial, gates, swap_map=None):
    """
    Simulate the circuit. If swap_map is provided then whenever a gate’s output wire
    is a key in swap_map, its computed value is written to swap_map[out] instead.
    """
    wires = dict(initial)
    remaining = list(gates)
    while remaining:
        progress = False
        next_remaining = []
        for in1, op, in2, out in remaining:
            effective_out = swap_map.get(out, out) if swap_map else out
            if in1 in wires and in2 in wires:
                wires[effective_out] = eval_gate(wires[in1], op, wires[in2])
                progress = True
            else:
                next_remaining.append((in1, op, in2, out))
        if not progress:
            break
        remaining = next_remaining
    return wires

def get_z_output(wires):
    """
    Combine wires whose names start with "z" into a binary number.
    z00 is the least significant bit.
    """
    z_names = sorted([name for name in wires if name.startswith("z")],
                     key=lambda s: int(s[1:]))
    result = 0
    for i, name in enumerate(z_names):
        result += (wires[name] << i)
    return result

def test_swap_configuration(initial, gates, swap_map, test_cases):
    """
    For each (x,y) pair in test_cases, set the initial x and y wires accordingly,
    simulate the circuit (using swap_map) and check that the computed z–output equals x+y.
    """
    xs = sorted([name for name in initial if name.startswith("x")],
                key=lambda s: int(s[1:]))
    ys = sorted([name for name in initial if name.startswith("y")],
                key=lambda s: int(s[1:]))
    num_bits = len(xs)
    for x_val, y_val in test_cases:
        test_initial = dict(initial)
        for i, name in enumerate(xs):
            test_initial[name] = (x_val >> i) & 1
        for i, name in enumerate(ys):
            test_initial[name] = (y_val >> i) & 1
        wires = simulate(test_initial, gates, swap_map)
        z_val = get_z_output(wires)
        if z_val != (x_val + y_val):
            return False
    return True

def generate_test_cases(num_bits, count=50):
    """Generate random (x,y) pairs with numbers in the range [0, 2^(num_bits)-1]."""
    max_val = (1 << num_bits) - 1
    return [(random.randint(0, max_val), random.randint(0, max_val))
            for _ in range(count)]

# -----------------------------------------------------
# Block–by–Block Sub–circuit Isolation and DFS Search
# -----------------------------------------------------

def get_subcircuit_candidates_for_block(gates, block_start, block_end):
    """
    Return the list of gates that lie on any dependency path from an input up to a z–wire
    whose index is in [block_start, block_end).
    """
    z_indices = set(range(block_start, block_end))
    produced_by = {g[3]: g for g in gates}
    candidate = set()
    queue = deque()
    for g in gates:
        if g[3].startswith("z"):
            idx = int(g[3][1:])
            if idx in z_indices:
                candidate.add(g)
                queue.append(g)
    while queue:
        g = queue.popleft()
        for inp in (g[0], g[2]):
            if inp in produced_by:
                pred = produced_by[inp]
                if pred not in candidate:
                    candidate.add(pred)
                    queue.append(pred)
    return list(candidate)

def candidate_pair_error(g1, g2, initial, gates):
    """
    For a candidate pair (swapping outputs of g1 and g2), return an error score
    on the default initial input.
    """
    swap_map = {g1[3]: g2[3], g2[3]: g1[3]}
    wires = simulate(initial, gates, swap_map)
    sim_z = get_z_output(wires)
    xs = sorted([name for name in initial if name.startswith("x")],
                key=lambda s: int(s[1:]))
    ys = sorted([name for name in initial if name.startswith("y")],
                key=lambda s: int(s[1:]))
    x_val = sum(initial[x] << i for i, x in enumerate(xs))
    y_val = sum(initial[y] << i for i, y in enumerate(ys))
    correct = x_val + y_val
    return abs(sim_z - correct)

def generate_candidate_pairs_from_candidates(candidates, initial, gates):
    """
    From a list of candidate gates, generate all candidate pairs and sort them by error.
    """
    cand_pairs = []
    n = len(candidates)
    for i in range(n):
        for j in range(i+1, n):
            g1 = candidates[i]
            g2 = candidates[j]
            err = candidate_pair_error(g1, g2, initial, gates)
            cand_pairs.append(((g1, g2), err))
    cand_pairs.sort(key=lambda pair: pair[1])
    return [pair[0] for pair in cand_pairs]

def dfs_candidate_pairs_sub(cand_pairs, initial, gates, test_cases, chosen, used, start):
    """
    Recursively search among candidate pairs (from a sub–circuit) for a set of swapped pairs
    that makes the circuit work for test_cases.
    (We use a quick prune on the first test case in test_cases.)
    Returns a list of candidate pairs (each a tuple (g1, g2)) if successful, else None.
    """
    # If we have chosen at least one candidate pair, test the partial swap mapping.
    if chosen:
        swap_map = {}
        for g1, g2 in chosen:
            swap_map[g1[3]] = g2[3]
            swap_map[g2[3]] = g1[3]
        if not test_swap_configuration(initial, gates, swap_map, [test_cases[0]]):
            return None
    # We allow any number (>=1) of swapped pairs to fix a block.
    # Here we return the current set if it already passes full test_cases.
    swap_map = {}
    for g1, g2 in chosen:
        swap_map[g1[3]] = g2[3]
        swap_map[g2[3]] = g1[3]
    if chosen and test_swap_configuration(initial, gates, swap_map, test_cases):
        return list(chosen)
    # Otherwise, try adding another candidate pair.
    for i in range(start, len(cand_pairs)):
        g1, g2 = cand_pairs[i]
        if g1 in used or g2 in used:
            continue
        chosen.append((g1, g2))
        used.add(g1)
        used.add(g2)
        result = dfs_candidate_pairs_sub(cand_pairs, initial, gates, test_cases, chosen, used, i+1)
        if result is not None:
            return result
        chosen.pop()
        used.remove(g1)
        used.remove(g2)
    return None

# -----------------------------------------------------
# Main Execution: Part 1 and Block–by–Block Part 2
# -----------------------------------------------------

if __name__ == '__main__':
    # (Input is the same as provided earlier.)
    input_text = """x00: 1
x01: 0
x02: 0
x03: 1
x04: 1
x05: 1
x06: 0
x07: 0
x08: 1
x09: 1
x10: 0
x11: 1
x12: 0
x13: 1
x14: 0
x15: 1
x16: 0
x17: 0
x18: 1
x19: 1
x20: 0
x21: 0
x22: 0
x23: 1
x24: 1
x25: 1
x26: 0
x27: 0
x28: 1
x29: 0
x30: 0
x31: 0
x32: 1
x33: 0
x34: 1
x35: 0
x36: 1
x37: 0
x38: 1
x39: 1
x40: 1
x41: 0
x42: 0
x43: 0
x44: 1
y00: 1
y01: 1
y02: 1
y03: 1
y04: 0
y05: 0
y06: 0
y07: 0
y08: 0
y09: 1
y10: 0
y11: 1
y12: 0
y13: 1
y14: 0
y15: 1
y16: 1
y17: 1
y18: 1
y19: 1
y20: 0
y21: 0
y22: 1
y23: 1
y24: 1
y25: 1
y26: 0
y27: 1
y28: 0
y29: 0
y30: 0
y31: 0
y32: 1
y33: 0
y34: 1
y35: 1
y36: 0
y37: 0
y38: 0
y39: 1
y40: 1
y41: 0
y42: 0
y43: 0
y44: 1

qgv OR dsf -> mjm
shj AND wsr -> ftr
jcf OR wgg -> chb
jbp AND grd -> tcw
rbm OR sck -> dtj
qjb OR qqm -> vdr
ktf OR pvt -> tjg
x32 XOR y32 -> wnj
nbc AND wjv -> tjm
y42 XOR x42 -> ksk
y31 XOR x31 -> mqk
y32 AND x32 -> jfp
grd XOR jbp -> z36
y39 XOR x39 -> bmb
vbj XOR chb -> z04
tqv XOR www -> z40
x34 AND y34 -> sck
y07 AND x07 -> dsf
y12 XOR x12 -> qvh
fnt AND bnk -> pvt
x10 XOR y10 -> fnt
wgw AND nph -> hjt
x30 XOR y30 -> bgs
bdm XOR hvn -> z37
mtg XOR vnm -> z06
gdn OR pck -> wsr
ttr OR nfj -> fbv
jtn AND vtk -> wqs
x08 XOR y08 -> qjb
dmm OR mmr -> nhk
qqd AND cph -> bqd
tqv AND www -> nnr
ggg XOR kbg -> z03
hff AND gdg -> twb
nqm OR whj -> ghb
x14 AND y14 -> nfj
crv XOR cvf -> z25
ftc OR jjn -> z45
bnk XOR fnt -> z10
y30 AND x30 -> mmr
qtv AND dnj -> gbg
x23 AND y23 -> vgr
ndd OR ncb -> fhg
x33 AND y33 -> qgm
rrh OR dqs -> gdp
y40 XOR x40 -> www
x41 XOR y41 -> wvq
jtn XOR vtk -> z20
tpd OR djn -> qvc
y18 AND x18 -> jdr
pnd OR hwf -> vtk
y26 AND x26 -> vqh
vcs XOR dtj -> jbp
x03 AND y03 -> wgg
rjv OR fgf -> brq
vjn AND tjg -> trg
cph XOR qqd -> z05
jbr AND ncd -> mvb
qvh AND wmd -> fbn
x25 XOR y25 -> cvf
x39 AND y39 -> rvc
y44 AND x44 -> ftc
y36 XOR x36 -> grd
y03 XOR x03 -> kbg
vvj XOR bqv -> z27
vbj AND chb -> kqr
twb OR dtd -> stw
mnv XOR hcg -> z13
y26 XOR x26 -> dnj
rkd OR rmp -> wrw
y22 XOR x22 -> tdc
wvq AND tkt -> jsc
mjm XOR gvw -> z08
hvn AND bdm -> pck
cbf XOR vdr -> z09
hdb OR hmb -> qtv
dvs OR mvd -> hwm
mqk AND nhk -> ncb
rfj OR jgc -> bst
wrw XOR hwh -> z28
gdp XOR stm -> z07
stm AND gdp -> qgv
hff XOR gdg -> z29
y44 XOR x44 -> vbd
tqq OR jjc -> tpn
qgm OR mvb -> cqg
dkg XOR ghb -> z02
wrw AND hwh -> pkq
hwm AND tdc -> z22
x02 AND y02 -> gws
jfp OR mpd -> ncd
y11 AND x11 -> smr
hvd AND bmb -> vts
kqr OR jsj -> qqd
y24 XOR x24 -> wgw
stw XOR bgs -> z30
tpn AND wcn -> tpd
y19 AND x19 -> pnd
y38 AND x38 -> dkn
pkq OR vbc -> hff
y31 AND x31 -> ndd
wwc AND nvv -> whj
y14 XOR x14 -> drk
bst AND pkj -> jjc
sht OR fhh -> bnk
x05 XOR y05 -> cph
vts OR rvc -> tqv
x04 AND y04 -> jsj
wjv XOR nbc -> z23
y17 XOR x17 -> wcn
x04 XOR y04 -> vbj
y01 AND x01 -> nqm
x01 XOR y01 -> wwc
vdr AND cbf -> sht
jhm AND wst -> dvs
tpv XOR drk -> z14
cjm XOR rws -> z19
bqd OR hns -> mtg
x20 XOR y20 -> jtn
x08 AND y08 -> gvw
cbc XOR cqg -> z34
rgt AND fbv -> rfj
wmd XOR qvh -> z12
x23 XOR y23 -> wjv
y35 AND x35 -> ppf
x43 AND y43 -> trf
fhg XOR wnj -> z32
x12 AND y12 -> cmn
y00 AND x00 -> nvv
tcw OR jms -> hvn
nhk XOR mqk -> z31
x07 XOR y07 -> stm
vgr OR tjm -> nph
drk AND tpv -> ttr
x09 AND y09 -> fhh
x22 AND y22 -> snh
wgw XOR nph -> z24
mtg AND vnm -> rrh
qvc AND mms -> tps
x06 XOR y06 -> vnm
tps OR jdr -> cjm
fbv XOR rgt -> jgc
y41 AND x41 -> wfd
x19 XOR y19 -> rws
hcg AND mnv -> cfk
wsr XOR shj -> z38
brq AND jpt -> wtr
cjm AND rws -> hwf
y25 AND x25 -> hmb
y02 XOR x02 -> dkg
y40 AND x40 -> qsg
bqv AND vvj -> rmp
hvd XOR bmb -> z39
y35 XOR x35 -> vcs
x42 AND y42 -> rjv
x37 AND y37 -> gdn
tjg XOR vjn -> z11
qtv XOR dnj -> z26
jhm XOR wst -> z21
nwp OR gws -> ggg
y00 XOR x00 -> z00
mrq OR wqs -> wst
x13 AND y13 -> rsq
ftr OR dkn -> hvd
jbr XOR ncd -> z33
x05 AND y05 -> hns
rsq OR cfk -> tpv
mms XOR qvc -> z18
x27 AND y27 -> rkd
crv AND cvf -> hdb
cqg AND cbc -> rbm
pkj XOR bst -> z16
x28 AND y28 -> vbc
jsc OR wfd -> ngw
mjm AND gvw -> qqm
wnj AND fhg -> mpd
y15 XOR x15 -> rgt
x20 AND y20 -> mrq
tkt XOR wvq -> z41
y13 XOR x13 -> mnv
y24 AND x24 -> nqr
wtr OR trf -> jvs
ggg AND kbg -> jcf
x36 AND y36 -> jms
x29 AND y29 -> dtd
ksk AND ngw -> fgf
x11 XOR y11 -> vjn
tpn XOR wcn -> z17
y43 XOR x43 -> jpt
vbd AND jvs -> jjn
nnr OR qsg -> tkt
x27 XOR y27 -> bqv
x28 XOR y28 -> hwh
x09 XOR y09 -> cbf
vcs AND dtj -> qrg
x34 XOR y34 -> cbc
ghb AND dkg -> nwp
y37 XOR x37 -> bdm
x38 XOR y38 -> shj
hjt OR nqr -> crv
vbd XOR jvs -> z44
fbn OR cmn -> hcg
x06 AND y06 -> dqs
y15 AND x15 -> z15
x33 XOR y33 -> jbr
y21 XOR x21 -> jhm
snh OR drg -> nbc
y18 XOR x18 -> mms
vqh OR gbg -> vvj
y21 AND x21 -> mvd
qrg OR ppf -> z35
y10 AND x10 -> ktf
x16 AND y16 -> tqq
tdc XOR hwm -> drg
wwc XOR nvv -> z01
x17 AND y17 -> djn
jpt XOR brq -> z43
smr OR trg -> wmd
x16 XOR y16 -> pkj
x29 XOR y29 -> gdg
bgs AND stw -> dmm
ngw XOR ksk -> z42"""

    # ------------------------------
    # Part 1: Simulate the Circuit and Compute z–Output
    # ------------------------------
    initial, gates = parse_input(input_text)
    wires = simulate(initial, gates)
    part1 = get_z_output(wires)
    print("Part one:", part1)
    
    # ------------------------------
    # Part 2: Block–by–Block Search for Swapped–Gate Pairs
    # ------------------------------
    # Global swap map will hold the corrections (keys: original output wires; values: swapped–in wire)
    global_swap = {}
    global_swapped_pairs = []  # List of (g1, g2) pairs we decide to swap.
    total_swaps_needed = 4  # There are exactly four swapped–gate pairs.
    
    # We'll divide the z–wires into blocks (here using blocks of 8 bits, with the last block adjusted).
    blocks = [(0,8), (8,16), (16,24), (24,32), (32,45)]
    
    # For each block, we generate test cases that vary only in that block.
    for block in blocks:
        block_start, block_end = block
        shift = block_start
        width = block_end - block_start
        def block_test_case():
            # Generate a number that varies only in this block (other bits forced to 0)
            k = random.randint(0, (1 << width) - 1)
            return k << shift
        # Generate a small set of test cases for this block.
        test_cases_block = [(block_test_case(), block_test_case()) for _ in range(10)]
        
        # Isolate candidate gates that influence z–wires in this block.
        candidates = get_subcircuit_candidates_for_block(gates, block_start, block_end)
        print(f"Block {block_start}-{block_end}: {len(candidates)} candidate gates")
        
        # From these candidates, generate candidate pairs (sorted by error on the default input).
        cand_pairs = generate_candidate_pairs_from_candidates(candidates, initial, gates)
        print(f"Block {block_start}-{block_end}: {len(cand_pairs)} candidate pairs")
        
        # Search (via DFS) for one or more swapped–gate pairs in this block that fix the circuit on test_cases_block.
        res = dfs_candidate_pairs_sub(cand_pairs, initial, gates, test_cases_block, chosen=[], used=set(), start=0)
        if res is not None:
            print(f"Block {block_start}-{block_end}: Found {len(res)} swap pair(s)")
            for (g1, g2) in res:
                # Add these pairs into our global solution.
                global_swap[g1[3]] = g2[3]
                global_swap[g2[3]] = g1[3]
                global_swapped_pairs.append((g1, g2))
                if len(global_swapped_pairs) >= total_swaps_needed:
                    break
        if len(global_swapped_pairs) >= total_swaps_needed:
            break

    if len(global_swapped_pairs) != total_swaps_needed:
        print("Did not find enough swapped pairs in block search.")
    else:
        # Now test the global swap mapping on full-range test cases.
        num_bits = len([name for name in initial if name.startswith("x")])
        full_test_cases = generate_test_cases(num_bits, count=50)
        if test_swap_configuration(initial, gates, global_swap, full_test_cases):
            swapped_wires = sorted(global_swap.keys())
            answer = ",".join(swapped_wires)
            print("Part two:", answer)
        else:
            print("Global swap mapping failed full test.")
