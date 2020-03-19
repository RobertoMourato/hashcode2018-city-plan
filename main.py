import sys
import time
from city import City
from building_proj import BuildingProj
from building import Building
from state import State
#USAGE: main input_file

def hill_climbing(initState, city, buildingProjs, map):
    state = initState
    state = state.nextState(buildingProjs[len(buildingProjs)-1], 0, 0)

    for nrow in range(len(map)):
        for ncol in range(len(map[nrow])):
            #print(ncol)
            #print(str(nrow) + ',' + str(ncol))
            for proj in buildingProjs:
                newState = state.nextState(proj, nrow, ncol)
                if newState != False and newState.score > state.score:
                    state = newState
                    #ncol += proj.cols
                    break

    return state



# returns city object. appends building projects to buildings
def parse_file(file_name):
    buildings = []
    bestUs = {}
    bestRindex = None
    i = 0
    bestR = None
    
    with open(file_name, 'r') as input_file:
        vars = input_file.readline().split()
        city = City(vars[0], vars[1], vars[2], vars[3])
        #print(vars[2])
        for line in input_file:
            i += 1
            plan = []
            vars = line.split()
            for nrow in range(int(vars[1])):
                row = input_file.readline()
                row = row.rstrip('\n')
                plan.append(row)
                building = BuildingProj(i, vars[0], vars[1], vars[2], vars[3], plan)
                if building.type == 'R':
                    if bestR == None:
                        bestR = building
                    elif building.ratio > bestR.ratio:
                        bestR = building
                elif building.type == 'U':
                    if building.cenas not in bestUs.keys():
                        bestUs[building.cenas] = building
                    elif building.rows * building.cols < bestUs[building.cenas].rows * bestUs[building.cenas].cols:
                        bestUs[building.cenas] = building
    input_file.close()
    return city, bestR, bestUs.values()

# main
start = time.time()

file_name = sys.argv[1]
city, bestR, bestUs = parse_file(file_name)
bestUs = list(bestUs)
bestUs.append(bestR)
buildingProjs = bestUs

initScore = 0
initMap = [['.' for col in range(city.cols)] for row in range(city.rows)]
initState = State(city, [], initMap, initScore)


finalState = hill_climbing(initState, city, buildingProjs, initMap)
print(finalState.score)
for rown in range(len(finalState.map)):
    print('\n', end='')
    for coln in range(len(finalState.map[0])):
        if finalState.map[rown][coln] == '.':
            print('......|', end='')
        else:
            print(finalState.buildings[int(finalState.map[rown][coln])-1].type, end='')
            print(str(finalState.buildings[int(finalState.map[rown][coln])-1].cenas).zfill(2), end='')
            print(",", end='')
            print(str(finalState.map[rown][coln]).zfill(2), end='')
            print('|', end='')

newBuildings = finalState.buildings
for n in range(len(newBuildings)):
    print(str(n))
    print(newBuildings[n].type)
    print(newBuildings[n].services)
    print('~~~~~~~~~~~~~~~~~~')
""" state = initState.nextState(buildingProjs[len(buildingProjs)-1], 0, 0)

nextBuilding = None

for building in buildingProjs:
    if building.id == 105:
        nextBuilding = building

state = state.nextState(nextBuilding, 2, 0)

print(state.score)
for rown in range(len(state.map)):
    print('\n', end='')
    for coln in range(len(state.map[0])):
        if state.map[rown][coln] == '.':
            print('....|', end='')
        else:
            print(state.buildings[int(state.map[rown][coln])-1].type, end='')
            print(str(state.buildings[int(state.map[rown][coln])-1].projId).zfill(3), end='')
            print('|', end='') """

end = time.time()
print(end - start)