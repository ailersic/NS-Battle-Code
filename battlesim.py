import xml.etree.ElementTree as ET
import urllib3
import random

offensiveNationName = "Nandiguo"
defensiveNationName = "Vittauria"
strikeLimit = 12
numSidedDie = 12

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
user_agent = {'user-agent': 'Python script for simulating roleplay battles, written by the nations of Usimbi and Vittauria'}
http = urllib3.PoolManager(1, headers = user_agent)

class nation:
    economyBins = ((25, 50, 75), ("Basket Case", "Third world", "Second world", "First world"))
    armsBins = ((4000, 8000, 12000, 16000), ("Poor", "Adequate", "Strong", "Industrious", "Schwarzeneggian"))
    complianceBins = ((25, 50, 75), ("Rebellious", "Restless", "Disciplined", "Slavish"))
    defenceBins = ((1000, 2000, 3000, 4000), ("Paper Thin", "Militia", "Conscripts", "Professional", "Elite"))
    
    def sortIntoBin(self, value, thresholds):
        for i in range(len(thresholds)):
            if value <= thresholds[i]:
                return i
        
        return len(thresholds)
    
    def getAttributes(self):
        response = http.request('GET', 'www.nationstates.net/cgi-bin/api.cgi?nation=' + self.name + ';q=demonym+census;scale=1+13+16+42+46')
        XMLstr = response.data
        root = ET.fromstring(XMLstr)
        
        self.demonym =      root[0].text
        self.economy =      float(root[1][0][0].text)
        self.infotech =     float(root[1][1][0].text)
        self.arms =         float(root[1][2][0].text)
        self.compliance =   float(root[1][3][0].text)
        self.defence =      float(root[1][4][0].text)
    
    def sortAttributes(self):
        self.economyBin = self.sortIntoBin(self.economy, self.economyBins[0])
        print("Economy: " + self.economyBins[1][self.economyBin])

        self.armsBin = self.sortIntoBin(self.arms, self.armsBins[0])
        print("Arms: " + self.armsBins[1][self.armsBin])

        self.complianceBin = self.sortIntoBin(self.compliance, self.complianceBins[0])
        print("Compliance: " + self.complianceBins[1][self.complianceBin])

        self.defenceBin = self.sortIntoBin(self.defence, self.defenceBins[0])
        print("Defence: " + self.defenceBins[1][self.defenceBin])
    
    def calcStats(self):
        self.attackStat = self.armsBin + self.complianceBin
        print("Attack Value: " + str(self.attackStat))
        
        self.defenceStat = self.defenceBin + self.economyBin
        print("Defence Value: " + str(self.defenceStat))
    
    def __init__(self, name):
        self.name = name
        print(name + ":")
        
        self.getAttributes()
        self.sortAttributes()
        self.calcStats()
        print("")

if __name__ == "__main__":
    offensiveNation = nation(offensiveNationName)
    defensiveNation = nation(defensiveNationName)
    
    if offensiveNation.arms > defensiveNation.arms:
        print(offensiveNation.name + " is ridiculously overpowered compared to " + defensiveNation.name + ".")
    elif offensiveNation.arms < defensiveNation.arms:
        print(defensiveNation.name + " is ridiculously overpowered compared to " + offensiveNation.name + ".")
    else:
        print(offensiveNation.name + " and " + defensiveNation.name + " are evenly matched in weaponry.")
    
    if offensiveNation.defence > defensiveNation.defence:
        print(defensiveNation.name + " could not penetrade the defences of " + offensiveNation.name + " with a nuclear bomb.")
    elif offensiveNation.defence < defensiveNation.defence:
        print(offensiveNation.name + " could not penetrade the defences of " + defensiveNation.name + " with a nuclear bomb.")
    else:
        print("Everything depends on what you can throw at one another; the two nations are evenly matched in defence...")
    
    if offensiveNation.infotech > defensiveNation.infotech:
        print(offensiveNation.name + " has seen the big board in the " + defensiveNation.demonym + " War Room.")
    elif offensiveNation.infotech < defensiveNation.infotech:
        print(offensiveNation.name + " has set up a permanent cocktail bar for " + defensiveNation.demonym + " spies.")
    else:
        print("The spying game is evenly matched: be careful out there.")
    
    strikeCounter = 1
    print("")
    
    while offensiveNation.defenceStat > 0 and defensiveNation.defenceStat > 0 and strikeCounter <= strikeLimit:
        print("STRIKE " + str(strikeCounter))
        
        if strikeCounter % 2:
            attacker = offensiveNation
            defender = defensiveNation
        else:
            attacker = defensiveNation
            defender = offensiveNation
        
        attackRoll = random.randint(0, numSidedDie)
        defenceRoll = random.randint(0, numSidedDie)
        
        if attackRoll < attacker.attackStat:
            print("Successful " + attacker.demonym + " attack!")
            
            if defenceRoll < defender.defenceStat:
                print(defender.name + " holds strong against the enemy!")
            elif defenceRoll == defender.defenceStat:
                defender.defenceStat = defender.defenceStat - 1
                print(defender.name + " survived that, but barely...")
            else:
                defender.defenceStat = defender.defenceStat - 2
                print(defender.name + " is slowly falling under the onslaught.")
            
            print(defender.demonym + " Defence Value: " + str(defender.defenceStat))
        else:
            print("The best " + attacker.demonym + " rocket fizzled out on takeoff.")
            
        strikeCounter = strikeCounter + 1
        print("")
    
    if offensiveNation.defenceStat <= 0 or defensiveNation.defenceStat <= 0:
        if defensiveNation.defenceStat <= 0:
            winner = offensiveNation
            loser = defensiveNation
            print(loser.name + " has lost the battle and the war; " + winner.name + " is victorious!")
        elif offensiveNation.defenceStat <= 0:
            winner = defensiveNation
            loser = offensiveNation
            print(loser.name + " REALLY should not have started that war, seeing as they have to surrender...")
        
        if winner.economy > loser.economy:
            print(loser.name + " can be safely assumed to fall under the " + winner.demonym + " sphere of influence...")
        else:
            print("Reparations and tribute are in order, are they not, " + loser.name + "?")
    else:
        print("A draw! Looks like more diplomacy is needed...")
        if offensiveNation.economy > defensiveNation.economy:
            print("Perhaps " + offensiveNation.name + " would be willing to help out?")
        elif offensiveNation.economy < defensiveNation.economy:
            print("Perhaps " + defensiveNation.name + " would be willing to help out?")
        else:
            print("Looks like these two idiots will have to clean up their own messes.")
