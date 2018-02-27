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
            if line[0] not in [983, 984]: #lignes d'item echangeable
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

    def getReliquat(self):
        return self.reliquat

    def initLinesUsingPacket(self, packet):
        packet_lines = packet['data']['effects']
        self.exotic_lines = []
        for line in packet_lines:
            try:
                if self.getLineByEffectId(line['actionId']) is not None:
                    self.getLineByEffectId(line['actionId']).initValue(int(line['value']))
                else:
                    self.exotic_lines.append(Line(line['actionId'], 0, 0, int(line['value'])))

            except Exception as e:
                print('e : ' + str(e))

        self.listener.updateItem(self)

    def executeFM(self, result_packet, rune):
        packet_lines = result_packet['data']['effects']
        for line in packet_lines:
            try:
                if self.getLineByEffectId(line['actionId']) is not None:
                    self.getLineByEffectId(line['actionId']).setValue(int(line['value']))
                else:
                    new_line = Line(line['actionId'], 0, 0)
                    new_line.setValue(line['value'])
                    self.exotic_lines.append(new_line)

            except Exception as e:
                print('e : ' + str(e))

        ids_in_packet = []
        for line in packet_lines:
            ids_in_packet.append(line['actionId'])

        for line in self.getLines():
            if line.getEffectId() not in ids_in_packet:
                line.setValue(0)

        result_type = self.getResultType(result_packet)
        if result_type == 'SC':
            theorical_earned_weight = rune.getWeight()
        elif result_type in ['SN', 'EN']:
            theorical_earned_weight = 0
        elif result_type == 'EC':
            theorical_earned_weight = -1 * rune.getWeight()

        real_earned_weight = 0
        for line in self.getLines():
            real_earned_weight += line.getLastModification()*line.getEffectWeight()

        print('Result : ' + result_type)
        print('Theorical earning : ' + str(theorical_earned_weight))
        print('Real earning :' + str(real_earned_weight))
        self.reliquat += -1*(real_earned_weight-theorical_earned_weight)

        #cas spécial de SC avec seulement une partie de la rune passee : c'est en fait un SN
        if result_type == 'SC' and real_earned_weight-theorical_earned_weight != 0:
            result_type = 'SN'
            self.reliquat -= rune.getWeight()

        self.listener.updateItem(self)
        return result_type

    def getResultType(self, result_packet):
        malus = False
        for line in self.getLines():
            if line.getLastModification() < 0:
                malus = True
        if result_packet['data']['craftResult'] == 2: #succes
            if malus:
                return 'SN'
            else:
                return 'SC'
        elif result_packet['data']['craftResult'] == 1:#echec
            if malus:
                return 'EC'
            else:
                if self.reliquat > 0:
                    return 'EC'
                else:
                    return 'EN'
