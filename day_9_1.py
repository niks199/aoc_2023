def parse_history(line: str) -> []:
    items = line.split(' ')

    return[int(item) for item in items]

def extrapolate(history: []) -> int:
    j = len(history)
    while True:
        stopLoop = True
        for i in range(1, j):
            history[i - 1] = history[i] - history[i - 1]
            if history[i - 1] != 0:
                stopLoop = False
        j -= 1
        if stopLoop == True:
            break

    extr = 0
    for i in range(j, len(history)):
        extr += history[i]

    return extr

def extrapolate_prevoius(history: []) -> int:
    j = len(history)

    while True:
        stopLoop = True
        for i in range(len(history) - 1, len(history) - j, -1):
            history[i] = history[i] - history[i - 1]
            if history[i] != 0:
                stopLoop = False
        j -= 1
        if stopLoop == True:
            break

    k = len(history) - j
    extr = history[k]
    for i in range(k - 1, -1, -1):
        extr = history[i] - extr

    return extr


def day_9(filename: str):
    histories = []

    with open(filename, 'r', encoding='UTF-8') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            history = parse_history(line)
            histories.append(history)

    print(histories)

    extrapolates = [extrapolate_prevoius(history) for history in histories]

    #[extrapolates] = extrapolate_prevoius(histories[2])

    print(extrapolates)

    ss = sum(extrapolates)

    print(ss)

if __name__ == '__main__':
    day_9("/Users/nstehov/PycharmProjects/pythonProject/input_9_2.txt")