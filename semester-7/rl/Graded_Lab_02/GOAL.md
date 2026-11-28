# Goal

Train a from-scratch DQN agent (exposing `agent.select_action(states)`) that solves
LunarLander-v2 — mean reward ≥ 200 over 10 evaluation episodes — and produce the
learning curves, evaluation score and video for the report.

## Success criteria
- [ ] DQN implemented from scratch in PyTorch (Q-network, replay buffer, target network, ε-greedy)
- [ ] Trained for 1,000,000 timesteps on the 16-env vectorized environment (MPS backend)
- [ ] Learning curve (episode reward vs. episodes) plotted
- [ ] Mean ± std reward over 10 evaluation episodes on a separate eval env
- [ ] Video of one episode of the trained agent, linked in the report
- [ ] Report (≤3 pages + ≤1 page discussion) with hyperparameters and how they were chosen

## Team
Jann Erhardt, Gian Gamper (gampegia)

## Current focus
Baseline done (273.54 ± 24.55, runs/dqn_lunarlander_20261125-085950). HPO overnight: 70 trials × 300k, 9 params → then re-validate top 3 on 1M → report

## Parking lot (later, not part of this lab's DQN submission)
- **PPO**: policy network outputs a probability distribution over actions → softmax
  output head (contrast with DQN's Q-network, which is regression over action values).
  PPO also needs a value head (regression, like DQN). Compare against DQN once DQN works.
- **Hyperparameter optimisation (after baseline)**: Optuna/TPE with pruning on shorter trials
  (~200–300k transitions), 3–5 params, re-validate top configs on full 1M runs.
  Prerequisite: refactor the training loop into `train(config, total_timesteps, report=None)`.
  Open decisions: compute budget, search space, objective (greedy eval vs. last-100 vs. AUC), seed noise.
