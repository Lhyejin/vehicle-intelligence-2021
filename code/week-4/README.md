# Week 4 - Motion Model & Particle Filters

---

[//]: # (Image References)
[empty-update]: ./empty-update.gif
[example]: ./example.gif

## Report
particle filter는 sampling한 데이터들을 이용하여 localization을 하는 방법이다.

1. update_weights 함수

    weight를 업데이트하기 위해 먼저 map landmark와 각 particle의 거리를 구하여 근처 landmark를 찾아냈다.
    그리고 observation을 map 관점으로 transformation한 뒤에 associate함수를 이용하여 map landmark와 관측한 landmark를 매칭시켰다.
    measurement의 확률, 각 observation에 대한 probability를 계산하기 위해 bivariate Gaussian distribution pdf을 사용하였다.
    각 particle에 대해 모든 observation의 probability는 곱해주고, p['w']를 업데이트 시킨다.
    
    구현하는데에 있어서 몇가지 에러가 생긴 적이 있다. weight를 제대로 계산하지 않으면, 
    그 다음에 particle sampling을 제대로 수행하지 못하게 되고 이는 그 다음 수행에도 문제가 된다.
    지금까지 확인한 문제는 2가지이다.
    1. resampling을 진행할 때, 모든 weight의 합이 0이 되는 문제가 있어서 normalize를 시키지 못했다.
    2. 전혀 다른 위치의 particle이 생성되면 map landmark의 거리가 멀어져 visible landmark가 존재하지 않는다. 
    
    이러한 문제들을 해결하기 위해, weight가 0이 되는 것을 막아야한다. 


2. resample 함수
    위의 update_weight 함수를 실행시킨 후에, weight를 기반으로 새롭게 particle을 뽑는다. 
    weight를 먼저 normalize를 시킨 후에, np.random.choice를 이용하여 각 particle에 가중치를 두고 샘플링을 진행하였다.
   ```angular2html
        particles = []
        # 1. Drawing particle samples according to their weights.
        normalized_weights = 0
        weights = []
        for p in self.particles:
            normalized_weights += p['w']
        print(normalized_weights)
        for i in range(self.num_particles):
            weights.append(self.particles[i]['w'] / normalized_weights)

        # 2. Make a copy of the particle; otherwise the duplicate particles
        #    will not behave independently from each other - they are
        #    references to mutable objects in Python.
        idxs = np.random.choice(self.num_particles, self.num_particles, p=weights)
        for i in idxs:
            particles.append(self.particles[i])

        # Finally, self.particles shall contain the newly drawn set of
        #   particles.
        self.particles = particles
```


## Assignment

You will complete the implementation of a simple particle filter by writing the following two methods of `class ParticleFilter` defined in `particle_filter.py`:

* `update_weights()`: For each particle in the sample set, calculate the probability of the set of observations based on a multi-variate Gaussian distribution.
* `resample()`: Reconstruct the set of particles that capture the posterior belief distribution by drawing samples according to the weights.

To run the program (which generates a 2D plot), execute the following command:

```
$ python run.py
```

Without any modification to the code, you will see a resulting plot like the one below:

![Particle Filter without Proper Update & Resample][empty-update]

while a reasonable implementation of the above mentioned methods (assignments) will give you something like

![Particle Filter Example][example]

Carefully read comments in the two method bodies and write Python code that does the job.
