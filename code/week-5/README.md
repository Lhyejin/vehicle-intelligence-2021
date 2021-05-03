# Week 5 - Path Planning & the A* Algorithm

---
## Report

5주차 과제의 목표는 방향 t를 고려한 optimal policy 찾을 수 있도록 구현하는 것이다.
기존의 dynamic programming 방식에서 t를 고려하게 되면 action은 4방향이 아닌 (right, forward, left)로
바뀌게 된다. 구현은 이 변한 action과 t를 고려하여, 기존 policy.py와 비슷한 방향으로 진행한다.

먼저, optimum_policy_2D 함수를 실행하게 되면, value와 policy를 4방향에 대해서 초기화한다.
그 뒤에, while문을 반복하면서 value function이 안정화될 때까지, 즉 change하지 않을 때까지 진행한다.
처음에는 모든 value가 초기화 갚으로 되어있고, 각 방향 t에 대해서 goal 위치의 value 값만 0으로 설정되고, 그 뒤에 차례로 goal 주위부터 value가
갱신되기 시작한다. 
현재 위치 y,x,t에서 모든 action을 진행했을 때의 value를 구하여 현재 위치의 value를 갱신하거나 유지한다.
다음 위치는 t에서 각 action을 진행하여 구한다. 맵의 절대적인 방향을 [(-1,  0),( 0, -1),( 1,  0),( 0,  1)]이라고 정의한다면, 
t에 따라 left, right의 방향은 밑과 같이 변하게 된다.

t=0, left=1, forward=0, right=3
t=1, left=2, forward=1, right=0
t=2, left=3, forward=2, right=1
t=3, left=4, forward=3, right=2

t를 기준으로 left, right는 주어진 action 변수 + t가 된다. (t+action)
기존 policy.py와 다르게 다음 위치로 이동하게 되면 t 또한 변하게 되므로 같이 업데이트 시켜야 한다.
나머지 구현방식은 모두 policy.py에 따른다.

policy를 모두 갱신시킨 후에 start와 goal이 주어지면 optimal path를 찾을 수 있다.
시작 위치에서부터 policy대로 계속 행동하면 goal이 나온다. 만약 policy대로 이동했는데도 goal이 나오지 않을 경우에는
맵 위치를 벗어나게 되므로, 맵 이외의 위치가 나온다면 실패라고 구현한다.


## Examples

We have four small working examples for demonstration of basic path planning algorithms:

* `search.py`: simple shortest path search algorithm based on BFS (breadth first search) - only calculating the cost.
* `path.py`: built on top of the above, generating an optimum (in terms of action steps) path plan.
* `astar.py`: basic implementation of the A* algorithm that employs a heuristic function in expanding the search.
* `policy.py`: computation of the shortest path based on a dynamic programming technique.

These sample source can be run as they are. Explanation and test results are given in the lecture notes.

## Assignment

You will complete the implementation of a simple path planning algorithm based on the dynamic programming technique demonstrated in `policy.py`. A template code is given by `assignment.py`.

The assignmemt extends `policy.py` in two aspects:

* State space: since we now consider not only the position of the vehicle but also its orientation, the state is now represented in 3D instead of 2D.
* Cost function: we define different cost for different actions. They are:
	- Turn right and move forward
	- Move forward
	- Turn left and move forward

This example is intended to illustrate the algorithm's capability of generating an alternative (detouring) path when left turns are penalized by a higher cost than the other two possible actions. When run with the settings defined in `assignment.py` without modification, a successful implementation shall generate the following output,

```
[[' ', ' ', ' ', 'R', '#', 'R'],
 [' ', ' ', ' ', '#', ' ', '#'],
 ['*', '#', '#', '#', '#', 'R'],
 [' ', ' ', ' ', '#', ' ', ' '],
 [' ', ' ', ' ', '#', ' ', ' ']]
```

because of the prohibitively high cost associated with a left turn.

You are highly encouraged to experiment with different (more complex) maps and different cost settings for each type of action.
