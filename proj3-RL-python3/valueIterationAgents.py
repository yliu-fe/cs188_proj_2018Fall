# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        while self.iterations:
            self.iterations -= 1
            new_values = util.Counter()
            update_flag = util.Counter()
            for state in states:
                best_action = self.computeActionFromValues(state)
                if best_action is not None:
                    new_values[state] = self.computeQValueFromValues(state, best_action)
                    update_flag[state] == 1
            # Notice: the update process should hold behind choosing best_actions for all states, 
            # otherwise V func(self.values) updated will mislead the best_action choice.
            for state in states:
                if update_flag:
                    self.values[state] = new_values[state]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        possible_states = self.mdp.getTransitionStatesAndProbs(state, action)
        q_value = 0
        for next_state, prob in possible_states:
            reward = self.mdp.getReward(state, action, next_state)
            q_value += prob * (reward + self.discount * self.values[next_state])

        return q_value
        

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        possible_actions = self.mdp.getPossibleActions(state)
        if len(possible_actions) == 0:
            return None
        best_action = None
        best_value = float('-inf')
        for action in possible_actions:
            q_value = self.computeQValueFromValues(state, action)
            if q_value > best_value:
                best_value = q_value
                best_action = action
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        legal_states = self.mdp.getStates()
        num_states = len(legal_states)
        for i in range(self.iterations):
            current_state = legal_states[i % num_states]
            if self.mdp.isTerminal(current_state):
                continue
            best_action = self.computeActionFromValues(current_state)
            if best_action is not None:
                self.values[current_state] = self.computeQValueFromValues(current_state, best_action)
            else:
                self.values[current_state] = 0.0


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors = {} 
        legal_states = self.mdp.getStates()
        # 1. Compute predecessor states for all states
        for state in legal_states:
            if self.mdp.isTerminal(state):
                continue
            for action in self.mdp.getPossibleActions(state):
                if action is not None:
                    for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        if prob > 0:
                            if next_state in predecessors:
                                predecessors[next_state].add(state)
                            else:
                                predecessors[next_state] = {state}
        # 2. Initialize an empty priority queue
        priority_queue = util.PriorityQueue()

        # 3. For each non-terminal state s, do:
        for state in legal_states:
            if self.mdp.isTerminal(state):
                continue
            # 3a. Find the absolute value of the difference between the current value of s in self.values
            # and the highest Q-value across all possible actions from s (this represents what the value should be);
            # call this number diff. Do NOT update self.values[s] in this step.
            value = []
            for action in self.mdp.getPossibleActions(state):
                q_value = self.computeQValueFromValues(state,action)
                value.append(q_value)
            diff = abs(self.values[state] - max(value))
            # 3b. Push s into the priority queue with priority -diff (note that this is negative).
            # We use a negative because the priority queue is a min heap,
            # but we want to prioritize updating states that have a higher error.
            priority_queue.update(state, -diff)

        # 4. For iteration in 0, 1, 2, ..., self.iterations - 1, do:
        for i in range(self.iterations):
            # 4a. If the priority queue is empty, then terminate.
            if priority_queue.isEmpty():
                break
            # 4b. Pop a state s off the priority queue.
            current_state = priority_queue.pop()
            # 4c. Update s's value (if it is not a terminal state) in self.values.
            if self.mdp.isTerminal(current_state):
                continue
            values = []
            for action in self.mdp.getPossibleActions(current_state):
                q_value = self.computeQValueFromValues(current_state, action)
                values.append(q_value)
            self.values[current_state] = max(values)

            # 4d. For each predecessor p of s, do:
            for p in predecessors[current_state]:
                # 4d i. Find the absolute value of the difference between the current value of p in self.values
                # and the highest Q-value across all possible actions from p
                # (this represents what the value should be); call this number diff.
                # Do NOT update self.values[p] in this step.
                if self.mdp.isTerminal(p):
                    continue
                value = []
                for action in self.mdp.getPossibleActions(p):
                    q_value = self.computeQValueFromValues(p, action)
                    value.append(q_value)
                diff = abs(self.values[p] - max(value))
                # 4d ii. If diff > theta, push p into the priority queue with priority -diff
                # (note that this is negative),
                # as long as it does not already exist in the priority queue with equal or lower priority.
                # As before, we use a negative because the priority queue is a min heap,
                # but we want to prioritize updating states that have a higher error.
                if diff > self.theta:
                    priority_queue.update(p, -diff)
