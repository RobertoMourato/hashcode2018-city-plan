class Building:
    # locR e locC: row e col em que o building vai ser construido,
    def __init__(self, building_proj, mrow, mcol, building_id):
        self.projId = building_proj.id
        self.type = building_proj.type
        self.rows = building_proj.rows
        self.cols = building_proj.cols
        self.cenas = building_proj.cenas
        self.plan = building_proj.plan
        self.mrow = mrow
        self.mcol = mcol
        self.services = []
        self.score = None
        self.building_id = building_id

    def __eq__(self, other):
        if self.projId == other.projId and self.building_id == other.building_id:
            return True
        else:
             False