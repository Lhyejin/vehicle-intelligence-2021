# Week 2 - Markov Localization

---

[//]: # (Image References)
[plot]: ./markov.gif

## Week2 Report

bayes filter를 계산하기 위해서는 prior distribution과 measurement의 distribution을 구해야한다.
각각을 계산하기 위해 motion_model 함수와 observation_model 함수를 수행한다.
각 함수는 밑과 같이 구현하였다.

### 1. motion_model() Function
motion_model 함수는 belief distribution에서 belief prediction(<span style="text-decoration:overline">bel</span>(x))를 계산한다.
u_t만으로 현재 자동차의 위치가 있을 확률(x_t의 prior distribution)을 계산하는 함수는 P_tras * P_prior(이전의 belief)이다.
transition probability는 normal distribution으로 가정하였다.
모든 이전 위치의 prior distribution을 계산하고 더해줘야하므로 for문을 돌면서 이전에 있었던 위치에 대해 
norm_pdf(position-i, mov, stdev**2) * prior[i]를 계산하고 모두 더해준다.
그 결과값은 현재 position에 대한 prior distribution이 되며, return을 해준다. 
```angular2html
def motion_model(position, mov, priors, map_size, stdev):
    position_prob = 0.0
    for i in range(map_size): # 이전의 모든 위치에 대해서 
        position_prob += norm_pdf(position-i, mov, stdev**2) * priors[i] # belief predition을 수행
    return position_prob
```
### 2. observation_model() Function
observation_model 함수는 observation이 주어졌을 때, measurement의 확률을 계산한다. 
measurement의 확률은 normal distribution을 따른다고 가정했다.  
만약에 observation이 존재하지 않거나, 실제 관측되어야 하는 landmark보다 observation이 더 많을 경우에는 계산이 불가하므로 0을 반환해준다.
관측된 landmark의 개수가 실제 landmark보다 작거나 같을 때는 계산이 가능하므로 계속 진행한다.
observation에서 관측된 각 landmark의 거리와 실제거리로 normal distribution을 계산한다. 그리고 모든 observation에 대해 계산하기 위해
각각 계산된 값을 distance_prob에 곱해준다.
```angular2html
def observation_model(landmarks, observations, pseudo_ranges, stdev):
    distance_prob = 1.0
    if len(observations) == 0: # observation이 없을 때는 수행 못함
        return 0.0
    elif len(observations) > len(pseudo_ranges): # 실제보다 더 많이 관측했을 때도 수행 못함
        return 0.0
    else:
        for i in range(len(observations)): # 관측된 모든 landmark에 대해서
            distance_prob *= norm_pdf(observations[i], pseudo_ranges[i], stdev**2) # measurement의 확률을 계산
    return distance_prob
```

main 함수에서 motion_model 함수와 observation_model 함수에서 각각 prior와 measurement의 확률을 구한 후에 
그 두 결과값을 곱하면 postrier(현재 x의 belief)가 나오게 된다. 

## Assignment

You will complete the implementation of a simple Markov localizer by writing the following two functions in `markov_localizer.py`:

* `motion_model()`: For each possible prior positions, calculate the probability that the vehicle will move to the position specified by `position` given as input.

* `observation_model()`: Given the `observations`, calculate the probability of this measurement being observed using `pseudo_ranges`.


![Expected Result of Markov Localization][plot]

