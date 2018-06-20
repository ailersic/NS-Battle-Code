import xml.etree.ElementTree as ET
import urllib3
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
user_agent = {'user-agent': 'Python script for simulating roleplay battles, written by the nations of Usimbi and Vittauria'}
http = urllib3.PoolManager(1, headers = user_agent)

class nation:
    economyBins = ((33, 66), ("Third world", "Second world", "First world"))
    armsBins = ((7000, 14000), ("Poor", "Fair", "Industrious"))
    complianceBins = ((50, 75), ("Rebellious", "Moderate", "Slavish"))
    defenceBins = ((2000, 4000), ("Lazy", "Average", "Vigilant"))
    
    def sortIntoBin(self, value, thresholds):
        for i in range(len(thresholds)):
            if value <= thresholds[i]:
                return i
        
        return len(thresholds)
    
    def getAttributes(self):
        response = http.request('GET', 'www.nationstates.net/cgi-bin/api.cgi?nation=' + self.name + ';q=census;scale=1+13+16+42+46')
        XMLstr = response.data
        
        root = ET.fromstring(XMLstr)
        
        self.economy =      float(root[0][0][0].text)
        self.infotech =     float(root[0][1][0].text)
        self.arms =         float(root[0][2][0].text)
        self.compliance =   float(root[0][3][0].text)
        self.defence =      float(root[0][4][0].text)
    
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
        self.demonym = name + "ian"
        print(name + ":")
        
        self.getAttributes()
        self.sortAttributes()
        self.calcStats()
        print("")
    
    def __init__(self, name, demonym):
        self.name = name
        self.demonym = demonym
        print(name + ":")
        
        self.getAttributes()
        self.sortAttributes()
        self.calcStats()
        print("")

def greet(lang):
    if lang == "vi":
        print("Good day to you!")
    if lang == "ki":
        print("Ungimua!")
    if lang == "na":
        print("Nihao!")

if __name__ == "__main__":
    greet("vi")
    
    nation1 = nation("Vittauria", "Vittaurian")
    nation2 = nation("Nandiguo", "Nandiguese")
    
    if nation1.arms > nation2.arms:
        print(nation1.name + " is ridiculously overpowered compared to " + nation2.name + ".")
    elif nation1.arms < nation2.arms:
        print(nation2.name + " is ridiculously overpowered compared to " + nation1.name + ".")
    else:
        print(nation1.name + " and " + nation2.name + " are evenly matched in weaponry.")
    
    if nation1.defence > nation2.defence:
        print(nation2.name + " could not penetrade the defences of " + nation1.name + " with a nuclear bomb.")
    elif nation1.defence < nation2.defence:
        print(nation1.name + " could not penetrade the defences of " + nation2.name + " with a nuclear bomb.")
    else:
        print("Everything depends on what you can throw at one another; the two nations are evenly matched in defence...")
    
    if nation1.infotech > nation2.infotech:
        print(nation1.name + " has seen the big board in the " + nation2.demonym + " War Room.")
    elif nation1.infotech < nation2.infotech:
        print(nation1.name + " has set up a permanent cocktail bar for " + nation2.demonym + " spies.")
    else:
        print("The spying game is evenly matched: be careful out there.")
    
    strikeCounter = 1
    strikeLimit = 12
    print("")
    
    while nation1.defenceStat > 0 and nation2.defenceStat > 0 and strikeCounter <= strikeLimit:
        print("STRIKE " + str(strikeCounter))
        
        if strikeCounter % 2:
            attacker = nation1
            defender = nation2
        else:
            attacker = nation2
            defender = nation1
        
        attackRoll = random.randint(0,6)
        defenceRoll = random.randint(0,6)
        
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
            print("The best " + nation1.demonym + " rocket fizzled out on takeoff.")
            
        strikeCounter = strikeCounter + 1
        print("")
    
    if strikeCounter < strikeLimit:
        if nation2.defenceStat <= 0:
            winner = nation1
            loser = nation2
            print(loser.name + " has lost the battle and the war; " + winner.name + " is victorious!")
        elif nation1.defenceStat <= 0:
            winner = nation2
            loser = nation1
            print(loser.name + " REALLY should not have started that war, seeing as they have to surrender...")
        
        if winner.economy > loser.economy:
            print(loser.name + " can be safely assumed to fall under the " + winner.demonym + " sphere of influence...")
        else:
            print("Reparations and tribute are in order, are they not, " + loser.name + "?")
    else:
        print("A draw! Looks like more diplomacy is needed...")
        if nation1.economy > nation2.economy:
            print("Perhaps " + nation1.name + " would be willing to help out?")
        elif nation1.economy < nation2.economy:
            print("Perhaps " + nation2.name + " would be willing to help out?")
        else:
            print("Looks like these two idiots will have to clean up their own messes.")
