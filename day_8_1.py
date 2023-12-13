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

def how_many_steps(moves: [], node_map: {}, src: str, dst: str) -> int:
    current_node = node_map[src]
    move_index = 0
    steps_count = 0

    while True:
        move = moves[move_index]
        steps_count += 1

        next_node_id = current_node[move]
        current_node = node_map[next_node_id]

        if current_node['id'] == dst and move_index == len(moves) - 1:
            break
        
        move_index += 1

        if move_index == len(moves):
            move_index = 0
        
    return steps_count

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

    step_num = how_many_steps(moves, node_map, 'AAA', 'ZZZ')

    print(step_num)

if __name__ == '__main__':
    day_8("/Users/nstehov/PycharmProjects/pythonProject/input_8_3.txt")