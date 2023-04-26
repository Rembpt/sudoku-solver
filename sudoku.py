from random import randint
import math
import copy

def read_sudoku_file(filename, delimiter=','):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file]
    sudoku = []
    for line in lines:
        row = [int(num) for num in line.split(delimiter)]
        sudoku.append(row)
    return sudoku

m = read_sudoku_file("sudoku.txt", delimiter=',')

grid_size = 9
tile_size = math.sqrt(grid_size)
tile_size = int(tile_size)

m_copy = copy.deepcopy(m)

def init_map_values(m, v):
    for a in range(grid_size):
        for b in range(grid_size):
            if m[a][b] != 0:
                reduce_entropy(v, a, b, m[a][b])
    return v

def set_map_values(m):
    v = [["123456789" for j in range(grid_size)] for i in range(grid_size)]
    v = init_map_values(m, v)
    return(v)

def print_map(m):
    i = 0
    while i < grid_size:
        print(m[i])
        i += 1

def reduce_entropy(v, y, x, i):
    for a in range(grid_size):
        if str(i) in str(v[y][a]):
            v[y][a] = str(v[y][a]).replace(str(i), "")

        if str(i) in str(v[a][x]):
            v[a][x] = str(v[a][x]).replace(str(i), "")

    xm = 0
    ym = 0
    while x - tile_size >= 0:
        x -= tile_size
        xm += tile_size
    while y - tile_size >= 0:
        y -= tile_size
        ym += tile_size

    for a in range(tile_size):
        for b in range(tile_size):
            if str(i) in str(v[a + ym][b + xm]):
                v[a + ym][b + xm] = str(v[a + ym][b + xm]).replace(str(i), "")



    return(v)

def find_lowest_entropy(m, v):
    low_antropy = []
    count = 0
    a = 1
    for a in range(grid_size + 1):
        positions = []
        for y in range(grid_size):
            for x in range(grid_size):
                if m[y][x] == 0 and len(str(v[y][x])) == a and a != 0:
                    positions.append((y, x))
                    count += 1
        if positions:
            low_antropy.append(positions)
        if count > 0:
            return low_antropy
    return low_antropy

v = set_map_values(m)

while True:

    rd_nb = 0

    arr_of_low_entropy = find_lowest_entropy(m, v)

    if len(arr_of_low_entropy) == 0:
        m = copy.deepcopy(m_copy)
        v = set_map_values(m)
        continue

    arr_len = len(arr_of_low_entropy[0])

    rd_pos = randint(0, arr_len - 1)

    rd_y = arr_of_low_entropy[0][rd_pos][0]
    rd_x = arr_of_low_entropy[0][rd_pos][1]

    while str(rd_nb) not in str(v[rd_y][rd_x]):
        rd_nb = randint(1, 9)

    m[rd_y][rd_x] = rd_nb

    v = reduce_entropy(v, rd_y, rd_x, rd_nb)

#    print()

#    print_map(v)

#    print_map(m)

    zero_count = 0
    for a in range(grid_size):
        for b in range(grid_size):
            if m[a][b] == 0:
                zero_count += 1
    if zero_count == 0:
        print_map(m)
        exit(0)
