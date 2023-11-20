# Note for Project 3 Reinforcement Learning

## Target Files

- `valueIterationAgents.py` for Question 1, 4, 5,
- `qlearningAgents.py` for Question 6, 7, 9, 10
- `analysis.py` for question 2, 3, 8

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
Q^{*}(s,a) = \sum_{s'}T(s,a,s')[R(s,a,s') + \gamma V^{*}(s')]
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
V^{*}(s) = \max_{a}Q^{*}(s,a) = \max_{a}\sum_{s'}T(s,a,s')[R(s,a,s') + \gamma V^{*}(s')]
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
> Use `update_flag` to avoid the In fact, all updates in `new_values` will be synchronized to the actual value table, `self.values`, without any selection. However, we cannot update `self.values` immediately because the evaluation of potential states that have not been traversed yet depends on the unupdated `self.values`. If we evaluate and update simultaneously, it would lead to significant learning bias, as the value of later-evaluated states would be influenced by the previous-evaluated state values.
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

