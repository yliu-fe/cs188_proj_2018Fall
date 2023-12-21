# HW4: Ghost Busters

## Introduction

Design a pacman agent that use sensors to locate and eat invisible ghosts, from locating single stationary ghosts to multiple moving ghosts.

All files to be edited:

- `bustersAgents.py`, for question 4,
- `inference.py`, for questions 0-3, 5-10.

and files to be read:

<!-- TODO: list those files should be read during homework. -->

## Question 0

No credit here, but it's useful to complete the `DiscreteDistribution` class, a modified dictionary, to model belief distributions and weight distributions. This class is defined in `inference.py`.

> Task here:
>
> - Fill method `normalize`;
> - Fill method `sample`.
>

**Firstly**, we fill the `normalize` method. If no item here (`len(self.keys()) == 0`), or the total value is 0 (`self.total() == 0`), the function should be passed to avoid error.If neither of these cases is triggered, this method will normalize all values in this dictionary.

**Secondly**, `sample` method should be filled. This method will return a **key** (instead of the value!) with the probability proportional to keys' corresponding value. `random.random()` is recommended, which generates a float between 0 and 1 without any arguments. We can implement the method with steps below:

- Normalize the dictionary, if `self.total() != 1`;
- generate a random float with `random.random()`
- list key-item pairs with sorted keys: `list(sorted(self.items()))`
- for pairs in the list above, if value is higher than random signal, return the key here; otherwise, reduce the random signal by value.

```python
    def sample(self):
        "*** YOUR CODE HERE ***"

        if self.total() != 1:
            self.normalize()
        randomSignal = random.random()
        listedItems = list(sorted(self.items()))
        for pair in listedItems:
            if pair[1] >= randomSignal:
                return pair[0]
            else:
                randomSignal -= pair[1]
```

## Question 1

在已知带噪距离`noisyDistance`、吃豆人位置和鬼的真实位置后，返回带噪距离的概率分布。利用`busters.getObservationProbability(noisyDistance, trueDistance)`来构造。距离用`manhattanDistance`。

> 这个`getObservationProbability`方法是如何实现的？

额外考虑“jail”（监狱）的情况。如果pacman抓到了鬼并将其送到“监狱”位置，距离传感器将确定性地返回为`None`。因此，如果鬼的位置是监狱位置，则其`noisyDistance`得到`None`的概率为1，其他任何值的概率都是0。反过来说，如果`noisyDistance != None`，那么这个鬼在监狱中的概率为0，如果`noisyDistance == None`，则鬼在监狱中的概率为1。

Implement `getObservationProb` in `InferenceModule`.

This question requests us to calculate the probability(a distribution) of noisy distance reading,
given the true position of pacman and ghosts, and (if possible) the position of jail, if the ghost is
captured, the ghost will be sent there.

How to implement:

- Calculate the true distance with Manhattan distance(`utils.manhattanDistance`), no matter whether a ghost is captured.

- Consider the case that `noisyDistance` is `None`, and check if `ghostPosition` equals `jailPosition`.

- If the ghost is not captured, use `busters.getObservationProbability(noisyDistance, trueDistance)`, where `trueDistance` is calculated by step 1, using method `manhattanDistance`.

## Question 2

完成`ExactInference`类中的`observeUpdate`方法。该方法将利用`noisyDistance`，更新agent关于鬼位置的信念分布。

需要遍历`self.allPositions`中的每个合法位置，以及“监狱位置”。所谓的“belief”指的是鬼在某个特定位置的概率，被存储在`self.beliefs`，其数据结构应当为`DiscreteDistribution`。

方法指引：

- 利用`self.getObservationProb`来作为主体函数
- 其中Pacman的位置来自`gameState.getPacmanPosition`
- 监狱位置是`self.getJailPosition`

Implement the method `observeUpdate` in `ExactInference` class.

The bayesian likelihood can be obtained by `getObservationProb`, get PacmanPos and JailPos, and iterate over all legal positions for ghosts.

The posterior belief: `self.belief[pos] *= self.getObservationProb(obs, pacman, ghost, jail)`.

## Question 3

加入另一种信念更新的诱因，即pacman清楚鬼的一部分移动特征，例如它不能过墙，也不能一次走两步。譬如，pacman的多次观测发现，绝大多数的观测值都表明鬼离它非常近，只有一次数据发现鬼离它非常远，这个极远的结果可能来自一个buggy sensor，但是，pacman知道，鬼一次只能走一格，而且过不了墙，那么这个极远的noisy distance将被pacman降权。

This question is to implement the `elapseTime` method of `ExactInference` class. We should still iterate over all legal positions, 