class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self):
        """Initialize statistics."""
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = 3
        self.score = 0
        self.level = 0

    def update_scores(self, new_score):
        """Adds to the score and updates the high score."""
        self.score += new_score
        if self.score > self.high_score:
            self.high_score = self.score
