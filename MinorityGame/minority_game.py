import numpy as np
from .agent import Agent
from typing import List


class MinorityGame:
    """An implementation of the minority game.

    N agents in Santa Fe decide each day whether they should go to the El Farol
    bar or if they should rather stay at home. This is a binary decision.

    For an agent, the winning choice is that of the minority: go to the bar if
    it's not too crowded, otherwise stay at home.

    Agents decide what to do based on past observations: they look at the M last
    days and decide what to do based on their strategies.
    """

    def __init__(self, N: int, M: int, s: int):
        """Initialise a minority game instace.

        Parameters
        ----------
        N : int
            Number of agents in the game.
        M : int
            Memory span of the agents: how far back to look to decide
        s : int
            Number of strategies per agent
        """
        self.N_agents: int = N
        self.memory_span: int = M
        initial_outcome = np.random.choice(['0', '1'],
                                           size=M)
        self.outcomes: str = ''
        for i in initial_outcome:
            self.outcomes += i
        self.agents: List[Agent] = [Agent(s) for _ in range(N)]
        self.global_outcome: int = 0
        self.winning_action: int = 0

    def get_state(self):
        """Get current state, represented by the last outcomes corresponding to
        agents' memory span.

        Returns
        -------
        str
            Last outcomes
        """
        return self.outcomes[-self.memory_span:]

    def winning_action_to_string(self):
        """Returns the winning action, represented by a 0 or 1 here.

        Returns
        -------
        str
            Winning action, '0' or '1'
        """
        if self.winning_action == 1:
            return '1'
        else:
            return '0'

    def act_agents(self):
        """Make agents act on current state
        """
        state = self.get_state()
        for agent in self.agents:
            agent.act(state)

    def update_agents(self):
        """Update agents' strategies
        """
        for agent in self.agents:
            agent.update(self.winning_action)

    def update_winning_action(self):
        """Update the winning action, taken by the minority.
        """
        actions = np.array([agent.action for agent in self.agents])
        self.global_outcome = np.sum(actions)
        if self.global_outcome > 0:
            self.winning_action = '0'
        else:
            self.winning_action = '1'

    def iterate(self):
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
