import copy


def tilepuzzle(start, goal):
    return reverse(state_search([start], goal, []))


def state_search(unexplored, goal, path):
    if unexplored == []:
        return []
    elif goal == head(unexplored):
        return cons(goal, path)
    elif head(unexplored) in path:
        return state_search(tail(unexplored), goal,
                            path)
    elif len(path) > 30:
        return []
    else:
        result = state_search(generate_new_state(head(unexplored)),
                              goal,
                              cons(head(unexplored), path))
        if result != []:
            return result
        else:
            return state_search(tail(unexplored),
                                goal,
                                path)


def generate_new_state(current_state):
    return (generate_slide_top(current_state) + generate_slide_left(current_state) +
            generate_slide_down(current_state) + generate_slide_right(current_state))


def generate_slide_left(current_state):
    temp_state = copy_current_state(current_state)
    result = []
    # find 0
    empty_pos = find_empty_pos(temp_state)

    # check if the element is at the rear
    if empty_pos[1] != 0:
        temp_state[empty_pos[0]][empty_pos[1]], temp_state[empty_pos[0]][empty_pos[1] -
                                                                         1] = temp_state[empty_pos[0]][empty_pos[1] - 1], temp_state[empty_pos[0]][empty_pos[1]]

        result.append(temp_state)
    return result


def generate_slide_right(current_state):
    temp_state = copy_current_state(current_state)
    result = []
    empty_pos = find_empty_pos(temp_state)

    if empty_pos[1] != len(temp_state[0]) - 1:
        temp_state[empty_pos[0]][empty_pos[1]], temp_state[empty_pos[0]][empty_pos[1] +
                                                                         1] = temp_state[empty_pos[0]][empty_pos[1] + 1], current_state[empty_pos[0]][empty_pos[1]]
        result.append(temp_state)
    return result


def generate_slide_top(current_state):
    temp_state = copy_current_state(current_state)
    result = []
    empty_pos = find_empty_pos(temp_state)

    if empty_pos[0] != 0:
        temp_state[empty_pos[0]][empty_pos[1]], temp_state[empty_pos[0]-1][empty_pos[1]
                                                                           ] = temp_state[empty_pos[0]-1][empty_pos[1]], current_state[empty_pos[0]][empty_pos[1]]
        result.append(temp_state)
    return result


def generate_slide_down(current_state):
    temp_state = copy_current_state(current_state)
    result = []
    empty_pos = find_empty_pos(temp_state)

    if empty_pos[0] != len(temp_state)-1:
        temp_state[empty_pos[0]][empty_pos[1]], temp_state[empty_pos[0]+1][empty_pos[1]
                                                                           ] = temp_state[empty_pos[0]+1][empty_pos[1]], temp_state[empty_pos[0]][empty_pos[1]]
        result.append(temp_state)
    return result


# find the position of blank space
def find_empty_pos(current_state):
    empty_pos = None
    for row_index in range(len(current_state)):
        try:
            empty_pos = (row_index, current_state[row_index].index(0))
        except ValueError:
            continue
    return empty_pos


# make a copy of current state
def copy_current_state(current_state):
    return copy.deepcopy(current_state)


def head(lst):
    return lst[0]


def cons(item, lst):
    return [item] + lst


def tail(lst):
    return lst[1:]


def reverse(st):
    return st[::-1]


print(tilepuzzle([[2, 8, 3], [1, 0, 4], [7, 6, 5]],
                 [[1, 0, 3], [7, 2, 4], [6, 8, 5]]))

'''
Sample output 1:
tilepuzzle([[[2, 8, 3], [1, 0, 4], [7, 6, 5]], [[2, 8, 3], [1, 4, 5], [7, 0, 6]])
[[[2, 8, 3], [1, 0, 4], [7, 6, 5]], [[2, 0, 3], [1, 8, 4], [7, 6, 5]], [[0, 2, 3], [1, 8, 4], [7, 6, 5]],
[[1, 2, 3], [0, 8, 4], [7, 6, 5]], [[1, 2, 3], [7, 8, 4],
    [0, 6, 5]], [[1, 2, 3], [7, 8, 4], [6, 0, 5]],
[[1, 2, 3], [7, 0, 4], [6, 8, 5]], [[1, 0, 3], [7, 2, 4],
    [6, 8, 5]], [[1, 3, 0], [7, 2, 4], [6, 8, 5]],
[[1, 3, 4], [7, 2, 0], [6, 8, 5]], [[1, 3, 4], [7, 0, 2],
    [6, 8, 5]], [[1, 0, 4], [7, 3, 2], [6, 8, 5]],
[[1, 4, 0], [7, 3, 2], [6, 8, 5]], [[1, 4, 2], [7, 3, 0],
    [6, 8, 5]], [[1, 4, 2], [7, 0, 3], [6, 8, 5]],
[[1, 4, 2], [7, 8, 3], [6, 0, 5]], [[1, 4, 2], [7, 8, 3],
    [0, 6, 5]], [[1, 4, 2], [0, 8, 3], [7, 6, 5]],
[[0, 4, 2], [1, 8, 3], [7, 6, 5]], [[4, 0, 2], [1, 8, 3],
    [7, 6, 5]], [[4, 2, 0], [1, 8, 3], [7, 6, 5]],
[[4, 2, 3], [1, 8, 0], [7, 6, 5]], [[4, 2, 3], [1, 8, 5],
    [7, 6, 0]], [[4, 2, 3], [1, 8, 5], [7, 0, 6]],
[[4, 2, 3], [1, 8, 5], [0, 7, 6]], [[4, 2, 3], [0, 8, 5],
    [1, 7, 6]], [[0, 2, 3], [4, 8, 5], [1, 7, 6]],
[[2, 0, 3], [4, 8, 5], [1, 7, 6]], [[2, 8, 3], [4, 0, 5],
    [1, 7, 6]], [[2, 8, 3], [0, 4, 5], [1, 7, 6]],
[[2, 8, 3], [1, 4, 5], [0, 7, 6]], [[2, 8, 3], [1, 4, 5], [7, 0, 6]]]
'''

'''
Sample output 2:
print(tilepuzzle([[2, 8, 3], [1, 0, 4], [7, 6, 5]],[[1, 0, 3], [7, 2, 4], [6, 8, 5]]))
[[[2, 8, 3], [1, 0, 4], [7, 6, 5]], [[2, 0, 3], [1, 8, 4], [7, 6, 5]], 
[[0, 2, 3], [1, 8, 4], [7, 6, 5]], [[1, 2, 3], [0, 8, 4], [7, 6, 5]], 
[[1, 2, 3], [7, 8, 4], [0, 6, 5]], [[1, 2, 3], [7, 8, 4], [6, 0, 5]], 
[[1, 2, 3], [7, 0, 4], [6, 8, 5]], [[1, 0, 3], [7, 2, 4], [6, 8, 5]]]
'''
