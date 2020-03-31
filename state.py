from city import City
from building_proj import BuildingProj
from building import Building
from copy import deepcopy
from utils import removeFromMap

class State:
    def __init__(self, city, buildings, map, score):
        self.city = city
        self.buildings = deepcopy(buildings)
        self.map = deepcopy(map)
        self.score = score
    # building project a ser construido na row 'mrow' e col 'mcol'
    def nextState(self, building_proj, mrow, mcol):
        new_map = deepcopy(self.map)
        new_buildings = deepcopy(self.buildings)
        building_id = len(self.buildings)+1
        new_buildings.append(Building(building_proj, mrow, mcol, building_id))

        for prow in range(building_proj.rows):
            for pcol in range(building_proj.cols):
                if building_proj.plan[prow][pcol] == '#':
                    if mrow + prow >= len(new_map) or mcol + pcol >= len(new_map[mrow + prow]):
                        return False
                    if new_map[mrow+prow][mcol+pcol] == '.':
                        new_map[mrow+prow][mcol+pcol] =  building_id
                    else:
                        return False
        new_score = self.calculateScore(self.city.walk_dist, self.score, self.map, building_proj, mrow, mcol, new_buildings)
        new_buildings[-1].score = new_score - self.score
        return State(self.city, new_buildings, new_map, new_score)

    # argumentos: walking distance, antigo score, mapa, buildingProject, row do mapa onde se vai construir
    #, col do mapa onde se vai construir, buildings e index com default a 1 (para dar a usar no replace building
    # isto pois quando se está a construir a solução inicial o building a que se está a calcular os score é sempre
    # o último mas no replace building não. é um index arbitrário, sendo que o index se mantém mesmo depois do building
    # ser substituido por outro)
    def calculateScore(self, walkd, old_score, map, building_proj, mrow, mcol, buildings, index=-1):
        visited = [] # edificios construidos já visitados 
        services = [] # servicos do edificio residencial que esta a ser construido ja encontrados
        score = old_score # score a somar
        self_building_id = buildings[index].building_id
        for prow in range(building_proj.rows): # por cada row do projeto do edificio a construir
            for pcol in range(building_proj.cols): # por cada col do projeto do edificio a construir
                if building_proj.plan[prow][pcol] == '#': # caso exista uma celula ocupada do plano
                    for nrow in range(-walkd + (mrow + prow), walkd + (mrow+prow)+1): # verificar casas dentro do raio walking distance
                        if nrow >= len(map) or nrow < 0: # ver boundaries do mapa
                            continue
                        for ncol in range(-walkd + abs(nrow-mrow-prow) + pcol+mcol, walkd - abs(nrow-mrow-prow) + pcol + mcol + 1): # verificar casas dentro do raio walking distance
                            if ncol >= len(map[nrow]) or ncol < 0 : # ver boundarie sdo mapa
                                continue
                            if map[nrow][ncol] != '.' and map[nrow][ncol] != self_building_id:
                                building_n = int(map[nrow][ncol]) # index+1 do building no array dos buildings ja construidos
                                if building_n not in visited:
                                    visited.append(building_n)
                                    found_building = buildings[building_n-1]
                                    if found_building.type == 'R' and building_proj.type == 'U':
                                        if building_proj.attribute not in found_building.services:
                                            found_building.services.append(building_proj.attribute) # append nos services do edificio encontrado o serviço que está ser construido
                                            score += found_building.attribute         
                                    elif found_building.type == 'U' and building_proj.type == 'R':
                                        if found_building.attribute not in buildings[index].services and found_building.attribute not in services:
                                            buildings[index].services.append(found_building.attribute) # append nos services do edificio a ser construido o servico encontrado
                                            score += building_proj.attribute
        return score

    def replaceBuilding(self, index, building_proj):
        building = self.buildings[index]
        # vai se tentar construir building no mesmo sitio que o outro estava
        mrow = building.mrow
        mcol = building.mcol

        new_map = removeFromMap(self.map, building)

        # check if new building can replace the one to be replaced
        for prow in range(building_proj.rows):
            for pcol in range(building_proj.cols):
                if building_proj.plan[prow][pcol] == '#':
                    if mrow + prow >= self.city.rows or mcol + pcol >=self.city.cols:
                        return False
                    if new_map[mrow+prow][mcol+pcol] == '.':
                        new_map[mrow+prow][mcol+pcol] = building.building_id
                    else:
                        return False
        # copiar buildings e substituir building a ser substituito pelo novo mas com o mesmo building_id
        new_buildings = deepcopy(self.buildings)
        new_buildings[index] = Building(building_proj, mrow, mcol, building.building_id)
        # calcular score usando a mesma cidade, tirando do score o contributo do edificio removido, etc etc e no fim 
        # parametro opcional para passar index do novo building na lista dos buildings
        new_score = self.calculateScore(self.city.walk_dist, self.score - building.score, new_map, building_proj, mrow, mcol, new_buildings, building.building_id-1)
        new_buildings[index].score = new_score - (self.score - building.score)

        return State(self.city, new_buildings, new_map, new_score)