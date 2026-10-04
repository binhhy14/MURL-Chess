# Reinforcement Learning

## What is Reinforcement Learning?

Reinforcement learning (RL) is a method where an agent learns by interacting with an environment.

The basic idea is:

Agent
↓
Action
↓
Environment
↓
Reward
↓
Agent learns from the result

## Main Components

### Agent

The learner that chooses actions.

In chess, the agent can be a chess-playing program.

### Environment

The world in which the agent operates.

For this project, the environment is the chess game.

### State

The current situation.

For chess, the state includes the current board position and whose turn it is.

### Action

A choice made by the agent.

For chess, an action can be a legal chess move.

### Reward

A numerical value that tells the agent how good or bad the result was.

For example:
- Win → positive reward
- Loss → negative reward
- Draw → neutral reward

## Reinforcement Learning and Chess

A chess-playing agent can repeatedly:
1. Observe the board.
2. Choose a move.
3. Play the move.
4. Receive information about the result.
5. Learn from the result.

## Relationship to Neural Networks

A neural network can be used by the RL agent to help estimate which actions or positions are good.

So RL and neural networks are related, but they are not the same thing.

- Reinforcement learning = learning strategy
- Neural network = model that can represent what the agent learns

## Current Status

I am currently learning the basic RL concepts and examining the professor-provided Python starter program.

## Questions

- How does the starter program represent the chess board?
- What is the state?
- What is the action?
- What is the reward?
- Where is the neural network used?
- How does the program update what it has learned?