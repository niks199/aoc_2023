from collections import namedtuple
import sys

State = namedtuple('State', ['pt', 'length'])
Point = namedtuple('Point', ['row', 'col'])

# 0 - left, 1 - up, 2 - right, 3 - down
moves = [Point(col=-1, row=0), Point(col=0, row=-1), Point(col=1, row=0), Point(col=0, row=1)]

def parse_line(line: str) -> []:
    ch = []
    for i in range(0, len(line)):
        ch.append(line[i])

    return ch

def find_start(sketch: []) -> Point:
    for row in range(0, len(sketch)):
        for col in range(0, len(sketch[row])):
            if sketch[row][col] == 'S':
                return Point(row=row, col=col)
            
    return None

def pt_to_hash(pt: Point, width: int) -> int:
    return pt.row * width + pt.col

def hash_to_pt(h: int, width: int) -> Point:
    return Point(row = int(h / width), col = int(h % width))

def longest_half_bfs(sketch: [], start_pt: []):
    queue = []

    queue.append(State(pt=start_pt, length=0))

    visited = set()

    width = len(sketch[0])
    height = len(sketch)

    visited.add(pt_to_hash(start_pt, width))

    moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    while len(queue) > 0:
        state = queue.pop(0)
        
        if pt_to_hash(state.pt, width) in visited:
            continue

        tile = sketch[state.pt.row][state.pt.col]

        if tile == 'S':
            for i in range(0, len(moves)):
                move = moves[i]

                new_pt = Point(row = state.pt.row + move[1], col=state.pt.col + move[0])

                if new_pt.col < 0 or new_pt.col >= width:
                    continue
                if new_pt.row < 0 or new_pt.row >= height:
                    continue
                
                new_tile = sketch[new_pt.row][new_pt.col]

                if i == 0 and new_tile in ['-', 'L', 'F']:
                    queue.append(State(length=state.length + 1, pt=new_pt))
                    visited.add(pt_to_hash(new_pt, width))
                elif i ==1 and new_tile in ['F', '|', '7']:
                    queue.append(State(length=state.length + 1, pt=new_pt))
                    visited.add(pt_to_hash(new_pt, width))
                elif i == 2 and new_tile in ['-', 'J', '7']:
                    queue.append(State(length=state.length + 1, pt=new_pt))
                    visited.add(pt_to_hash(new_pt, width))
                elif i == 3 and new_tile in ['|', 'L', 'J']:
                    queue.append(State(length=state.length + 1, pt=new_pt))
                    visited.add(pt_to_hash(new_pt, width))
        elif tile == '.':
            pass
        else:
            move_i = []
            if tile == '|':
                move_i = [1, 3]
            elif tile == '-':
                move_i = [0, 2]
            elif tile == 'L':
                move_i = [0, 2]
            elif tile == 'J':
                pass
            elif tile == '7':
                pass
            elif tile == 'F':
                pass

    pass

def get_allowed_move_indexes(tile: str) -> []:
    if tile == '.':
        return []
    elif tile == '|':
        return [1, 3]
    elif tile == '-':
        return [0, 2]
    elif tile == 'L':
        return [1, 2]
    elif tile == 'J':
        return [1, 0]
    elif tile == '7':
        return [3, 0]
    elif tile == 'F':
        return [3, 2]
    elif tile == 'S':
        return [0, 1, 2, 3]

def get_allowed_dot_move_indexes(tile: str) -> []:
    if tile == '.':
       return [0, 1, 2, 3]
    return []

def new_tile_match_current_move(new_tile: str, move_index: int) -> bool:
    if move_index == 0 and new_tile in ['-', 'L', 'F']:
        return True
    elif move_index == 1 and new_tile in ['F', '|', '7']:
        return True
    elif move_index == 2 and new_tile in ['-', 'J', '7']:
        return True
    elif move_index == 3 and new_tile in ['|', 'L', 'J']:
        return True
    if new_tile == 'S':
        return True
    
    return False

def get_neightbours(sketch: [], pt: []) -> []:
    tile = get_tile(sketch=sketch, pt=pt)

    move_indexes = get_allowed_move_indexes(tile)

    neightbours = []

    for move_index in move_indexes:
        move = moves[move_index]

        new_pt = Point(row = pt.row + move.row, col=pt.col + move.col)

        if new_pt.col < 0 or new_pt.col >= len(sketch[0]):
            continue
        if new_pt.row < 0 or new_pt.row >= len(sketch):
            continue

        new_tile = get_tile(sketch=sketch, pt=new_pt)

        if not new_tile_match_current_move(new_tile, move_index):
            continue

        neightbours.append(new_pt)

    return neightbours

def get_start_neightbours(sketch: [], pt: []) -> []:
    tile = get_tile(sketch=sketch, pt=pt)

    move_indexes = get_allowed_move_indexes(tile)

    neightbours = []

    for move_index in move_indexes:
        move = moves[move_index]

        new_pt = Point(row = pt.row + move.row, col=pt.col + move.col)

        if new_pt.col < 0 or new_pt.col >= len(sketch[0]):
            continue
        if new_pt.row < 0 or new_pt.row >= len(sketch):
            continue
        new_tile = sketch[new_pt.row][new_pt.col]

        if not new_tile_match_current_move(new_tile, move_index):
            continue
        if new_tile == 'S':
            continue

        neightbours.append(new_pt)

    return neightbours

def get_tile(sketch: [], pt: []):
    return sketch[pt.row][pt.col]

def get_orderding(sketch: [], pt: [], visited: set, stack: [], depth: int) -> None:
    if get_tile(sketch=sketch, pt=pt) == 'S':
        return
    
    #print("depth " + str(depth))
    
    visited.add(pt_to_hash(pt, len(sketch[0])))

    neightbours = get_neightbours(sketch=sketch, pt=pt)

    for neightbour in neightbours:
        if not pt_to_hash(neightbour, len(sketch[0])) in visited:
            get_orderding(sketch=sketch, pt=neightbour, visited=visited, stack=stack, depth=depth + 1)
    
    stack.append(pt_to_hash(pt, len(sketch[0])))


def longest_half_dfs(sketch: [], pt: [], visited: set):
    stack = []
    get_orderding(sketch=sketch, pt=pt, visited=visited, stack=stack, depth=0)

    answer = int((len(stack) + 1) / 2)

    return answer, stack



def is_inside(pt: Point, sketch: [], path_set: set) -> bool:
    if pt_to_hash(pt=pt, width=len(sketch[0])) in path_set:
        return False
    return True

def is_on_way(pt: Point, sketch: [], path_set: set) -> bool:
    if pt_to_hash(pt=pt, width=len(sketch[0])) in path_set:
        tile = get_tile(sketch, pt)
        if tile == 'L' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == 'J':
            return True
        elif tile == 'J' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == 'L':
            return True
        elif tile == '|' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == '|':
            return True
        elif tile == '|' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == '|':
            return True
        elif tile == 'F' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == '7':
            return True
        elif tile == '7' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == 'F':
            return True
        elif tile == 'L' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == '7':
            return True
        # 7L
        elif tile == '7' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == 'L':
            return True
        # |F
        elif tile == 'F' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == '|':
            return True
        # |F
        elif tile == 'I' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == 'F':
            return True
        # |L
        elif tile == 'L' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == '|':
            return True
        # |L
        elif tile == 'I' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == 'L':
            return True
        # J
        #  F
        elif tile == 'F' and pt.col - 1 >= 0 \
                and pt.row - 1 >= 0 \
                and get_tile(sketch=sketch, pt=Point(row=pt.row - 1, col=pt.col - 1)) == 'J':
            return True
        # J
        #  F
        elif tile == 'J' and pt.col + 1 < len(sketch[0]) \
                and pt.row + 1 < len(sketch) \
                and get_tile(sketch=sketch, pt=Point(row=pt.row - 1, col=pt.col - 1)) == 'F':
            return True
        
    return False

def new_tile_match_current_move_fill(new_tile: str, move_index: int) -> bool:
    if move_index == 0 and new_tile in ['-', 'L', 'F']:
        return True
    elif move_index == 1 and new_tile in ['F', '|', '7']:
        return True
    elif move_index == 2 and new_tile in ['-', 'J', '7']:
        return True
    elif move_index == 3 and new_tile in ['|', 'L', 'J']:
        return True
    if new_tile == 'S':
        return False
    if new_tile == '.':
        return True
    
    return False

def get_neightbours_fill(sketch: [], pt: []) -> []:
    tile = get_tile(sketch=sketch, pt=pt)

    move_indexes = []
    # move up or down
    # JL
    if tile == 'L' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == 'J':
        move_indexes = [1, 3]
    # JL
    elif tile == 'J' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == 'L':
        move_indexes = [1, 3]
    # ||
    elif tile == '|' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == '|':
        move_indexes = [1, 3]
    # ||
    elif tile == '|' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == '|':
        move_indexes = [1, 3]
    # 7F
    elif tile == 'F' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == '7':
        move_indexes = [1, 3]
    # 7F
    elif tile == '7' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == 'F':
        move_indexes = [1, 3]
    # 7L
    elif tile == 'L' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == '7':
        move_indexes = [1, 3]
    # 7L
    elif tile == '7' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == 'L':
        move_indexes = [1, 3]
    # |F
    elif tile == 'F' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == '|':
        move_indexes = [1, 3]
    # |F
    elif tile == 'I' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == 'F':
        move_indexes = [1, 3]
    # |L
    elif tile == 'L' and pt.col - 1 >= 0 and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col - 1)) == '|':
        move_indexes = [1, 3]
    # |L
    elif tile == 'I' and pt.col + 1 < len(sketch[0]) and get_tile(sketch=sketch, pt=Point(row=pt.row, col=pt.col + 1)) == 'L':
        move_indexes = [1, 3]
    # J
    #  F
    elif tile == 'F' and pt.col - 1 >= 0 \
            and pt.row - 1 >= 0 \
            and get_tile(sketch=sketch, pt=Point(row=pt.row - 1, col=pt.col - 1)) == 'J':
        move_indexes = [1]
    # J
    #  F
    elif tile == 'J' and pt.col + 1 < len(sketch[0]) \
            and pt.row + 1 < len(sketch) \
            and get_tile(sketch=sketch, pt=Point(row=pt.row - 1, col=pt.col - 1)) == 'F':
        move_indexes = [3]

    neightbours = []

    for move_index in move_indexes:
        move = moves[move_index]

        new_pt = Point(row = pt.row + move.row, col=pt.col + move.col)

        if new_pt.col < 0 or new_pt.col >= len(sketch[0]):
            continue
        if new_pt.row < 0 or new_pt.row >= len(sketch):
            continue

        new_tile = get_tile(sketch=sketch, pt=new_pt)

        if not new_tile_match_current_move_fill(new_tile, move_index):
            continue

        neightbours.append(new_pt)

    return neightbours

def enclosed_count(sketch: [], path: []) -> int:
    # while len(stack) > 0:
    #     pt_hash = stack.pop()
    #     ppp = hash_to_pt(pt_hash, len(sketch[0]))
    #     print(ppp)
    # print("path len " + str(len(stack)) + " answer " + str(answer))

    path_set = set(path)

    visited = set()

    queue = []

    st_pt = Point(row=0, col=0)

    queue.append(st_pt)
    visited.add(pt_to_hash(st_pt, len(sketch[0])))

    outside_count = 0

    count = 0
    while len(queue) > 0:
        pt = queue.pop(0)

        pt_outside = is_inside(pt=pt, path_set=path_set, sketch=sketch)

#        tt = get_tile(sketch, pt)
#        print(str(pt) + ' ' + tt)
        count += 1

        pt_on_way = is_on_way(pt=pt, path_set=path_set, sketch=sketch)

        if pt_on_way:
            pass

        #pt_on_way = False
        if not pt_outside and not pt_on_way:
            continue

        if pt_outside:
            outside_count += 1
            print("outside " + str(pt))

        # neighbours = get_neightbours_fill(sketch, pt)

        neighbours = []

        if pt_on_way == True:
            neighbours = get_neightbours_fill(sketch, pt)
        else:
            for move in moves:
                new_pt = Point(row=pt.row + move.row, col=pt.col + move.col)
                if new_pt.row < 0 or new_pt.row >= len(sketch):
                    continue
                if new_pt.col < 0 or new_pt.col >= len(sketch[0]):
                    continue
                neighbours.append(new_pt)

        for neighbour in neighbours:
            if pt_to_hash(neighbour, len(sketch[0])) in visited:
                continue
            queue.append(neighbour)
            visited.add(pt_to_hash(neighbour, len(sketch[0])))

    print('count ' + str(count))
    print('prod ' + str(len(sketch) * len(sketch[0])))
    return outside_count

def extend_sketch(sketch: []) -> []:
    new_w = len(sketch[0]) + 2

    new_sketch = []

    top_line = []
    for i in range(0, new_w):
        top_line.append('.')

    new_sketch.append(top_line)

    for r in range(0, len(sketch)):
        mid_line = []
        mid_line.append('.')
        for c in range(0, len(sketch[0])):
            mid_line.append(sketch[r][c])
        mid_line.append('.')

        new_sketch.append(mid_line)

    bottom_line = []
    for i in range(0, new_w):
        bottom_line.append('.')

    new_sketch.append(bottom_line)

    return new_sketch

def shift_path(path: [], old_sketch: [], new_sketch: []) -> []:
    shifted_path = []
    for item_hash in path:
        pt = hash_to_pt(item_hash, len(old_sketch[0]))
        new_pt = Point(row = pt.row + 1, col = pt.col + 1)
        hh = pt_to_hash(new_pt, len(new_sketch[0]))
        shifted_path.append(hh)
    return shifted_path

def day_10(filename: str):
    sketch = []

    with open(filename, 'r', encoding='UTF-8') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            ll = parse_line(line)
            sketch.append(ll)

    # print(sketch)

    start_pt = find_start(sketch=sketch)

    print(start_pt)

    start_neightbours = get_start_neightbours(sketch, start_pt)
    
    pp = 0
    # visited = set()
    # visited.add(pt_to_hash(start_pt, len(sketch[0])))
    # pp = max(pp, longest_half_dfs(sketch, Point(row=2, col=1), visited))

 
    longest_path = []

    for neighbour in start_neightbours:
       visited = set()
       visited.add(pt_to_hash(start_pt, len(sketch[0])))
       c_size, path = longest_half_dfs(sketch, neighbour, visited)
       if c_size > pp:
           longest_path = path
       pp = max(pp, c_size)

    print(pp)

    longest_path.append(pt_to_hash(start_pt, len(sketch[0])))

    e_sketch = extend_sketch(sketch)
    e_path = shift_path(longest_path, sketch, e_sketch)
    ec = enclosed_count(e_sketch, e_path)

    ec -= 2 * (len(e_sketch[0]) - 1) + 2 * (len(e_sketch) - 1)

    total = len(sketch) * len(sketch[0])
    area = total - ec - len(longest_path)

    print("outside " + str(ec))
    print("enclosed " + str(area))

# 6806
if __name__ == '__main__':
    sys.setrecursionlimit(14500)

    day_10("/Users/nstehov/PycharmProjects/pythonProject/input_10_5.txt")