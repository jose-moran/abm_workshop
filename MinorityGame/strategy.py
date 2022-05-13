from random import choice


class Strategy:
    """A strategy class: implements a dictionary that associates a binary
    response (+1 or -1) to an abstract state.
    The state only needs to be a hashable object.
    """

    def __init__(self) -> None:
        """Initialise a strategy.
        """
        self.score: int = 0  # Strategy's initial score
        self.Responses: dict = {}  # Records the reponse to each state

    def act(self, state: str) -> int:
        """Act according to current state. If the state hasn't been observed,
        a random response is initialised as a strategy to it.

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

    def update_score(self, v=1) -> None:
        """Update the score of the strategy.

        Parameters
        ----------
        v : int, optional
            amount by which to update score, by default +1
        """
        self.score += v
