from collections import namedtuple
import copy
import sys
import heapq

Point = namedtuple('Point', ['row', 'col'])
State = namedtuple('State', ['point', 'length', 'dist'])

inf = sys.maxsize

# 0 - left, 1 - up, 2 - right, 3 - down
moves = [Point(col=-1, row=0), Point(col=0, row=-1), Point(col=1, row=0), Point(col=0, row=1)]

def parse_line(line: str):
    line_a = []
    for i in range(0, len(line)):
        line_a.append(line[i])

    return line_a

def pt_to_v(row: int, col: int, w: int) -> int:
    return row * w + col

def d_image(image: []) -> []:
    n_v = len(image) * len(image[0])

    d_image = []

    for row in range(0, n_v):
        d_line = []
        for col in range(0, n_v):
            d_line.append(inf)
        d_image.append(d_line)

    for row in range(0, n_v):
        d_image[row][row] = 0

    w = len(image[0])
    h = len(image)

    moves = [[-1, 0], [0, -1], [1, 0], [0, 1]]

    for row in range(0, len(image)):
        for col in range(0, len(image[0])):
            v = pt_to_v(row, col, w)

            for move in moves:
                n_row = row + move[1]
                n_col = col + move[0]

                if n_row < 0 or n_row >= h:
                    continue
                if n_col < 0 or n_col >= w:
                    continue

                n_v = pt_to_v(n_row, n_col, w)

                d_image[v][n_v] = image[row][col]
                d_image[n_v][v] = image[row][col]


    return d_image

def adjacency_list(image: []) -> []:
    #adj_list = [[] for i in range(0, len(image[0]))]
    adj_list = {}

    w = len(image[0])
    h = len(image)

    moves = [[-1, 0], [0, -1], [1, 0], [0, 1]]

    for row in range(0, len(image)):
        for col in range(0, len(image[0])):
            v = pt_to_v(row, col, w)

            for move in moves:
                n_row = row + move[1]
                n_col = col + move[0]

                if n_row < 0 or n_row >= h:
                    continue
                if n_col < 0 or n_col >= w:
                    continue

                n_v = pt_to_v(n_row, n_col, w)

                n_g = adj_list.setdefault(n_v, {})
                n_g[v] = image[row][col]

                g = adj_list.setdefault(v, {})
                g[n_v] = image[row][col]
    return adj_list

def distance_image(image: []) -> []:
    dist = []
    ext = 1000000

    for row in range(0, len(image)):
        dist_line = []
        for col in range(0, len(image[0])):
            dist_line.append(1)
        dist.append(dist_line)

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
            dist[row][col_adj[i]] = ext

    row_adj = []
    for row in range(0, len(image)):
        g_count = 0
        for col in range(0, len(image[0])):
            if image[row][col] == '#':
                g_count += 1
        if g_count == 0:
            row_adj.append(row)

    for i in range(len(row_adj) - 1, -1, -1):
        for col in range(0, len(image[0])):
            dist[row_adj[i]][col] = ext

    return dist

def floyd_warshall(image: []) -> None:
    n_v = len(image[0])

    for k in range(0, n_v):
        for i in range(0, n_v):
            for j in range(0, n_v):
                if image[i][k] + image[k][j] < image[i][j]:
                    image[i][j] = image[i][k] + image[k][j]

def dijkstra(v: int, adj_list: {}, src: int) -> []:
    dist = [inf for i in range(0, v)]
    dist[src] = 0

    pq = []

    heapq.heappush(pq, (0, src))

    while len(pq) > 0:
        cur_dist, cur = heapq.heappop(pq)

        for n, n_dist in adj_list[cur].items():
            if dist[cur] + n_dist < dist[n]:
                dist[n] = dist[cur] + n_dist

                heapq.heappush(pq, (dist[n], n))
    
    return dist

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

def shortest_dist(pair: [], width: int, height: int, galaxies: {}, dist_image: []):
    visited = set()

    queue = []

    st_g = galaxies[pair[0]]
    f_g = galaxies[pair[1]]

    queue.append(State(point=st_g, length=0, dist=dist_image[st_g.row][st_g.col]))
    visited.add(pt_to_hash(st_g, width))

    while len(queue) > 0:
        state = queue.pop(0)

        pt = state.point
        
        if pt == f_g and state.dist == 0:
            return state.length
        
        if state.dist == 0:
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
                queue.append(State(point=neighbour, length=state.length + 1, dist=dist_image[neighbour.row][neighbour.col]))
                visited.add(pt_to_hash(neighbour, width))
        else:
            queue.append(State(point=pt, length=state.length + 1, dist=state.dist - 1))

def day_11(filename: str) -> int:
    image = []

    with open(filename, 'r', encoding='UTF-8') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            line_arr = parse_line(line)
            image.append(line_arr)

    print("read")

    galaxies = get_galaxies(image)

    pairs = []
    for i in range(1, len(galaxies) + 1):
        for j in range(i + 1, len(galaxies) + 1):
            pairs.append([i, j])
    
    #print('i ' + str(i) + ' j ' + str(j))

    print(len(pairs))

    dist_image = distance_image(image=image)

    #print(dist_image)
    print('distance_image')

    adj_list = adjacency_list(dist_image)
    print(adj_list)

    width = len(image[0])
    height = len(image)

    sum = 0

    galaxy_vetices = set()

    for i in range(1, len(galaxies) + 1):
        pt1 = galaxies[i]
        v1 = pt_to_v(pt1.row, pt1.col, width)
        galaxy_vetices.add(v1)

    for i in range(1, len(galaxies) + 1):
        pt1 = galaxies[i]
        v1 = pt_to_v(pt1.row, pt1.col, width)
        distances = dijkstra(width * height, adj_list, v1)
        for d_index in range(0, len(distances)):
            if d_index in galaxy_vetices:
                sum += distances[d_index]

    # print(ddd)

    # sum = 0
    # for pair in pairs:
    #     dist = shortest_dist(pair, width, height, galaxies, dist_image)
    #     sum += dist
    #     #print(str(pair) + ' ' + str(dist))

    print(int(sum / 2) )

    return sum


    d_image_1 = d_image(dist_image)
    print('d_image')

    #print(d_image_1)

    floyd_warshall(d_image_1)
    print('floyd_warshall')

    #print(d_image_1)

    sum = 0

    for pair in pairs:
        pt1 = galaxies[pair[0]]
        pt2 = galaxies[pair[1]]
        src_v = pt_to_v(pt1.row, pt1.col, len(image[0]))
        dst_v = pt_to_v(pt2.row, pt2.col, len(image[0]))

        dist = d_image_1[src_v][dst_v]

        sum += dist

    print(sum)

    return sum

    # e_image = expand_image(image)

    # print("copied")

    # width = len(e_image[0])
    # height = len(e_image)

    # galaxies = get_galaxies(e_image)

    # pairs = []
    # for i in range(1, len(galaxies) + 1):
    #     for j in range(i + 1, len(galaxies) + 1):
    #         pairs.append([i, j])
    
    # #print('i ' + str(i) + ' j ' + str(j))

    # print(len(pairs))


    # adj = {}
    # sum = 0
    # for pair in pairs:
    #     dist = shortest_dist(pair, width, height, galaxies, adj)
    #     g = adj.setdefault(pair[0], {})
    #     g[pair[1]] = dist
    #     g = adj.setdefault(pair[1], {})
    #     g[pair[0]] = dist
    #     sum += dist
    #     #print(str(pair) + ' ' + str(dist))

    # print(sum)
    # return sum

if __name__ == '__main__':
    v1 = day_11("/Users/nstehov/PycharmProjects/pythonProject/input_11_1.txt")
    if v1 == 374:
        print('test 1 true')

    v2 = day_11("/Users/nstehov/PycharmProjects/pythonProject/input_11_2.txt")
