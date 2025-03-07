import numpy as np
import itertools

# Given map
grid = np.array([
    [1, 1, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1]
])

# List of possible actions defined in terms of changes in
# the coordinates (y, x)
forward = [
    (-1,  0),   # Up
    ( 0, -1),   # Left
    ( 1,  0),   # Down
    ( 0,  1),   # Right
]

# Three actions are defined:
# - right turn & move forward
# - straight forward
# - left turn & move forward
# Note that each action transforms the orientation along the
# forward array defined above.
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

init = (4, 3, 0)    # Representing (y, x, o), where
                    # o denotes the orientation as follows:
                    # 0: up
                    # 1: left
                    # 2: down
                    # 3: right
                    # Note that this order corresponds to forward above.
goal = (2, 0)
cost = (2, 1, 20)   # Cost for each action (right, straight, left)

# EXAMPLE OUTPUT:
# calling optimum_policy_2D with the given parameters should return
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]

def optimum_policy_2D(grid, init, goal, cost):
    # Initialize the value function with (infeasibly) high costs.
    value = np.full((4, ) + grid.shape, 999, dtype=np.int32)
    # Initialize the policy function with negative (unused) values.
    policy = np.full((4,) + grid.shape, -1, dtype=np.int32)
    # Final path policy will be in 2D, instead of 3D.
    policy2D = np.full(grid.shape, ' ')

    # Apply dynamic programming with the flag change.
    change = True
    while change:
        change = False
        # This will provide a useful iterator for the state space.
        p = itertools.product(
            range(grid.shape[0]),
            range(grid.shape[1]),
            range(len(forward))
        )
        # Compute the value function for each state and
        # update policy function accordingly.
        for y, x, t in p:
            # Mark the final state with a special value that we will
            # use in generating the final path policy.
            if (y, x) == goal and value[(t, y, x)] > 0:
                value[(t, y, x)] = 0
                policy[(t, y, x)] = 0 # goal이기 때문에 뭘하든 상관없음
                change = True

            # Try to use simple arithmetic to capture state transitions.
            elif grid[(y, x)] == 0:
                for act in action: # 모든 action에 대해서 수행
                    t2, y2, x2 = (t+act)%4, y + forward[(t+act)%4][0], x + forward[(t+act)%4][1] # 다음 위치 갱신
                    if 0 <= y2 < grid.shape[0] and 0 <= x2 < grid.shape[1] \
                        and grid[(y2, x2)] == 0:
                        v2 = value[(t2, y2, x2)] + cost[act+1]
                        if v2 < value[(t, y, x)]: #현재 value가 v2보다 클 때, v2로 update
                            change = True
                            value[(t, y, x)] = v2
                            policy[(t, y, x)] = act


    # Now navigate through the policy table to generate a
    # sequence of actions to take to follow the optimal path.
    # TODO: implement code
    # init 이용해서 optimal path 출력 (policy2D에)
    curr_y, curr_x, curr_t = init[0], init[1], init[2]
    fail = False
    while True:
        if (curr_y, curr_x) == goal: # goal에 도달할 떄까지 반복한다.
            policy2D[(curr_y, curr_x)] = '*'
            break
        act = policy[(curr_t, curr_y, curr_x)]
        policy2D[(curr_y, curr_x)] = action_name[act+1] # action 이름 할당
        curr_t, curr_y, curr_x = (curr_t+act)%4, curr_y + forward[(curr_t+act)%4][0], curr_x + forward[(curr_t+act)%4][1]
        if grid.shape[0] <= curr_y or curr_y < 0 or 0 > curr_x or curr_x >= grid.shape[1]: # 맵외로 벗어나면 실패
            # 길이 없음, 실패
            fail = True
            break
    # Return the optimum policy generated above.
    return policy2D

print(optimum_policy_2D(grid, init, goal, cost))
