import imageio
import random
from abc import ABC, abstractmethod
from typing import NamedTuple, Sequence

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# ---------------------------------------------------------------------------
# Agent interfaces
#
# A *learner* owns the Q-table and decides HOW to learn from experience.
# An *explorer* decides WHICH action to take, given the current Q-table.
# The training loop (run_env) only talks to these interfaces, so any learner
# can be combined with any explorer.
# ---------------------------------------------------------------------------


class Transition(NamedTuple):
    """One step of experience: in `state` we took `action` and got `reward`."""
    state: int
    action: int
    reward: float


class Learner(ABC):
    """Base class for all learners.

    The training loop calls:
      - reset()        once at the start of every run
      - observe(...)   after every environment step
      - end_episode()  once when an episode is finished
    """

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.reset()

    def reset(self):
        """Forget everything learned so far. Extend this if you keep more state."""
        self.qtable = np.zeros((self.state_size, self.action_size))

    @abstractmethod
    def observe(self, state, action, reward, new_state, terminated):
        """Called after every step with the transition that just happened."""

    def end_episode(self):
        """Called once at the end of every episode. Default: do nothing."""


class EpisodicLearner(Learner):
    """Base class for learners that can only learn once the episode is over
    (e.g. Monte Carlo). It records the trajectory step by step and hands the
    complete episode to `learn_from_episode` at the end.
    """

    def reset(self):
        super().reset()
        self.trajectory = []

    def observe(self, state, action, reward, new_state=None, terminated=None):
        self.trajectory.append(Transition(state, action, reward))

    def end_episode(self):
        self.learn_from_episode(tuple(self.trajectory))
        self.trajectory = []

    @abstractmethod
    def learn_from_episode(self, trajectory: Sequence[Transition]):
        """Update the Q-table from one complete episode (oldest step first)."""


class Explorer(ABC):
    """Base class for all action-selection strategies (policies)."""

    @abstractmethod
    def choose_action(self, action_space, state, qtable) -> int:
        """Return the action to take in `state`."""


def postprocess(episodes, params, rewards, steps, map_size):
    """ To make it easy to plot the results with Seaborn, we'll save the main
    results of the simulation in Pandas dataframes.
    """

    """Convert the results of the simulation in dataframes."""
    res = pd.DataFrame(
        data={
            "Episodes": np.tile(episodes, reps=params.n_runs),
            "Rewards": rewards.flatten(),
            "Steps": steps.flatten(),
        }
    )
    res["cum_rewards"] = rewards.cumsum(axis=0).flatten(order="F")
    res["map_size"] = np.repeat(f"{map_size}x{map_size}", res.shape[0])

    st = pd.DataFrame(data={"Episodes": episodes, "Steps": steps.mean(axis=1)})
    st["map_size"] = np.repeat(f"{map_size}x{map_size}", st.shape[0])
    return res, st


def qtable_directions_map(qtable, map_size):
    """We want to plot the policy the agent has learned in the end. To do that
    we will: 1. extract the best Q-values from the Q-table for each state,
    2. get the corresponding best action for those Q-values, 3. map each
    action to an arrow so we can visualize it.
    """
    """Get the best learned action & map it to arrows."""
    qtable_val_max = qtable.max(axis=1).reshape(map_size, map_size)
    qtable_best_action = np.argmax(qtable, axis=1).reshape(map_size, map_size)
    directions = {0: "←", 1: "↓", 2: "→", 3: "↑"}
    qtable_directions = np.empty(qtable_best_action.flatten().shape, dtype=str)
    eps = np.finfo(float).eps  # Minimum float number on the machine
    for idx, val in enumerate(qtable_best_action.flatten()):
        if qtable_val_max.flatten()[idx] > eps:
            # Assign an arrow only if a minimal Q-value has been learned as best action
            # otherwise since 0 is a direction, it also gets mapped on the tiles where
            # it didn't actually learn anything
            qtable_directions[idx] = directions[val]
    qtable_directions = qtable_directions.reshape(map_size, map_size)
    return qtable_val_max, qtable_directions


def plot_q_values_map(qtable, env, map_size, params, img_label):
    """With the following function, we'll plot on the left the last frame of
    the simulation. If the agent learned a good policy to solve the task, we
    expect to see it on the tile of the treasure in the last frame of the
    video. On the right we'll plot the policy the agent has learned. Each
    arrow will represent the best action to choose for each tile/state.
    """

    """Plot the last frame of the simulation and the policy learned."""
    qtable_val_max, qtable_directions = qtable_directions_map(qtable, map_size)

    # Plot the last frame
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    ax[0].imshow(env.render())
    ax[0].axis("off")
    ax[0].set_title("Last frame")

    # Plot the policy
    sns.heatmap(
        qtable_val_max,
        annot=qtable_directions,
        fmt="",
        ax=ax[1],
        cmap=sns.color_palette("Blues", as_cmap=True),
        linewidths=0.7,
        linecolor="black",
        xticklabels=[],
        yticklabels=[],
        annot_kws={"fontsize": "xx-large"},
    ).set(title="Learned Q-values\nArrows represent best action")
    for _, spine in ax[1].spines.items():
        spine.set_visible(True)
        spine.set_linewidth(0.7)
        spine.set_color("black")
    img_title = f"frozenlake_q_values_{map_size}x{map_size}_{img_label}.png"
    fig.savefig(params.savefig_folder / img_title, bbox_inches="tight")
    plt.show()


def plot_states_actions_distribution(states, actions, map_size, params, img_label):
    """As a sanity check, we can plot the distributions of states and actions
    with the following function:
    """

    """Plot the distributions of states and actions."""
    labels = {"LEFT": 0, "DOWN": 1, "RIGHT": 2, "UP": 3}

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    sns.histplot(data=states, ax=ax[0], kde=True)
    ax[0].set_title("States")
    sns.histplot(data=actions, ax=ax[1])
    ax[1].set_xticks(list(labels.values()), labels=labels.keys())
    ax[1].set_title("Actions")
    fig.tight_layout()
    img_title = f"frozenlake_states_actions_distrib_{map_size}x{map_size}_{img_label}.png"
    fig.savefig(params.savefig_folder / img_title, bbox_inches="tight")
    plt.show()


def plot_steps_and_rewards(rewards_df, steps_df, params):
    """This function plots the cumulated sum of
    rewards, as well as the number of steps needed until the end of the
    episode."""

    """Plot the steps and rewards from dataframes."""
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    sns.lineplot(
        data=rewards_df, x="Episodes", y="cum_rewards", hue="map_size", ax=ax[0]
    )
    ax[0].set(ylabel="Cumulated rewards")

    sns.lineplot(data=steps_df, x="Episodes", y="Steps", hue="map_size", ax=ax[1])
    ax[1].set(ylabel="Averaged steps number")

    for axi in ax:
        axi.legend(title="map size")
    fig.tight_layout()
    img_title = "frozenlake_steps_and_rewards.png"
    fig.savefig(params.savefig_folder / img_title, bbox_inches="tight")
    plt.show()


def record_video(env, Qtable, params, fname, fps=1):
    """
  Generate a replay video of the agent
  :param env
  :param Qtable: Qtable of our agent
  :param fname: filename
  :param fps: how many frame per seconds (with taxi-v3 and frozenlake-v1 we use 1)
  """
    images = []
    terminated = False
    truncated = False
    state, info = env.reset(seed=random.randint(0, 500))
    img = env.render()
    images.append(img)
    done = False
    step = 0
    # while not terminated or truncated:
    while not done:
        # Take the action (index) that have the maximum expected future reward given that state
        action = np.argmax(Qtable[state][:])
        state, reward, terminated, truncated, info = env.step(
            action)  # We directly put next_state = state for recording logic
        img = env.render()
        plot_q_values_map(qtable, env, params.map_size)
        images.append(img)

        done = terminated or truncated
        step += 1

    # writer = imageio.get_writer(fname, fps=fps, plugin="ffmpeg")

    # writer.append_data(imageio.imread(im))
    # writer.append_data([np.array(img) for i, img in enumerate(images)])
    # writer.close()
    # imageio.mimsave(fname , [np.array(img) for i, img in enumerate(images)], fps=fps, plugin="ffmpeg")
