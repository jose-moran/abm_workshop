from .strategy import Strategy


class Agent:
    """An Agent class for generic games.
    """

    def __init__(self, n_strategies: int = 2) -> None:
        """Initialises an agent with his own set of strategies

        Parameters
        ----------
        n_strategies : int, optional
            Number of strategies used by the agent, by default 2
        """
        self.n_strategies = n_strategies  # number of strategies
        self.strategies = [Strategy() for _ in range(n_strategies)]
        self.score: int = 0  # total number of wins
        self.state: str = ''
        self.action: int = 0

    def act(self, state: str) -> None:
        """Decide which action to take. Chooses agent's best scoring strategy
        then acts based on its response.

        Parameters
        ----------
        state : str
            Current observed state.
        """
        self.state = state
        best_strategy = max(self.strategies,
                            key=lambda x: x.score)
        self.action = best_strategy.act(state)

    def update(self, winning_action: str) -> None:
        """Updates scores for the strategies. If a strategy had made the winning
        choice, then its score is increased. It is decreased otherwise.

        Parameters
        ----------
        winning_choice : int
            The winning choice in the game (that of the minority in the
            Minority Game).
        """
        winning_choice_int = 1 if winning_action == '1' else -1
        for strategy in self.strategies:
            if strategy.act(self.state) == winning_choice_int:
                strategy.update_score(1)
            else:
                strategy.update_score(-1)

        if self.action == winning_choice_int:
            self.score += 1
        else:
            self.score += -1

    def __str__(self) -> str:
        strep = ''
        for i, s in enumerate(self.strategies):
            strep += f'Strategy {i}:'
            strep += '\n' + str(s) + '\n'
            strep += '='*15 + '\n\n'
        return strep
