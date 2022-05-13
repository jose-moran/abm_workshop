from .strategy import Strategy


class Agent:
    """An Agent class for generic games.
    """

    def __init__(self, s: int = 2) -> None:
        """Initialises an agent with his own set of strategies

        Parameters
        ----------
        s : int, optional
            Number of strategies used by the agent, by default 2
        """
        self.s = s  # number of strategies
        self.Strategies = [Strategy() for i in range(s)]
        self.score = 0  # total number of wins
        self.state = None
        self.action = None

    def act(self, state: str) -> None:
        """Decide which action to take. Chooses agent's best scoring strategy
        then acts based on its response.

        Parameters
        ----------
        state : str
            Current observed state.
        """
        self.state = state
        best_strategy = max(self.Strategies, key=lambda x: x.score)
        self.action = best_strategy.act(state)

    def update(self, winning_choice: str) -> None:
        """Updates scores for the strategies. If a strategy had made the winning
        choice, then its score is increased. It is decreased otherwise.

        Parameters
        ----------
        winning_choice : int
            The winning choice in the game (that of the minority in the
            Minority Game).
        """
        winning_choice = 1 if winning_choice == '0' else -1
        for strategy in self.Strategies:
            if strategy.act(self.state) == winning_choice:
                strategy.update_score(1)
            else:
                strategy.update_score(-1)

        if self.action == winning_choice:
            self.score += 1
        else:
            self.score += -1
