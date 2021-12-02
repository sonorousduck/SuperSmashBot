class Reward:
    def __init__(self):
        self.stocks = 4
        self.percent = 0
        self.opponent_stocks = 4
        self.opponent_percent = 0




    def understandState(self, playerData, otherPlayerData):
        reward = 0
        changed = False

        if self.stocks > int(playerData.stock):
            reward -= 450
            self.stocks = int(playerData.stock)
            changed = True

        if self.percent < playerData.percent:
            reward -= .75 * (abs(self.percent - playerData.percent))
            self.percent = playerData.percent
            changed = True


        if self.opponent_stocks > int(otherPlayerData.stock):
            reward += 200
            self.opponent_stocks = int(otherPlayerData.stock)
            changed = True


        if self.opponent_percent < otherPlayerData.percent:
            reward += 0.5 * (abs(self.opponent_percent - otherPlayerData.percent))
            self.opponent_percent = otherPlayerData.percent
            changed = True

        if not changed:
            # Give a punishment for nothing happening too
            reward -= 1

        return reward

    def reset(self):
        self.stocks = 4
        self.percent = 0
        self.opponent_stocks = 4
        self.opponent_percent = 0




