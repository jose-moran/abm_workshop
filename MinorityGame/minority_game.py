from JMTools import chron
import numpy as np
from .agent import Agent
from typing import List, Tuple
import sys
sys.path.append('..')


class MinorityGame:
    """An implementation of the minority game.

    N agents in Santa Fe decide each day whether they should go to the El Farol
    bar or if they should rather stay at home. This is a binary decision.

    For an agent, the winning choice is that of the minority: go to the bar if
    it's not too crowded, otherwise stay at home.

    Agents decide what to do based on past observations: they look at the M last
    days and decide what to do based on their strategies.
    """

    def __init__(self, N_agents: int,
                 memory_span: int,
                 n_strategies: int) -> None:
        """Initialise a minority game instance.

        Parameters
        ----------
        N : int
            Number of agents in the game.
        M : int
            Memory span of the agents: how far back to look to decide
        s : int
            Number of strategies per agent
        """
        self.N_agents: int = N_agents
        self.memory_span: int = memory_span
        initial_outcome = np.random.choice(['0', '1'],
                                           size=memory_span)
        self.outcomes: str = ''
        for i in initial_outcome:
            self.outcomes += i
        self.agents: List[Agent] = [Agent(n_strategies)
                                    for _ in range(N_agents)]
        self.global_outcome: int = 0
        self.winning_action: str = ''

    def get_state(self) -> str:
        """Get current state, represented by the last outcomes corresponding to
        agents' memory span.

        Returns
        -------
        str
            Last outcomes
        """
        return self.outcomes[-self.memory_span:]

    def act_agents(self) -> None:
        """Make agents act on current state
        """
        state = self.get_state()
        for agent in self.agents:
            agent.act(state)

    def update_agents(self) -> None:
        """Update agents' strategies
        """
        for agent in self.agents:
            agent.update(self.winning_action)

    def update_winning_action(self) -> None:
        """Update the winning action, taken by the minority.
        """
        actions = np.array([agent.action for agent in self.agents])
        self.global_outcome = np.sum(actions)
        if self.global_outcome > 0:
            self.winning_action = '0'
        else:
            self.winning_action = '1'

    def iterate(self) -> None:
        """Run an interation loop:
        - Have the agents act
        - Find out what the winning action was
        - Agents update their strategy score
        """
        self.act_agents()

        self.update_winning_action()

        self.outcomes += self.winning_action
        # agents update their strategies
        self.update_agents()

    @chron
    def run(self, T: int) -> Tuple[np.ndarray, np.ndarray]:
        """Run the simulation over T timesteps

        Parameters
        ----------
        T : int
            Number of timesteps over which to run the simulation
        timed : bool
            Extra parameter from chron wrapper: set to true to time run.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            First array: N_agents by T array, where coordinate [t,i] contains
            the score of agent i at time t.
            Second array: global outcome at time t (sum of agents actions,
            +1 if they went to the bar, -1 otherwise).
        """
        agent_scores = np.empty(
            (self.N_agents, T)
        )
        global_outcomes = np.empty(T)
        for i in range(T):
            self.iterate()
            global_outcomes[i] = self.global_outcome
            agent_scores[:, i] = [agent.score for agent in self.agents]
        return global_outcomes, agent_scores
