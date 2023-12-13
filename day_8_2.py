import math

def parse_moves(line: str)-> []:
    moves = []
    for i in range(len(line)):
        moves.append(line[i])
    return moves

def parse_node(line:str):
    items = line.split('=')

    id = items[0].strip()

    s_ids = items[1].strip()

    s_ids = s_ids[1:-1]

    s_ids = s_ids.split(',')

    left = s_ids[0].strip()

    right = s_ids[1].strip()

    return {'id': id, 'L': left, 'R': right}

def get_current_nodes(node_ids: [], node_map: {}) -> []:
    return [node_map[node_id] for node_id in node_ids]


def all_nodes_done(current_nodes: [], dst: str) -> bool:
    count = 0

    for current_node in current_nodes:
        if current_node['id'][2] == dst[2]:
            count += 1

        #if not current_node['id'][2] == dst[2]:
        #    return False

    if count == 4:
        print(count)
    return count == len(current_nodes)

def get_next_nodes(current_nodes: [], node_map: {}, move: str):
    next_nodes = []

    for current_node in current_nodes:
        next_node_id = current_node[move]
        next_current_node = node_map[next_node_id]
        next_nodes.append(next_current_node)
    return next_nodes

def how_many_steps(moves: [], node_map: {}, starting_ids: [], dst: str) -> int:
    current_nodes = get_current_nodes(starting_ids, node_map)

    move_index = 0
    steps_count = 0

    while True:
        if all_nodes_done(current_nodes, dst):
            break
        
        move = moves[move_index]
        steps_count += 1

        current_nodes = get_next_nodes(current_nodes, node_map, move)

        move_index += 1

        if move_index == len(moves):
            move_index = 0
        
    return steps_count

def how_many_steps_single(moves: [], node_map: {}, src: str, dst: str, max_match_count: int) -> int:
    current_node = node_map[src]
    move_index = 0
    steps_count = 0

    match_count = 0

    while True:
        if move_index == len(moves):
            move_index = 0

        if current_node['id'][2] == dst[2]:
            match_count += 1
            if match_count == max_match_count:
                break
            else:
                print("steps_count " + str(steps_count) + " match_count " + str(match_count))
        
        move = moves[move_index]
        steps_count += 1

        next_node_id = current_node[move]
        current_node = node_map[next_node_id]

        move_index += 1
        
    return steps_count, move_index

def day_8(filename: str):
    moves = []
    node_map = {}

    with open(filename, 'r', encoding='UTF-8') as f:
        lines = [line.rstrip('\n') for line in f]
        
        moves = parse_moves(lines[0].strip())

        for line in lines[1:]:
            s_line = line.strip()
            if len(s_line) == 0:
                continue
            node = parse_node(s_line)
            node_map[node['id']] = node

    print(moves)
    print(node_map)

    starting_ids = []

    for key, value in node_map.items():
        if key[2] == 'A':
            print(key)
            starting_ids.append(key)


    # step_counts = []
    # for starting_id in starting_ids:
    #     step_count, move_index = how_many_steps_single_cycle(moves, node_map, starting_id, '##Z')
    #     print(starting_id + " step_count " + str(step_count) + " move_index " + str(move_index) 
    #             + " move len " + str(len(moves)))
    #     step_counts.append(step_count)


    step_counts = []
    sums = []
    for starting_id in starting_ids:
        step_count, move_index = how_many_steps_single(moves, node_map, starting_id, '##Z', 1)
        print(starting_id + " step_count " + str(step_count) + " move_index " + str(move_index) 
                + " move len " + str(len(moves)))
        step_counts.append(step_count)
        sums.append(step_count)

    gcd = math.gcd(*step_counts)
    lcm = math.lcm(*step_counts)

    print(lcm)

    print(gcd)

if __name__ == '__main__':
    day_8("/Users/nstehov/PycharmProjects/pythonProject/input_8_3.txt")