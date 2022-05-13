from random import choice


class Strategy:

    def __init__(self):
        """Initialise a strategy.
        """
        self.score: int = 0  # Strategy's initial score
        self.Responses: dict = {}  # Records the reponse to each state

    def act(self, state: str):
        """Act according to current state.

        Parameters
        ----------
        state : str
            The state: string containing past observed values

        Returns
        -------
        int
            A response: -1 or +1
        """
        if state not in self.Responses:
            self.Responses[state] = choice([-1, 1])
        return self.Responses[state]

    def update_score(self, v=1):
        """Update the score of the strategy.

        Parameters
        ----------
        v : int, optional
            amount by which to update score, by default +1
        """
        self.score += v
