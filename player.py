class Player:

    def __init__(self, name, team, games, position, goals, assists, plusMinus, goalieWins, goalieLosses, goalieShutouts):
        self._name = name
        self._team = team
        self._games = games
        self._position = position
        self._goals = goals
        self._assists = assists
        self._plusMinus = plusMinus
        self._goalieWins = goalieWins
        self._goalieLosses = goalieLosses
        self._goalieShutouts = goalieShutouts

    def getName(self):
        return self._name

    def getTeam(self):
        return self._team

    def getPosition(self):
        return self._position

    def getGoals(self):
        return self._goals

    def getAssists(self):
        return self._assists

    def getPlusMinus(self):
        return self._plusMinus

    def getGoalieWins(self):
        return self._goalieWins

    def getGoalieLosses(self):
        return self._goalieLosses

    def getGoalieShutouts(self):
        return self._goalieShutouts
