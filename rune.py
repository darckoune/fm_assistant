import sqlite3

class Rune:

    def __init__(self, id, listener):
        self.listener = listener

        connection = sqlite3.connect('database.sqlite')
        c = connection.cursor()

        result = c.execute('SELECT item.id, item.icon_id, description.description_text FROM item, description WHERE item.id=? AND item.description_id = description.id', [id]).fetchone()

        self.id = id
        self.name = result[2]

        c.execute('SELECT effect.id, effect_line.min, effect.weight, description.description_text FROM item_effect_line, effect_line, effect, description WHERE item_effect_line.item_id=? AND item_effect_line.effect_line_id=effect_line.id AND effect_line.effect_id=effect.id AND effect.description_id=description.id', [id])
        result = c.fetchone()

        self.effect_id = result[0]
        self.effect_value = result[1]
        self.effect_weight = result[2]
        self.description = result[3].replace("#1{~1~2 à }#2", str(self.effect_value))

        self.listener.updateRune(self)
        connection.close()

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getEffectId(self):
        return self.effect_id

    def getEffectValue(self):
        return self.effect_value

    def getEffectWeight(self):
        return self.effect_weight

    def getWeight(self):
        return int(self.effect_value*self.effect_weight)

    def getDescription(self):
        return self.description
