from asyncio.windows_events import NULL
from distutils import command
from threading import currentThread
from tkinter import *
import tkinter
from turtle import color
from PIL import ImageTk, Image
import requests
import datetime
from player import Player

#Features:
#1. Current games for the day and their scores/info page
#2. Page listing the league standings per division
#3. Player stats page

root = Tk()
root.title('NHL Stats App')
root.iconbitmap('pics/nhlLogos/puck.ico')
api_key = "46210c73e0464fd580a04f88e2f5d95a"


#Dictionary with the team logos
standardWidth = 25
standardHeight = 25
teamLogos = {
'ANA': ImageTk.PhotoImage(Image.open('pics/nhlLogos/anaheimDucks.png').resize((standardWidth,standardHeight))), #Anaheim
'ARI': ImageTk.PhotoImage(Image.open('pics/nhlLogos/phoenixCoyotes.png').resize((standardWidth,standardHeight))), #Arizona
'BOS': ImageTk.PhotoImage(Image.open('pics/nhlLogos/bostonBruins.png').resize((standardWidth,standardHeight))), #Boston
'BUF': ImageTk.PhotoImage(Image.open('pics/nhlLogos/buffaloSabres.png').resize((standardWidth,standardHeight))), #Buffalo
'CGY': ImageTk.PhotoImage(Image.open('pics/nhlLogos/calgaryFlames.png').resize((standardWidth,standardHeight))), #Calgary
'CAR': ImageTk.PhotoImage(Image.open('pics/nhlLogos/carolinaHurricanes.png').resize((standardWidth,standardHeight))), #Carolina
'CHI': ImageTk.PhotoImage(Image.open('pics/nhlLogos/chicagoBlackhawks.png').resize((standardWidth,standardHeight))), #Chicago
'COL': ImageTk.PhotoImage(Image.open('pics/nhlLogos/coloradoAvalanche.png').resize((standardWidth,standardHeight))), #Colorado
'CBJ': ImageTk.PhotoImage(Image.open('pics/nhlLogos/columbusBlueJackets.png').resize((standardWidth,standardHeight))), #Columbus
'DAL': ImageTk.PhotoImage(Image.open('pics/nhlLogos/dallasStars.png').resize((standardWidth,standardHeight))), #Dallas
'DET': ImageTk.PhotoImage(Image.open('pics/nhlLogos/detroitRedWings.png').resize((standardWidth,standardHeight))), #Detroit
'EDM': ImageTk.PhotoImage(Image.open('pics/nhlLogos/edmontonOilers.png').resize((standardWidth,standardHeight))), #Edmonton
'FLA': ImageTk.PhotoImage(Image.open('pics/nhlLogos/floridaPanthers.png').resize((standardWidth,standardHeight))), #Florida
'LA': ImageTk.PhotoImage(Image.open('pics/nhlLogos/losAngelesKings.png').resize((standardWidth,standardHeight))), #Los Angeles
'MIN': ImageTk.PhotoImage(Image.open('pics/nhlLogos/minnesotaWild.png').resize((standardWidth,standardHeight))), #Minnesota
'MON': ImageTk.PhotoImage(Image.open('pics/nhlLogos/montrealCanadiens.png').resize((standardWidth,standardHeight))), #Montreal
'NAS': ImageTk.PhotoImage(Image.open('pics/nhlLogos/nashvillePredators.png').resize((standardWidth,standardHeight))), #Nashville
'NJ': ImageTk.PhotoImage(Image.open('pics/nhlLogos/newJerseyDevils.png').resize((standardWidth,standardHeight))), #NewJersey
'NYI': ImageTk.PhotoImage(Image.open('pics/nhlLogos/newYorkIslanders.png').resize((standardWidth,standardHeight))), #NY Islanders
'NYR': ImageTk.PhotoImage(Image.open('pics/nhlLogos/newYorkRangers.png').resize((standardWidth,standardHeight))), #NY Rangers
'OTT': ImageTk.PhotoImage(Image.open('pics/nhlLogos/ottawaSenators.png').resize((standardWidth,standardHeight))), #Ottawa
'PHI': ImageTk.PhotoImage(Image.open('pics/nhlLogos/philadelphiaFlyers.png').resize((standardWidth,standardHeight))), #Philadelphia
'PIT': ImageTk.PhotoImage(Image.open('pics/nhlLogos/pittsburghPenguins.png').resize((standardWidth,standardHeight))), #Pittsburgh
'SJ': ImageTk.PhotoImage(Image.open('pics/nhlLogos/sanJoseSharks.png').resize((standardWidth,standardHeight))), #San Jose
'STL': ImageTk.PhotoImage(Image.open('pics/nhlLogos/stLouisBlues.png').resize((standardWidth,standardHeight))), #St Louis
'TB': ImageTk.PhotoImage(Image.open('pics/nhlLogos/tampaBayLightning.png').resize((standardWidth,standardHeight))), #Tampa Bay
'TOR': ImageTk.PhotoImage(Image.open('pics/nhlLogos/torontoMapleLeafs.png').resize((standardWidth,standardHeight))), #Toronto
'VAN': ImageTk.PhotoImage(Image.open('pics/nhlLogos/vancouverCanucks.png').resize((standardWidth,standardHeight))), #Vancouver
'VEG': ImageTk.PhotoImage(Image.open('pics/nhlLogos/vegasGoldenKnights.png').resize((standardWidth,standardHeight))), #Las Vegas
'WAS': ImageTk.PhotoImage(Image.open('pics/nhlLogos/washingtonCapitals.png').resize((standardWidth,standardHeight))), #Washington
'WPG': ImageTk.PhotoImage(Image.open('pics/nhlLogos/winnipegJets.png').resize((standardWidth,standardHeight))), #Winnipeg
'SEA': ImageTk.PhotoImage(Image.open('pics/nhlLogos/seattleKraken.png').resize((standardWidth,standardHeight))), #Seattle
'PACIFIC': ImageTk.PhotoImage(Image.open('pics/nhlLogos/pacificDivision.png').resize((standardWidth,standardHeight))), #Pacific
'ATLANTIC': ImageTk.PhotoImage(Image.open('pics/nhlLogos/atlanticDivision.png').resize((standardWidth,standardHeight))), #Atlantic
'CENTRAL': ImageTk.PhotoImage(Image.open('pics/nhlLogos/centralDivision.png').resize((standardWidth,standardHeight))), #Central
'METRO': ImageTk.PhotoImage(Image.open('pics/nhlLogos/metroPolitanDivision.png').resize((standardWidth,standardHeight))) #Metropolitan
}




#Checking NHL status to see if there are any games on
url = "https://api.sportsdata.io/v3/nhl/scores/json/AreAnyGamesInProgress?key="+api_key 
isGameOnRequest = requests.get(url)
isGameOn = isGameOnRequest.json()

#The games that are on today
todaysDate = datetime.date.today().strftime('%Y-%m-%d')
urlGamesToday = "https://api.sportsdata.io/v3/nhl/scores/json/GamesByDate/" + todaysDate + "?key=" + api_key
todaysGamesRequest = requests.get(urlGamesToday)
todaysGames = todaysGamesRequest.json()

#All players and their stats
currentYear = datetime.date.today().strftime('%Y')
urlPlayerStats = "https://api.sportsdata.io/v3/nhl/stats/json/PlayerSeasonStats/" + currentYear + "?key=" + api_key
playerStatsRequest = requests.get(urlPlayerStats)
playerStats = playerStatsRequest.json()


#Function that will get the list of games for today (and basic details) and assign it to a label to later be drawn
def getTodaysGames():
    allGameDetails = []
    for game in todaysGames:
        strScore = str(game['GameID']) + "\n" + game['HomeTeam'] + " - " + str(game['HomeTeamScore']) + "\n" + game['AwayTeam'] + " - " + str(game['AwayTeamScore']) + "\n" + game['Status']
        gameScore = strScore
        #Changed the gamescore from just the string, to include the 2 logos
        allGameDetails.append((teamLogos[game['HomeTeam']],gameScore, teamLogos[game['AwayTeam']]))
        print(strScore)
    return allGameDetails


#Function that will get all players and their stats and place them into a list of player objects
def getAllPlayers():
    allPlayers = []
    for player in playerStats:
        playerName = player['Name']
        playerTeam = player['Team']
        playerGamesPlayed = player['Games']
        playerPosition = player['Position']

        skaterGoals = player['Goals']
        skaterAssists = player['Assists']
        skaterPlusMinus = player['PlusMinus']
        goalieWins = player['GoaltendingWins']
        goalieLosses = player['GoaltendingLosses']
        goalieShutouts = player['GoaltendingShutouts']
        
        newPlayer = Player(playerName, playerTeam, playerGamesPlayed, playerPosition, skaterGoals, skaterAssists, skaterPlusMinus, goalieWins, goalieLosses, goalieShutouts)
        allPlayers.append(newPlayer)
        print(str(newPlayer.getName()))

    return allPlayers



#Function that will display a message if there are games on, based on the isGameOn info pulled via api
##Try to add the ability to draw each team's logo on either side of this label by implementing a hash table
def displayIfGamesOn():
    global isGameOn
    if(isGameOn == True):
        lblAreGamesOn = Label(root, text="There is hockey on tonight")
    else:
        lblAreGamesOn = Label(root, text="No hockey games on.")
    lblAreGamesOn.grid(row=0,column=3)

print(todaysDate)



#Division ranking sorting function (swap sort)
def rankSort(currentDivision):
    tempDiv = currentDivision.copy()
    tempX = 0
    tempI = 0
     
    for x in range(currentDivision.__len__()):
        i = x+1
        while i < currentDivision.__len__():
            if int(currentDivision[x][0]) > int(currentDivision[i][0]):
                tempX = currentDivision[x]
                tempI = currentDivision[i]
                tempDiv[x] = tempI
                tempDiv[i] = tempX
                currentDivision = tempDiv.copy()
            i = i + 1

        currentDivision = tempDiv

    currentDivision = tempDiv
    return currentDivision

#Function that will display the league standings in a new window once the button is clicked on the main window 
def goToLeagueStandings():
    leagueWindow = Toplevel()
    leagueWindow.title("NHL League Standings")
    leagueWindow.iconbitmap('pics/nhlLogos/puck.ico')
    lblLeagueStandings = Label(leagueWindow, text="Season Standings")
    atl = []
    met = []
    cen = []
    pac = []

    seasonYear = str(datetime.datetime.now().year)
    urlStandings = "https://api.sportsdata.io/v3/nhl/scores/json/Standings/" + seasonYear + "?key=46210c73e0464fd580a04f88e2f5d95a"
    leagueStandings = requests.get(urlStandings).json()
    print(leagueStandings)
    allLeagueDetails = []
    for s in leagueStandings:
        #print(s['Season'])
        print(s['City'])
        print(s['Division'])
        print(s['DivisionRank'])
        if(s['Division'] == 'Atlantic'):
            atl.append(str(s['DivisionRank']) + '. ' + s['City'] + '\n')
        elif(s['Division'] == 'Metropolitan'):
            met.append(str(s['DivisionRank']) + '. ' + s['City'] + '\n')
        elif(s['Division'] == 'Central'):
            cen.append(str(s['DivisionRank']) + '. ' + s['City'] + '\n')
        else:
            pac.append(str(s['DivisionRank']) + '. ' + s['City'] + '\n')

    #Sort the rankings of each division
    atl = rankSort(atl)
    met = rankSort(met)
    cen = rankSort(cen)
    pac = rankSort(pac)

    lblAtlanticStandings = Label(leagueWindow, text= "Atlantic Standings\n" + "".join(map(str,atl)))
    lblMetropolitanStandings = Label(leagueWindow, text="Metropolitan Standings\n"+ "".join(map(str,met)))
    lblCentralStandings = Label(leagueWindow, text="Central Standings\n" + "".join(map(str,cen)))
    lblPacificStandings = Label(leagueWindow, text="Pacific Standings\n" + "".join(map(str,pac)))
    
    lblAtlanticStandings.pack()
    lblMetropolitanStandings.pack()
    lblCentralStandings.pack()
    lblPacificStandings.pack()


#function to allow user to search for a player and get their stats from entire list
def findPlayer(personToFind, listOfPlayers, currentWindow, lblPlayerStats):
    global searchResult
    global inputSearch
    global resultsDrop
    selected = StringVar()

    resultsDrop.pack_forget()

    foundPlayer = False
    for x in listOfPlayers:
        if(personToFind == x.getName()):
            searchResult = x
            foundPlayer = True
            break
    
    if(foundPlayer == False):
        #A dropdown box with possible different choices of players user could have been searching for.
        resultsDrop['menu'].delete(0,'end')
        possibleResults = []
        for x in listOfPlayers: 
            if(personToFind in x.getName()):
                possibleResults.append(x.getName())
                resultsDrop['menu'].add_command(label=x.getName(), command=tkinter._setit(selected,x.getName()))
        if(len(possibleResults) == 0 or personToFind==''):
            searchResult =  "Player could not be found, please try searching again"
            lblPlayerStats.config(text=searchResult)
            lblPlayerStats.pack()
        else:
            lblPlayerStats.config(text="Player could not be found. Check the dropdown box for possible suggestions")
            lblPlayerStats.pack()
            resultsDrop.pack()
            inputSearch.config(textvariable=selected)

    elif(foundPlayer == True):
        if(searchResult.getPosition() != "G"):
            lblPlayerStats.config(text = "Stats:\n" 
            + "Player: " + str(searchResult.getName()) + "\n"
            + "Team: " +str(searchResult.getTeam()) + "\n"
            + "Position: " + str(searchResult.getPosition()) + "\n"
            + "Goals: " + str(searchResult.getGoals()) + "\n"
            + "Assists: " + str(searchResult.getAssists()) + "\n"
            + "PlusMinus: " + str(searchResult.getPlusMinus()) + "\n")
        else:
            lblPlayerStats.config(text="Stats:\n" 
            + "Player: " + str(searchResult.getName()) + "\n"
            + "Team: " +str(searchResult.getTeam()) + "\n"
            + "Position: " + str(searchResult.getPosition()) + "\n"
            + "Wins: " + str(searchResult.getGoalieWins()) + "\n"
            + "Losses: " + str(searchResult.getGoalieLosses()) + "\n"
            + "Shutouts: " + str(searchResult.getGoalieShutouts()) + "\n")
        lblPlayerStats.pack()


#Function that will allow user to search and display player stats in a new window once the button is clicked on the main window 
def goToPlayerStats():
    global searchResult
    global lblPlayerStats
    global inputSearch
    global resultsDrop

    searchResult = ''
    allActivePlayers = getAllPlayers() #Retrieve all players in a list format
    playerWindow = Toplevel()
    playerWindow.title("Player Statistics")
    playerWindow.iconbitmap('pics/nhlLogos/puck.ico')
    lblPlayerStats = Label(playerWindow, text="Stats:" + searchResult)
    inputSearch = Entry(playerWindow, width=100, bg="lightblue")
    selected = StringVar()
    resultsDrop = OptionMenu(playerWindow, selected, None)
    btnSearch = Button(playerWindow, text = 'Player Search', pady=30, command=lambda:findPlayer(inputSearch.get(), allActivePlayers, playerWindow,lblPlayerStats))
    inputSearch.pack()
    btnSearch.pack()

#The title on the app's main page
titleFrame = LabelFrame(root, padx=15,pady=15)
screenTitle = Label(titleFrame, text="NHL Stats App", font=("courier",44), anchor=NW) #,width=20, height= 5)



##
##DRAWING
##
##drawing the gui items on screen
currentColumn = 0
currentRow = 0
titleFrame.grid(row = currentRow, column= currentColumn, columnspan=3)
screenTitle.grid(row = 0, column= 0)



#Draw the scores of all the games on today
currentColumn = 0
currentRow = 1
displayIfGamesOn()
todaysGames = getTodaysGames()
for curGame in todaysGames:
    gameFrame = LabelFrame(root)
    gameFrame.grid(row=currentRow,column=currentColumn)
    lblHome = Label(gameFrame, image=curGame[0])
    lblHome.grid(row = 0, column= 0)
    lblScore = Label(gameFrame, text=curGame[1])
    lblScore.grid(row = 0, column= 1)
    lblAway = Label(gameFrame, image=curGame[2])
    lblAway.grid(row = 0, column= 2)

    currentRow+=1
    if(currentRow >= 5):
        currentRow = 1
        currentColumn += 1



currentRow+=4
btnLeagueStandings = Button(root, text = "See League Standings", pady=25, command=lambda:goToLeagueStandings())
btnLeagueStandings.grid(row = currentRow, column=0)

btnPlayerStats = Button(root, text = "Player Stats", pady=25, command=lambda:goToPlayerStats())
btnPlayerStats.grid(row = currentRow, column=1)

root.mainloop()
