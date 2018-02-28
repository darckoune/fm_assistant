import binascii

class DofusPacket:
    def __init__(self, id, len, raw_data):
        self.id = id
        self.len = len
        self.raw_data = raw_data

    def parse(self):
        parsed = {}
        if self.id == 5516 or self.id == 5519:
            data_parsed = self.parse_ExchangeObjectMessage(self.raw_data)
            if self.isRune(data_parsed['objectGID']):
                object_type = 'rune'
            else:
                object_type = 'item'
            parsed['type'] = object_type
            parsed['data'] = data_parsed
        elif self.id == 6188:
            parsed['type'] = 'item_update'
            parsed['data'] = self.parse_ExchangeCraftResultWithObjectDescMessage(self.raw_data)
        return parsed

    def parse_ExchangeObjectMessage(self, raw_data):
        remaining = raw_data[1:]
        remaining, position = self.readIntFromBytes(remaining, 1)
        remaining, objectGID = self.readVarShort(remaining)
        remaining, numberOfEffects = self.readIntFromBytes(remaining, 2)
        effects = []
        for i in range (numberOfEffects):
            remaining, effectType = self.readIntFromBytes(remaining, 2  )
            if effectType == 70: #ObjectEffectInteger
                remaining, actionId = self.readVarShort(remaining)
                remaining, value = self.readVarShort(remaining)
                effects.append({
                    'actionId': actionId,
                    'value': value
                })
            elif effectType == 82: #ObjectEffectMinMax
                remaining, actionId = self.readVarShort(remaining)
                remaining, mini = self.readVarShort(remaining)
                remaining, maxi = self.readVarShort(remaining)
                effects.append({
                    'actionId': actionId,
                    'min': mini,
                    'max': maxi
                })
        remaining, objectUID = self.readVarInt(remaining)
        remaining, quantity = self.readVarInt(remaining)
        return ({
            'position': position,
            'objectGID': objectGID,
            'effects': effects,
            'objectUID': objectUID,
            'quantity': quantity
        })

    def parse_ExchangeCraftResultWithObjectDescMessage(self, raw_data):
        remaining, craftResult = self.readIntFromBytes(raw_data, 1)
        remaining, objectGID = self.readVarShort(remaining)
        remaining, numberOfEffects = self.readIntFromBytes(remaining, 2)
        effects = []
        for i in range (numberOfEffects):
            remaining, effectType = self.readIntFromBytes(remaining, 2)
            if effectType == 70: #ObjectEffectInteger
                remaining, actionId = self.readVarShort(remaining)
                remaining, value = self.readVarShort(remaining)
                effects.append({
                    'actionId': actionId,
                    'value': value
                })
            elif effectType == 82: #ObjectEffectMinMax
                remaining, actionId = self.readVarShort(remaining)
                remaining, mini = self.readVarShort(remaining)
                remaining, maxi = self.readVarShort(remaining)
                effects.append({
                    'actionId': actionId,
                    'min': mini,
                    'max': maxi
                })
        remaining, objectUID = self.readVarInt(remaining)
        remaining, quantity = self.readVarInt(remaining)
        remianing, magicPoolStatus = self.readIntFromBytes(remaining, 1)
        return ({
            'craftResult': craftResult,
            'objectGID': objectGID,
            'effects': effects,
            'objectUID': objectUID,
            'quantity': quantity,
            'magicPoolStatus': magicPoolStatus
        })

    #Variable readers

    def readVarShort(self, bytes_array):
        result = 0
        progress = 0
        current_byte = 0
        continuer = False
        while(progress < 16):
            current_byte = bytes_array[0]
            bytes_array = bytes_array[1:]
            continuer = (current_byte & 0b10000000) == 0b10000000
            if progress > 0:
                result = result + ((current_byte & 0b01111111) << progress)
            else:
                result = result + (current_byte & 0b01111111)
            progress += 7
            if not continuer:
                if(result > 32767):
                    result = result - 65536
                return (bytes_array, result)
        raise ValueError("Too much data")

    def readVarInt(self, bytes_array):
        result = 0
        progress = 0
        current_byte = 0
        continuer = False
        while(progress < 32):
            current_byte = bytes_array[0]
            bytes_array = bytes_array[1:]
            continuer = (current_byte & 0b10000000) == 0b10000000
            if progress > 0:
                result = result + ((current_byte & 0b01111111) << progress)
            else:
                result = result + (current_byte & 0b01111111)
            progress += 7
            if not continuer:
                return (bytes_array, result)
        raise ValueError("Too much data")

    def readIntFromBytes(self, bytes_array, size):
        return (bytes_array[size:], int.from_bytes(bytes_array[0:size], byteorder='big'))

    def isRune(self, objectGID):
        if objectGID in [1557, 7435, 7433, 7438, 1519, 1545, 1551, 1524, 1549, 1555, 1525, 1550, 1556, 1521, 1546, 1552, 1523, 1548, 1554, 1522, 1547, 1553, 1558, 7436, 10618, 10619, 7443, 7444, 7445, 11641, 11642, 11643, 11644, 7448, 7449, 7450, 7451, 10662, 7434, 7442, 7459, 7560, 7458, 7457, 7460, 7437, 7446, 10613, 7447, 10615, 10616, 7455, 7454, 7453, 7452, 7456, 11645, 11646, 11647, 11648, 11649, 11650, 11651, 11652, 11653, 11654, 11655, 11656, 11657, 11658, 11659, 11660, 11661, 11662, 11663, 11664, 11665, 11666, 11637, 11638, 11639, 11640, 10057, 18719, 18723, 18720, 18724, 18721, 18722]:
            return True
        else:
            return False

    def isInteresting(self):
        if self.id in [5516, 5519, 6188]:
            return True
        else:
            return False
