"""Snake & Ladder Terminal Game
By Vishesh Bajpayee
features-
1. Customisable Board(OPTIONAL FEATURE)
2. Game continues after a players wins
and player count > 2(OPTIONAL FEATURE)
3. Shows stats after game ends(OPTIONAL FEATURE)
4. Customisable player count
5. Customisable Snake & Ladder count
6. Customisable Snake & ladder position
7. Scalable Code(OPTIONAL FEATURE)
8. OOPs implimentation
"""


import random
import time


class Player:
    def __init__(self, name):
        self.won = False
        self.playerName = name
        self.playerState = 0

    def setState(self, playerState):
        self.playerState = playerState

    def getState(self):
        return self.playerState


class Game:
    numberOfPlayers = 0
    playerNamesList = None
    NumberOfLadders = 0
    NumberOfSnakes = 0
    snakes = None
    ladders = None
    number_of_dice = 1
    leaderboard = None

    def __init__(self):
        self.set_board()
        self.SetPlayer()
        self.SetSnakes()
        self.SetLadders()
        self.generateFst()
        self.leaderboard = []

    def set_board(self):
        self.board_size = int(input("Enter number of squares: "))
        self.board = list(range(1, self.board_size + 1))

    def SetPlayer(self):
        numberOfPlayers = int(input("Enter number of players: "))
        self.numberOfPlayers = numberOfPlayers
        playerNameList = []
        for i in range(numberOfPlayers):
            playerName = input(f"Enter player {i + 1} name: ")
            playerNameList.append(Player(playerName))
        self.playerNamesList = playerNameList

    def rolldice(self):
        rollDice = [random.randint(1, 6) for _ in range(self.number_of_dice)]
        return rollDice

    def is_double_turn(self, dice_roll):
        return all([r == 6 for r in dice_roll])

    def SetSnakes(self):
        snakes = []
        numberOfSnakes = int(input("Enter number of snakes: "))
        assert(numberOfSnakes >= 0)
        i = 0
        while i < numberOfSnakes:
            s = int(input(f"Enter snake {i + 1} start position: "))
            e = int(input(f"Enter snake {i + 1} end position: "))
            if s <= e or s <= 0 or s > self.board_size or e <= 0 or e > self.board_size:
                print("Values are incorrect please try again.")
                continue
            snakes.append((s, e))
            i += 1
        self.snakes = snakes
        self.numberOfSnakes = numberOfSnakes

    def SetLadders(self):
        ladders = []
        numberOfLadders = int(input("Enter number of ladders: "))
        assert (numberOfLadders >= 0)
        i = 0
        while i < numberOfLadders:
            s = int(input(f"Enter ladder {i + 1} start position: "))
            e = int(input(f"Enter ladder {i + 1} end position: "))
            if s >= e or s <= 0 or s > self.board_size or e <= 0 or e > self.board_size:
                print("values are incorrect please try again")
                continue

            all_locs = [loc for sublist in self.snakes for loc in sublist]
            if e in all_locs or s in all_locs:
                print("Cant add ladder at the same location as snake")
                continue
            ladders.append((s, e))
            i += 1
        self.ladders = ladders
        self.numberOfLadders = numberOfLadders

    def playTurn(self, k, diceValue):
        player = self.playerNamesList[k]
        print(f"Player {player.playerName} is at: {player.playerState}")
        print("The dice rolls: ", diceValue)
        val = player.playerState + sum(diceValue)
        if val > self.board_size:
            return False
        if val == self.board_size:
            return True
        while self.fst[val] != val:
            val = self.fst[val]
            print(val, self.fst[val])
        player.playerState = val
        print(f"Player {player.playerName} reaches to: {player.playerState}")
        return False

    def generateFst(self):
        self.fst = {x: x for x in self.board}
        for snake in self.snakes:
            self.fst[snake[0]] = snake[1]
        for ladder in self.ladders:
            self.fst[ladder[0]] = ladder[1]

    def playGame(self):
        k = 0
        while True:
            prior_state = self.playerNamesList[k].playerState
            sixes_count, turn = 0, True
            while turn:
                turn = False
                print(f"Its {self.playerNamesList[k].playerName}'s turn")
                input("Press Enter to roll a Dice: ")
                diceValue = self.rolldice()
                if self.playTurn(k, diceValue):
                    print(
                        f"{self.playerNamesList[k].playerName} has finished the game")
                    self.leaderboard.append(self.playerNamesList[k].playerName)
                    del self.playerNamesList[k]
                    k -= 1
                    if len(self.playerNamesList) == 1:
                        self.leaderboard.append(
                            self.playerNamesList[0].playerName)
                        print("Final positions:")
                        print([(i + 1, v)
                               for i, v in enumerate(self.leaderboard)])
                        return
                    break
                time.sleep(1.5)
                if self.is_double_turn(diceValue):
                    turn = True
                    sixes_count += 1
                if sixes_count == 3:
                    self.playerNamesList[k].playerState = prior_state
                    print("3 Sixes in a row, cancelling the turn")
                    break
            k = (k + 1) % len(self.playerNamesList)


if __name__ == '__main__':
    gameBegins = Game()
    gameBegins.playGame()