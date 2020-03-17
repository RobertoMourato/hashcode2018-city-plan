from city import City
from building_proj import BuildingProj
from building import Building
from copy import deepcopy

class State:
    def __init__(self, city, buildings, map, score):
        self.city = city
        self.buildings = deepcopy(buildings)
        self.map = deepcopy(map)
        self.score = score
        # falta criar lista de lsitas com o mapa todo consoante os buildings
        
    # cria um novo estado e adiciona building ao mapa
    def nextState(self, buildingProj, mrow, mcol):
        newMap = deepcopy(self.map)
        #print("AWUDNBAWUIDBAWD")
        #print(self.buildings)
        newBuildings = deepcopy(self.buildings)
        newBuildings.append(Building(buildingProj, mrow, mcol))
        #print(self.buildings)

        for prow in range(buildingProj.rows):
            for pcol in range(buildingProj.cols):
                if buildingProj.plan[prow][pcol] == '#':
                    if newMap[mrow+prow][mcol+pcol] == '.':
                        newMap[mrow+prow][mcol+pcol] = len(self.buildings)+1
                    else:
                        return False
        newScore = self.calculateScore(self.city.walkDist, self.score, self.map, buildingProj, mrow, mcol, newBuildings)
        return State(self.city, newBuildings, newMap, newScore)

    def calculateScore(self, walkd, oldScore, map, buildingProj, mrow, mcol, buildings):
        visited = []
        services = []
        score = oldScore
        for prow in range(buildingProj.rows):
            for pcol in range(buildingProj.cols):
                if buildingProj.plan[prow][pcol] == '#':
                    for nrow in range(-walkd+mrow, walkd+1+mrow):
                        for ncol in range(-(walkd - abs(nrow) + mcol), walkd - abs(nrow) + 1 + mcol):
                            dist = self.calcManhattanDist(prow+mrow, pcol+mcol, nrow, ncol)
                            if map[nrow][ncol] != '.':
                                building_n = int(map[nrow][ncol])
                                if building_n not in visited:
                                    visited.append(building_n)
                                    foundBuilding = buildings[building_n-1]
                                    if foundBuilding.type == 'R' and buildingProj.type == 'U':
                                        if buildingProj.cenas not in foundBuilding.services:
                                            buildings[building_n-1].services.append(buildingProj.cenas)
                                            score += foundBuilding.cenas         
                                    elif foundBuilding.type == 'U' and buildingProj.type == 'R':
                                        if foundBuilding.cenas not in services:
                                            services.append(foundBuilding.cenas)
                                            score += buildingProj.cenas
        return score
                
    def calcManhattanDist(self, row1, col1, row2, col2):
        return ( abs(row2 - row1) + abs(col2 - col1) )
