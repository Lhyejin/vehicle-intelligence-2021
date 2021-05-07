# Week 7 - Hybrid A* Algorithm & Trajectory Generation

---

[//]: # (Image References)
[has-example]: ./hybrid_a_star/has_example.png
[ptg-example]: ./PTG/ptg_example.png

## Report

7주차는 hybrid a* algorithm을 구현하는 것이다. 
1. expend 함수
   
이 함수는 현재 state에서 가능한 다음 state를 계산하는 역할을 한다. 주어진 omega를 이용하여 가능한 모든 theta에 대해 계산하고, x와 y 좌표를 계산한다.
theta는 0과 2PI 사이의 값으로 normalize 해준다. 계산한 다음 state들은 반환해준다. 
2. search 함수
   
search 함수는 goal에 도달할 때까지의 path를 계산하거나 도달하지 못한다는 것을 계산하는 역할을 한다.
가능한 다음 state를 open list에 넣어 cost function이 작은 순서대로 방문을 한다. 
방문한 위치에서 다음 state를 계산하고 그 state가 유효하면 다시 open list에 넣어 앞의 과정을 반복한다.
이렇게 goal에 닿을 때까지 반복하며, goal에 도달하지 못했는제 open list에 아무 것도 없을 경우에는 goal에 도달하는 방법이 없다는 것으로 간주하고 그대로 중단한다.

3. theta_to_stack_num 함수
   
이 함수는 주어진 theta를 THETA_CELL의 개수로 나누었을 때 어느 부분에 위치하는지 반환하는 함수이다.
radian에서 degree로 변환 후, theta가 어느 간격에 위치하는지 계산하고 반환한다. (ex: 0~num_theta_cell => 0번째 cell)

4. heuristic 함수

이 함수는 현재 위치에서 goal까지의 거리를 cost로 표현하는 함수이다. 
기존 a*에서는 discrete하기 때문에 셀의 개수로 거리를 표현하면 됐지만, 현재는 continuous space를 다루기 때문에 기존 표현을 사용하기 어렵다.
continuous space 안에서 거리를 측정하기 위해 euclidean distance를 사용하여 남은 거리를 계산하였다.

이렇게 구현한 결과, ppt에서 제공된 결과와는 차이가 있지만, path는 찾을 수 있었다.
다른 이유는 아마 heuristic 함수의 차이때문일 것이라고 생각한다.

## Assignment: Hybrid A* Algorithm

In directory [`./hybrid_a_star`](./hybrid_a_star), a simple test program for the hybrid A* algorithm is provided. Run the following command to test:

```
$ python main.py
```

The program consists of three modules:

* `main.py` defines the map, start configuration and end configuration. It instantiates a `HybridAStar` object and calls the search method to generate a motion plan.
* `hybrid_astar.py` implements the algorithm.
* `plot.py` provides an OpenCV-based visualization for the purpose of result monitoring.

You have to implement the following sections of code for the assignment:

* Trajectory generation: in the method `HybridAStar.expand()`, a simple one-point trajectory shall be generated based on a basic bicycle model. This is going to be used in expanding 3-D grid cells in the algorithm's search operation.
* Hybrid A* search algorithm: in the method `HybridAStar.search()`, after expanding the states reachable from the current configuration, the algorithm must process each state (i.e., determine the grid cell, check its validity, close the visited cell, and record the path. You will have to write code in the `for n in next_states:` loop.
* Discretization of heading: in the method `HybridAStar.theta_to_stack_num()`, you will write code to map the vehicle's orientation (theta) to a finite set of stack indices.
* Heuristic function: in the method `HybridAStar.heuristic()`, you define a heuristic function that will be used in determining the priority of grid cells to be expanded. For instance, the distance to the goal is a reasonable estimate of each cell's cost.

You are invited to tweak various parameters including the number of stacks (heading discretization granularity) and the vehicle's velocity. It will also be interesting to adjust the grid granularity of the map. The following figure illustrates an example output of the program with the default map given in `main.py` and `NUM_THETA_CELLS = 360` while the vehicle speed is set to 0.5.

![Example Output of the Hybrid A* Test Program][has-example]

---

## Experiment: Polynomial Trajectory Generation

In directory [`./PTG`](./PTG), a sample program is provided that tests polynomial trajectory generation. If you input the following command:

```
$ python evaluate_ptg.py
```

you will see an output such as the following figure.

![Example Output of the Polynomial Trajectory Generator][ptg-example]

Note that the above figure is an example, while the result you get will be different from run to run because of the program's random nature. The program generates a number of perturbed goal configurations, computes a jerk minimizing trajectory for each goal position, and then selects the one with the minimum cost as defined by the cost functions and their combination.

Your job in this experiment is:

1. to understand the polynomial trajectory generation by reading the code already implemented and in place; given a start configuration and a goal configuration, the algorithm computes coefficient values for a quintic polynomial that defines the jerk minimizing trajectory; and
2. to derive an appropriate set of weights applied to the cost functions; the mechanism to calculate the cost for a trajectory and selecting one with the minimum cost is the same as described in the previous (Week 6) lecture.

Experiment by tweaking the relative weight for each cost function. It will also be very interesting to define your own cost metric and implement it using the information associated with trajectories.
