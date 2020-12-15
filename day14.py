import itertools
import re
from enum import Enum, auto


class Ops(Enum):
    MASK = auto()
    MEM = auto()


def load_program(file_name):
    with open(f"inputs/{file_name}") as f:
        raw_lines = f.read().strip().split("\n")

    program = []
    for line in raw_lines:
        op = line[:3]
        if op == 'mas':
            # Hmmm, 0s in mask can get AND treatment, 1s in mask can get OR treatment
            mask = line.split(" = ")[1]
            zero_mask = int(mask.replace('X', '1'), 2)
            one_mask = int(mask.replace('X', '0'), 2)
            program.append((Ops.MASK, zero_mask, one_mask))
        elif op == 'mem':
            regex = r"^mem\[(\d+)\]"
            location = int(re.search(regex, line).group(1))
            value = int(line.split(" = ")[1])
            program.append((Ops.MEM, location, value))
        else:
            print(f"UNKNOWN OP: {op}")

    return program


def run_program(program):
    memory = {}
    zero_mask = 0
    one_mask = 0
    for line in program:
        if line[0] == Ops.MASK:
            zero_mask = line[1]
            one_mask = line[2]
        elif line[0] == Ops.MEM:
            # current_memory_value = 0
            location = line[1]
            value = line[2]
            # if location in memory:
            #     current_memory_value = memory[location]
            value &= zero_mask
            value |= one_mask
            memory[location] = value
    return memory


test_program = load_program('day14_test.txt')
test_memory = run_program(test_program)
assert sum(test_memory.values()) == 165

real_program = load_program('day14.txt')
real_memory = run_program(real_program)
memory_hash = sum(real_memory.values())
print(f"Part 1 answer is {memory_hash}")
assert memory_hash == 12408060320841


# Part 2
def load_program_v2(file_name):
    with open(f"inputs/{file_name}") as f:
        raw_lines = f.read().strip().split("\n")

    program = []
    for line in raw_lines:
        op = line[:3]
        if op == 'mas':
            # generate all possible masks given the X values
            mask = line.split(" = ")[1]
            program.append((Ops.MASK, mask))
        elif op == 'mem':
            regex = r"^mem\[(\d+)\]"
            location = int(re.search(regex, line).group(1))
            value = int(line.split(" = ")[1])
            program.append((Ops.MEM, location, value))
        else:
            print(f"UNKNOWN OP: {op}")

    return program


def run_program_v2(program):
    memory = {}
    mask = ""
    for line in program:
        if line[0] == Ops.MASK:
            mask = line[1]
        elif line[0] == Ops.MEM:
            # current_memory_value = 0
            location = line[1]
            value = line[2]
            location |= int(mask.replace('X', '0'), 2)
            location_as_bit_string = "{0:b}".format(location)
            location = location_as_bit_string.zfill(len(mask))
            float_permutations = ["".join(seq) for seq in itertools.product("01", repeat=mask.count('X'))]
            x_positions = [x for x, v in enumerate(mask) if v == 'X']
            for f in float_permutations:
                for i, x in enumerate(x_positions):
                    location = location[:x] + f[i] + location[x+1:]
                memory[int(location, 2)] = value
    return memory


test_program = load_program_v2('day14_testV2.txt')
test_memory = run_program_v2(test_program)
assert sum(test_memory.values()) == 208

real_program = load_program_v2('day14.txt')
real_memory = run_program_v2(real_program)
memory_hash = sum(real_memory.values())
print(f"Part 2 answer is {memory_hash}")
assert memory_hash == 4466434626828
