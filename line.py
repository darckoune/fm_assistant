import sqlite3

class Line:

    def __init__(self, effect_id, mini, maxi, value=0):
        connection = sqlite3.connect('database.sqlite')
        c = connection.cursor()
        result = c.execute('SELECT e.weight, d.description_text FROM effect e, description d WHERE e.id=? AND e.description_id = d.id', [effect_id]).fetchone()
        connection.close()
        self.effect_id = effect_id
        self.effect_weight = result[0]
        self.min = mini
        self.max = maxi
        self.description = result[1]
        self.value = value
        self.last_modification=0

    def getEffectId(self):
        return self.effect_id

    def getEffectWeight(self):
        return self.effect_weight

    def getWeight(self):
        return self.effect_weight*self.value

    def getMaxWeight(self):
        return self.effect_weight*self.max

    def getMin(self):
        return self.min

    def getMax(self):
        return self.max

    def getDescription(self):
        return self.description.replace("#1{~1~2 à }#2", str(self.value))

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.last_modification = value - self.value
        self.value = value

    def initValue(self, value):
        self.value = value

    def isOvermax(self):
        return self.value > self.max

    def getLastModification(self):
        return self.last_modification
