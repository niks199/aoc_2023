from collections import namedtuple
import copy

Point = namedtuple('Point', ['row', 'col'])
State = namedtuple('State', ['point', 'length'])

# 0 - left, 1 - up, 2 - right, 3 - down
moves = [Point(col=-1, row=0), Point(col=0, row=-1), Point(col=1, row=0), Point(col=0, row=1)]

def parse_line(line: str):
    line_a = []
    for i in range(0, len(line)):
        line_a.append(line[i])

    return line_a

def expand_image(image_s: []) -> []:
    image = copy.deepcopy(image_s)

    col_adj = []

    for col in range(0, len(image[0])):
        g_count = 0
        for row in range(0, len(image)):
            if image[row][col] == '#':
                g_count += 1
        if g_count == 0:
            col_adj.append(col)

    for row in range(0, len(image)):
        for i in range(len(col_adj) - 1, -1, -1):
            image[row].insert(col_adj[i], '.')

    row_adj = []
    for row in range(0, len(image)):
        g_count = 0
        for col in range(0, len(image[0])):
            if image[row][col] == '#':
                g_count += 1
        if g_count == 0:
            row_adj.append(row)

    for i in range(len(row_adj) - 1, -1, -1):
        row_c = ['.' for i in range(0, len(image[0]))]
        image.insert(row_adj[i], row_c)
                     
    return image

def get_galaxies(image: []) -> {}:
    galaxies = {}

    num = 1
    for row in range(0, len(image)):
        for col in range(0, len(image[0])):
            if image[row][col] == '#':
                galaxies[num] = Point(row=row, col=col)
                num += 1

    return galaxies


def pt_to_hash(pt: Point, width: int) -> int:
    return pt.row * width + pt.col

def hash_to_pt(h: int, width: int) -> Point:
    return Point(row = int(h / width), col = int(h % width))

def find_dest(adj: {}, src: int, dst: int, length: int) -> int:
    if src == dst:
        return length
    
    if src in adj:
        neighbours = adj[src]
        for key, sub_len in neighbours:
            find_dest(adj, key, dst, length + sub_len)
    else:
        return -1

def shortest_dist(pair: [], width: int, height: int, galaxies: {}, adj: {}):
    visited = set()

    queue = []

    st_g = galaxies[pair[0]]
    f_g = galaxies[pair[1]]

    queue.append(State(point=st_g, length=0))
    visited.add(pt_to_hash(st_g, width))

    while len(queue) > 0:
        state = queue.pop(0)

        pt = state.point
        
        if pt == f_g:
            return state.length
        
        neighbours = []

        for move in moves:
            new_pt = Point(row=pt.row + move.row, col=pt.col + move.col)

            if new_pt.row < 0 or new_pt.row >= height:
                continue
            if new_pt.col < 0 or new_pt.col >= width:
                continue

            neighbours.append(new_pt)

        for neighbour in neighbours:
            if pt_to_hash(neighbour, width) in visited:
                continue
            queue.append(State(point=neighbour, length=state.length+1))
            visited.add(pt_to_hash(neighbour, width))


def day_11(filename: str) -> int:
    image = []

    with open(filename, 'r', encoding='UTF-8') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            line_arr = parse_line(line)
            image.append(line_arr)

    print("read")

    e_image = expand_image(image)

    print("copied")

    width = len(e_image[0])
    height = len(e_image)

    galaxies = get_galaxies(e_image)

    pairs = []
    for i in range(1, len(galaxies) + 1):
        for j in range(i + 1, len(galaxies) + 1):
            pairs.append([i, j])
    
    #print('i ' + str(i) + ' j ' + str(j))

    print(len(pairs))

    adj = {}
    sum = 0
    for pair in pairs:
        dist = shortest_dist(pair, width, height, galaxies, adj)
        g = adj.setdefault(pair[0], {})
        g[pair[1]] = dist
        g = adj.setdefault(pair[1], {})
        g[pair[0]] = dist
        sum += dist
        print(str(pair) + ' ' + str(dist))

    print(sum)
    return sum

if __name__ == '__main__':
    v1 = day_11("/Users/nstehov/PycharmProjects/pythonProject/input_11_1.txt")
    if v1 == 374:
        print('test 1 true')

    v2 = day_11("/Users/nstehov/PycharmProjects/pythonProject/input_11_2.txt")
