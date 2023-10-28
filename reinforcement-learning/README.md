# Bellman Equation in Reinforcement Learning

The Bellman equation is a crucial concept in reinforcement learning, offering a recursive relationship between the value of a state and the values of its successor states. Named after Richard Bellman, this equation is essential for finding the optimal value function, which indicates the maximum expected cumulative reward achievable from a given state.

## Types of Bellman Equations

### 1. Bellman Equation for Value Functions

This form of the Bellman equation connects a state's value to the values of its successor states under a specific policy \( \pi \).

\[ V^\pi(s) = \sum_{a} \pi(a|s) \sum_{s', r} P(s', r | s, a) \left[ r + \gamma V^\pi(s') \right] \]

- \( V^\pi(s) \): Value of state \( s \) under policy \( \pi \)
- \( \pi(a|s) \): Probability of taking action \( a \) in state \( s \) under policy \( \pi \)
- \( P(s', r | s, a) \): Transition probability to state \( s' \) with reward \( r \) from state \( s \) after taking action \( a \)
- \( \gamma \): Discount factor, accounting for the agent's consideration for future rewards

### 2. Bellman Optimality Equation

This version of the equation defines the optimal value function, reflecting the maximum expected cumulative reward from each state, irrespective of the initial policy.

\[ V^*(s) = \max_{a} \sum_{s', r} P(s', r | s, a) \left[ r + \gamma V^*(s') \right] \]

- \( V^*(s) \): Optimal value of state \( s \)
- Remaining symbols have the same meanings as in the first equation.

## Application in Reinforcement Learning

These Bellman equations play a pivotal role in numerous reinforcement learning algorithms, aiding in the derivation of policies that maximize expected cumulative rewards. Solving these equations yields the value functions, facilitating the discovery of the optimal policy. The iterative process of applying the Bellman equation to refine value functions until they reach convergence is termed value iteration.
