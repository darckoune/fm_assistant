import sqlite3
from line import Line

class Item:

    def __init__(self, id, listener):
        self.listener = listener

        connection = sqlite3.connect('database.sqlite')
        c = connection.cursor()

        result = c.execute('SELECT item.id, item.level, item.icon_id, description.description_text FROM item, description WHERE item.id=? AND item.description_id=description.id', [id]).fetchone()

        self.id = id
        self.level = result[1]
        self.name = result[3]

        self.original_lines = []
        lines = c.execute('SELECT e.id, el.min, el.max FROM item_effect_line iel, effect_line el, effect e WHERE iel.item_id=? AND iel.effect_line_id=el.id AND el.effect_id=e.id', [id]).fetchall()
        for line in lines:
            self.original_lines.append(Line(line[0], line[1], line[2]))

        self.exotic_lines = []

        self.reliquat = 0

        connection.close()

    def getId(self):
        return self.id

    def getLevel(self):
        return self.level

    def getName(self):
        return self.name

    def getLines(self):
        return (self.original_lines + self.exotic_lines)

    def getOriginalLines(self):
        return self.original_lines

    def getExoticLines(self):
        return self.exotic_lines

    def getLineByEffectId(self, effect_id):
        for line in self.getLines():
            if line.getEffectId() == effect_id:
                return line

    def getWeight(self):
        total = 0
        for line in self.getLines():
            total += line.getWeight
        return total

    def initLinesUsingPacket(self, packet):
        packet_lines = packet['data']['effects']
        self.exotic_lines = []
        for line in packet_lines:
            try:
                if self.getLineByEffectId(line['actionId']) is not None:
                    self.getLineByEffectId(line['actionId']).setValue(int(line['value']))
                else:
                    self.exotic_lines.append(Line(line['actionId'], 0, 0, int(line['value'])))

            except Exception as e:
                print('e : ' + str(e))

        self.listener.updateItem(self)
