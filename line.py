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
        weight = self.effect_weight*self.value
        if weight == int(weight):
            return int(weight)
        else:
            return "%.1f" % weight

    def getMaxWeight(self):
        max_weight = self.effect_weight*self.max
        if max_weight == int(max_weight):
            return int(max_weight)
        else:
            return "%.1f" % max_weight

    def getMin(self):
        return self.min

    def getMax(self):
        return self.max

    def getDescription(self):
        return self.description.replace("#1{~1~2 à }#2", str(self.value))

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def isOvermax(self):
        return self.value > self.max
