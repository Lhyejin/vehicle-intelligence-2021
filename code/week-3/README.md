# Week 3 - Kalman Filters, EKF and Sensor Fusion

---

[//]: # (Image References)
[kalman-result]: ./kalman_filter/graph.png
[EKF-results]: ./EKF/plot.png

## Week3 Report
EKF는 nonlinear한 model에서 수행할 수 있도록 kalman filter를 확장시킨 알고리즘이다.
<span style="text-decoration:overline">u</span>_t는 nonlinear function으로 계산하며,
<span style="text-decoration:overline">sigma</span>_t(covariance)는 jacobian을 이용하여 계산한다.
kalman gain 또한 jacobian matrix를 사용하여 계산한다.

그렇게 prediction한 mu와 covariance를 이용하여 t의 mu, covariance를 update한다.

이를 순서대로 구현한 것이 update_ekf 함수이며, 수식을 그대로 적용하여 코드로 변환하였다.
중간에 계산한 pi를 normalize하기 위해 2pi만큼 계속 빼주거나 더해주었다.
그 뒤에 t에서의 mu와 covariance를 업데이트한다.

1. update_ekf 함수

먼저 자코비안을 계산하기 위해 구현되어있는 Jacobian 함수를 사용하였다.
그 뒤에 S를 계산하고, kalman gain을 
```angular2html
# 1. Compute Jacobian Matrix H_j
H_j = Jacobian(self.x)
# 2. Calculate S = H_j * P' * H_j^T + R
S = np.dot(np.dot(H_j, self.P), H_j.T) + self.R
# 3. Calculate Kalman gain K = P' * H_j^T * S^-1
K = np.dot(np.dot(self.P, H_j.T), np.linalg.inv(S))
# 4. Estimate y = z - h(x')
px, py, vx, vy = self.x
h_x_dot = np.array([sqrt(px * px + py * py),
                    atan2(py,px),
                    (px * vx + py * vy) / sqrt(px * px + py * py)
                    ])
y = z - h_x_dot
# 5. Normalize phi so that it is between -PI and +PI
if y[1] > pi:
    while y[1] > pi:
        y[1] -= 2*pi
if y[1] < pi:
    while y[1] < -pi:
        y[1] += 2*pi
# 6. Calculate new estimates
#    x = x' + K * y
self.x = self.x + np.dot(K, y)
#    P = (I - K * H_j) * P
self.P = np.dot((np.identity(K.shape[0]) - np.dot(K, H_j)), self.P)
```

## Kalman Filter Example

In directory [`./kalman_filter`](./kalman_filter), a sample program for a small-scale demonstration of a Kalman filter is provided. Run the following command to test:

```
$ python testKalman.py
```

This program consists of four modules:

* `testKalman.py` is the module you want to run; it initializes a simple Kalman filter and estimates the position and velocity of an object that is assumed to move at a constant speed (but with measurement error).
* `kalman.py` implements a basic Kalman fitler as described in class.
* `plot.py` generates a plot in the format shown below.
* `data.py` provides measurement and ground truth data used in the example.

The result of running this program with test input data is illustrated below:

![Testing of Kalman Filter Example][kalman-result]

Interpretation of the above results is given in the lecture.

In addition, you can run `inputgen.py` to generate your own sample data. It will be interesting to experiment with a number of data sets with different characteristics (mainly in terms of variance, i.e., noise, involved in control and measurement).

---

## Assignment - EFK & Sensor Fusion Example

In directory [`./EKF`](./EKF), template code is provided for a simple implementation of EKF (extended Kalman filter) with sensor fusion. Run the following command to test:

```
$ python run.py
```

The program consists of five modules:

* `run.py` is the modele you want to run. It reads the input data from a text file ([data.txt](./EKF/data.txt)) and feed them to the filter; after execution summarizes the result using a 2D plot.
* `sensor_fusion.py` processees measurements by (1) adjusting the state transition matrix according to the time elapsed since the last measuremenet, and (2) setting up the process noise covariance matrix for prediction; selectively calls updated based on the measurement type (lidar or radar).
* `kalman_filter.py` implements prediction and update algorithm for EKF. All the other parts are already written, while completing `update_ekf()` is left for assignment. See below.
* `tools.py` provides a function `Jacobian()` to calculate the Jacobian matrix needed in our filter's update algorithm.
*  `plot.py` creates a 2D plot comparing the ground truth against our estimation. The following figure illustrates an example:

![Testing of EKF with Sensor Fusion][EKF-results]

### Assignment

Complete the implementation of EKF with sensor fusion by writing the function `update_ekf()` in the module `kalman_filter`. Details are given in class and instructions are included in comments.
