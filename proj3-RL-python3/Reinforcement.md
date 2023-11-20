# Note for Project 3 Reinforcement Learning

## Target Files

- `valueIterationAgents.py` for Question 1, 4, 5,
- `qlearningAgents.py` for Question 6, 7, 9, 10
- `analysis.py` for question 2, 3, 8

## Debugger setting for vscode

```json
{
    "version": "0.2.0",
    "configurations": [

        {
            "name": "Python: valueIterationAgent",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/autograder.py",
            "args": ["-q","q5"], 
            "cwd": "D:/Repositories/cs188_proj_2018Fall/proj3-RL-python3",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

However, the debugger used in VScode requires python >= 3.7, and our autograder only supports python = 3.6. So it's better to debug with Jetbrains Pycharm.

## Question 1

This question requires you to implement class "valueIterationAgent", by filling function `runValueIteration`, `computeQvalueFromValues` and `computeActionFromValues` in `valueIterationAgents.py`.

### Q-value function

According to the logic of MDP, we first implement `computeQvalueFromValues`:

- Input: `state` and `action`

- Initialize `q_value` as 0.

- step1: find all possible next states `next_state`, with their probabilities`prob`, we can use `self.mdp.getTransitionStatesAndProbs(state, action)` to get them.

- step2: for each possible state in `next_state`, require the reward, this is a function of current state, action and possible next state. We can use `self.mdp.getReward(state, action, next_state)` to get it.

- step3: the `q_value` is the weighted average of all possible next states' reward and discounted value of next state. The discount factor is `self.discount`. The value of next state can be computed by `self.values[next_state]`.

- Output: `q_value`

These steps above strictly follows the Q function formula:

$$
Q^{*}(s,a) = \sum_{s'}T[s,a,s'](R(s,a,s') + \gamma V^{*}(s'))
$$

where $s,a,s'$ is the current state, action choosen and next state. $T(s,a,s')$ is the probability of transition from $s$ to $s'$ under action $a$. $R(s,a,s')$ is the reward of transition from $s$ to $s'$ under action $a$. $\gamma$ is the discount factor. $V^{*}(s')$ is the value (V function) of next state $s'$.

### Best Action

Secondly, we implement method `computeActionFromValues`:

- Input: `state`

- Initialize `best_action` as `None`, `best_score` as a extremely small number, for example, `-1e9`(negative one billion) or `float('-inf')`.

- Step1: if no legal action for current state, return `None` directly.

- Step2: for each legal action, require its Q value by `self.computeQvalueFromValues(state, action)`, and compare it with `best_score`, if it is strictly larger, update `best_score` and `best_action`.

- Output: `best_action`

These step above strictly follows V function:

$$
V^{*}(s) = \max_{a}Q^{*}(s,a) = \max_{a}\sum_{s'}T[s,a,s'](R(s,a,s') + \gamma V^{*}(s'))
$$

where $s$ is the current state, $a$ is the action choosen. $Q^{*}(s,a)$ is the Q function of current state and action.

### Value Iteration

Finally, we implement method `runValueIteration`:

- This function requires nothing but `self`.
  
>This method updates all states' value simultaneously, so we need to use a temporary variable `new_values` to store the new values, and update `self.values` after all states' value are updated.

- Initialize `new_values` and `update_flag` as two instances of `util.Counter()`, which is a better dictionary, returning default value 0 for all uncontained keys.

  - `new_values` is used to store the new values of all states.

  - `update_flag` is used to record whether the value of any state is updated.
  
> **Caution**
>
> In fact, all updates in `new_values` will be synchronized to the actual value table, `self.values`, without any selection. However, we cannot update `self.values` immediately because the evaluation of potential states that have not been traversed yet depends on the unupdated `self.values`. If we evaluate and update simultaneously, it would lead to significant learning bias, as the value of later-evaluated states would be influenced by the previous-evaluated state values.
>

- No output.

Main function is in a `while` loop, which will terminate when `self.iteration` reaches 0, as `self.iteation` will minus 1 in each iteration.

- Step1: for each state, compute its best action by `self.computeActionFromValues(state)`, and update `new_values[state]` by `self.computeQvalueFromValues(state, best_action)`.

- Step2: after **ALL** states' value are updated, update `self.values` by `new_values`, using `update_flag` to show which value should be updated.

Therefore, we need to iterate twice over the set of states in a single iteration.

Now, we can execute:

> Use the recommended python env as Python 3.6.
>
> This course may not recommend a requirement.txt for us, unlike CS285.

```shell
python gridworld.py -a value -i 5
```

to get the same image as in the project description.

## Question 2

Change the `question2` function in `analysis.py`. We are only permitted to change only one parameter.

To avoid dropping into high-penalty states beside the "bridge", we should forbid the agent to "explore freely", therefore we can set `noise` as a very little value, even `0`.

Changes of discount rate is helpless when we want to avoid agent from dropping into unexpected states. In Qvalue-based action choice, the agent will always choose the action with the highest Qvalue, those actions with high penalty(high negative reward) are extremely unlikely to be chosen, for a "rational agent".

## Question 3

Change all `question3` funcs in `analysis.py`. This is a possible parameter setting below.

|Ques No.|Agent Preference|disc|noise|living|
|--|--|--|--|--|
|1|prefer the close exit (+1), risking the cliff (-10)|0.8|0.2|-3|
|2|prefer the close exit (+1), but avoiding the cliff (-10)|0.2|0.2|-0.5|
|3|prefer the distant exit (+10), risking the cliff (-10)|1|0|-1|
|4|prefer the distant exit (+10), avoiding the cliff (-10)|0.7|0.2|2|
|5|avoid both exits and the cliff (so an episode should never terminate)|0|1|0|

### Risk or avoid cliff

To train an agent to risk the cliff, we should set `noise` as a little value, thus the agent will learn little from the cliff and their V table has little information about the high penalty from the "cliff". Then, we can set `living` as a high penalty, so that the agent will prefer to risk the cliff than living in the high-penalty states.

To train an agent to avoid the cliff, we give a higher `noise` and positive `living`, leading agent to safer states.

### Close or distant exit

To train an agent to prefer the further terminal with higher reward, we just increase the `discount` factor, to emphasize the future reward.

### Avoid both exits and the cliff

It's a weird query. We can set `discount` as 0, so that the agent will only care about the immediate reward.

We set `noise` as 1, thus it's impossible for agent to choose the best action.

> *Noise refers to how often an agent ends up in an unintended successor state when they perform an action.*
>
> *(Description in Problem 2)*

`Living` can be set as any value, as the agent will never terminate, because of no-best-choice setting.

## Question 4

A simple change from value iteration process.

- No input but need a `valueIterationAgent` instance.

- Step 1: require the list of all states in this environment, and record the number of states using `len(state_list)`.

- Step 2: for iteration flag `i` (meaning that this is the `i+1`th iteration), pick `state_list[i]` as the list to learn and value-update.

- Step 3: find its best action's Q value as the value of `state_list[i]`, using `self.computeActionFromValues(state_list[i])` and `self.computeQvalueFromValues(state_list[i], best_action)`. So we complete updating in an iteration.

- No output.

> (*In Chinese*) 这个题目的名字叫“异步价值迭代”，这是一种用于降低计算开支的训练方法，因为传统的价值迭代需要在每一轮遍历所有的可能状态，而这对于一些复杂的环境是比较困难的。
>
> 而异步迭代方法则在每一轮遍历中选择一部分（极端情况如Question 4，一次迭代一个状态）状态进行迭代，以任意的顺序进行更新，可能会导致部分状态更新很多次，而有的状态一次都没有更新的情况出现，为了正确收敛，需要增加迭代的次数并不断更新所有状态的值。
>
> 但是，异步迭代在计算开支上具有显著的优势，并且在每一轮更新的状态集选择上具有极大的灵活性。如Sutton & Barto指出的，有些状态与最优决策关系很小，所以可以放缓更新的频率，甚至直接跳过该状态。而有些状态则与最优决策关系很大，可以加快更新频率。简要的介绍参照Sutton & Barto 的章节4.5，关于状态取舍的问题，参照第8章的相关内容。
>
> (*In English*) The title of this question is "Asynchronous Value Iteration," which is a training method used to reduce computational expenses because traditional value iteration requires iterating over all possible states in each round, which can be challenging for complex environments.
>
> In contrast, asynchronous iteration methods select a subset of states to iterate over in each round, with the flexibility to update them in any order. This may result in some states being updated multiple times while others are not updated at all. To ensure proper convergence, the number of iterations needs to be increased, continually updating the values of all states.
>
> However, asynchronous iteration offers significant advantages in terms of computational costs and provides great flexibility in selecting the set of states to update in each round. As Sutton & Barto pointed out, some states have little relevance to optimal decision-making, allowing for a slower update frequency or even skipping those states altogether. On the other hand, some states have a significant impact on optimal decision-making and can be updated more frequently. A brief introduction can be found in Chapter 4.5, and Chapter 8 provides relevant content on the issue of state selection.

## Question 5

This question asks us to implement `PrioritizedSweepingValueIterationAgent` in `valueIterationAgents.py`. Which is an inheritance of `AsynchronousValueIterationAgent` (a grandson of `ValueIterationAgent` :p).

This value iteration method will focus on states which are likely to change the policy.

> 这种“优先扫描价值迭代”可能与Sutton & Barto书中章节8.4的“优先遍历”一致。

Be careful, the data structure `util.Counter` is a "better dictionary", but it limits its value as integar. So we build `predecessors` as dictionary.

Projects document has shown us the algorithm we should to implement, so read code for details.

> Be careful for idention.

Now we complete the `valueIterationAgents.py` file.