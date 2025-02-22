import re
from itertools import combinations, permutations

def solve():
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

    initial_values_str, gate_definitions_str = input_text.strip().split("\n\n")

    initial_values = {}
    for line in initial_values_str.split("\n"):
        wire, value = line.split(": ")
        initial_values[wire] = int(value)

    gate_definitions = []
    for line in gate_definitions_str.split("\n"):
        match = re.match(r"([a-z0-9]+) (AND|OR|XOR) ([a-z0-9]+) -> ([a-z0-9]+)", line)
        if match:
            input1, op, input2, output = match.groups()
            gate_definitions.append({'input1': input1, 'op': op, 'input2': input2, 'output': output})
            continue
        match = re.match(r"([a-z0-9]+) OR ([a-z0-9]+) -> ([a-z0-9]+)", line) #OR cases without AND/XOR before
        if match:
            input1, op, input2, output = match.groups()
            gate_definitions.append({'input1': input1, 'op': op, 'input2': input2, 'output': output})
            continue
        match = re.match(r"NOT ([a-z0-9]+) -> ([a-z0-9]+)", line) # NOT case (not used in this problem, but for completeness)
        if match:
            op_input, output = match.groups()
            gate_definitions.append({'input1': op_input, 'op': 'NOT', 'output': output}) # Assuming NOT has one input, for general case.

    def simulate_circuit(current_initial_values, current_gate_definitions):
        wires = current_initial_values.copy()
        updated = True
        while updated:
            updated = False
            for gate in current_gate_definitions:
                input1_name = gate['input1']
                input2_name = gate.get('input2') #input2 might not exist for NOT gate.
                op = gate['op']
                output_name = gate['output']

                input1_val = wires.get(input1_name)
                input2_val = wires.get(input2_name) if input2_name else None

                if input1_val is not None and (input2_val is not None if input2_name else True) : #Both inputs are ready (or single input for NOT)
                    output_val = None
                    if op == 'AND':
                        output_val = input1_val & input2_val
                    elif op == 'OR':
                        output_val = input1_val | input2_val
                    elif op == 'XOR':
                        output_val = input1_val ^ input2_val
                    elif op == 'NOT': #NOT gate case (not used in this problem)
                        output_val = 1 - input1_val #Assuming NOT means bitwise NOT for 0/1

                    if output_val is not None and wires.get(output_name) != output_val:
                        wires[output_name] = output_val
                        updated = True
        return wires

    # Part 1
    final_wires = simulate_circuit(initial_values, gate_definitions)
    z_wires_values = []
    for wire, value in final_wires.items():
        if wire.startswith('z'):
            z_wires_values.append((wire, value))
    z_wires_values.sort(key=lambda item: int(item[0][1:])) # Sort by z index
    binary_output = "".join([str(v) for _, v in z_wires_values])
    decimal_output_part1 = int(binary_output[::-1], 2) #Reverse for little-endian

    print(f"Part 1 Decimal Output: {decimal_output_part1}")

    # Part 2 - Find swapped wires
    original_gate_definitions = gate_definitions[:]
    all_gate_indices = list(range(len(original_gate_definitions)))
    best_swap_config = None
    test_inputs = [(0,0), (1,1), (5,3), (10,7), (20,15), (30,25), (100, 50)] #Test input pairs

    for gate_indices_to_swap_pairs_indices in combinations(all_gate_indices, 8):
        gate_indices_to_swap = list(gate_indices_to_swap_pairs_indices)

        swap_pairs_combinations = set()
        for p in permutations(gate_indices_to_swap):
            pairs_tuple = tuple(sorted([(p[0], p[1]), (p[2], p[3]), (p[4], p[5]), (p[6], p[7])]))
            swap_pairs_combinations.add(pairs_tuple)


        for swap_pairs in swap_pairs_combinations:
            current_gate_definitions = [gate.copy() for gate in original_gate_definitions] # create a copy

            swapped_wires_names = []
            for gate_index1, gate_index2 in swap_pairs:
                wire1 = current_gate_definitions[gate_index1]['output']
                wire2 = current_gate_definitions[gate_index2]['output']
                current_gate_definitions[gate_index1]['output'] = wire2
                current_gate_definitions[gate_index2]['output'] = wire1
                swapped_wires_names.extend(sorted([wire1, wire2]))

            is_adder = True
            for x_val, y_val in test_inputs:
                test_initial_values = initial_values.copy()
                x_binary = format(x_val, 'b').zfill(45) #Use 45 bits based on input size
                y_binary = format(y_val, 'b').zfill(45)

                for i in range(45):
                    x_wire_name = f'x{str(i).zfill(2)}'
                    y_wire_name = f'y{str(i).zfill(2)}'
                    if x_wire_name in test_initial_values:
                         test_initial_values[x_wire_name] = int(x_binary[44-i]) #Reverse for little-endian
                    if y_wire_name in test_initial_values:
                         test_initial_values[y_wire_name] = int(y_binary[44-i]) #Reverse for little-endian

                final_wires_test = simulate_circuit(test_initial_values, current_gate_definitions)
                z_wires_values_test = []
                for wire, value in final_wires_test.items():
                    if wire.startswith('z'):
                        z_wires_values_test.append((wire, value))
                z_wires_values_test.sort(key=lambda item: int(item[0][1:]))
                binary_output_test = "".join([str(v) for _, v in z_wires_values_test])
                if not binary_output_test:
                    decimal_output_test = 0
                else:
                    decimal_output_test = int(binary_output_test[::-1], 2)

                if decimal_output_test != x_val + y_val:
                    is_adder = False
                    break
            if is_adder:
                best_swap_config = swapped_wires_names
                break # Found correct config
        if best_swap_config:
            break


    if best_swap_config:
        print("Part 2 Swapped wires:", ",".join(sorted(best_swap_config)))
    else:
        print("Part 2: No correct swap configuration found within search space.")


solve()