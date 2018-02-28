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

    def isNegative(self, effect_id):
        for key, item in NEGATIVE_TO_POSITIVE.items():
            if effect_id == key:
                return True

NEGATIVE_TO_POSITIVE = {
116 : 117,   # - Portée
145 : 112,   # - Dommages
152 : 123,   # - Chance
153 : 125,   # - Vitalité
154 : 119,   # - Agilité
155 : 126,   # - Intelligence
156 : 124,   # - Sagesse
157 : 118,   # - Force
159 : 158,   # - Pods
162 : 160,   # - Esquive PA
163 : 161,   # - Esquive PM
168 : 111,   # - PA
169 : 128,   # - PM
171 : 115,   # - % Critique
175 : 174,   # - Initiative
177 : 176,   # - Prospection
179 : 178,   # - Soins
186 : 138,   # - Puissance
215 : 210,   # - % Résistance Terre
216 : 211,   # - % Résistance Eau
217 : 212,   # - % Résistance Air
218 : 213,   # - % Résistance Feu
219 : 214,   # - % Résistance Neutre
245 : 240,   # - Résistance Terre
246 : 241,   # - Résistance Eau
247 : 242,   # - Résistance Air
248 : 243,   # - Résistance Feu
249 : 244,   # - Résistance Neutre
411 : 410,   # - Retrait PA
413 : 412,   # - Retrait PM
415 : 414,   # - Dommages Poussée
417 : 416,   # - Résistance Poussée
419 : 418,   # - Dommages Critiques
421 : 420,   # - Résistance Critiques
423 : 422,   # - Dommages Terre
425 : 424,   # - Dommages Feu
427 : 426,   # - Dommages Eau
429 : 428,   # - Dommages Air
431 : 430,   # - Dommages Neutre
754 : 752,   # - Fuite
755 : 753,   # - Tacle
2801 : 2800, # - % Dommages mêlée
2802 : 2803, # - % Résistance mêlée
2805 : 2804, # - % Dommages distance
2806 : 2807, # - % Résistance distance
2809 : 2808, # - % Dommages d'armes
2813 : 2812  # - % Dommages aux sorts
}
