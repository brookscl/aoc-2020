# Part 1
def load_boot_code(file_name):
    with open(f"inputs/{file_name}") as f:
        raw_lines = f.read().strip().split("\n")
    code_list = []
    for line in raw_lines:
        ops = line.split(' ')
        code_list.append((ops[0], int(ops[1])))
    return code_list


def halt_on_second_pass(run_count, pc):
    return run_count[pc] == 2


def dump_core(code, run_count):
    print("CORE DUMP")
    print("=========")
    for i, op in enumerate(code):
        print(f"{i:04d}: [{run_count[i]}] {op[0]}: {op[1]}")

def run_program(code, halt_func, dump=False):
    pc = 0
    acc = 0
    run_count = [0] * len(code)
    while True:
        op, value = code[pc][0], code[pc][1]
        run_count[pc] += 1
        # Halting rule
        if halt_func(run_count, pc):
            print(f"HALT: PC={pc}, ACC={acc}")
            if dump:
                dump_core(code, run_count)
            return False
        if op == 'nop':
            pc += 1
        elif op == 'acc':
            acc += value
            pc += 1
        elif op == 'jmp':
            pc += value
        else:
            print(f"ILLEGAL OP: {op}: {value} at PC {pc}")
        if pc >= len(code):
            print(f"HALTING at end of program, ACC={acc}")
            return True


program = load_boot_code('day08_test.txt')
run_program(program, halt_on_second_pass)

real_program = load_boot_code('day08_input.txt')
run_program(real_program, halt_on_second_pass)


# Part 2
def try_all_programs(code):
    for i in range(len(code)):
        op, value = code[i][0], code[i][1]
        if op == 'nop':
            trial = code[:]
            trial[i] = ('jmp', value)
        elif op == 'jmp':
            trial = code[:]
            trial[i] = ('nop', value)
        else:
            continue
        if run_program(trial, halt_on_second_pass):
            print("SUCCESS")
            break

print("Part 2 test program:")
try_all_programs(program)

print("Part 2 real program:")
try_all_programs(real_program)
