import json

data_effects = json.loads(open("Effects.json").read())
data_effects_weights = json.loads(open("effect_weights.json").read())
data_malus = {
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

output_data = []

for effect in data_effects:
    id = effect["id"]
    try:
        weight = data_effects_weights[str(id)]
    except:
        try:
            weight = -1*(data_effects_weights[str(data_malus[id])]/2)
        except:
            weight=0
    output_data.append({
        'id': id,
        'description_id': effect["descriptionId"],
        'weight': weight
    })
        
with open("output/effects.json", "w") as outfile:
    json.dump(output_data, outfile, indent=4)
    

output_data = []

data_items = json.loads(open("Items.json").read())

for item in data_items:
    possibleEffects = []
    for line in item["possibleEffects"]:
        if line["diceSide"] == 0:
            max = line["diceNum"]
        else:
            max = line["diceSide"]
        possibleEffects.append({
            'effectId': line["effectId"],
            'min': line["diceNum"],
            'max': max
        })
    output_data.append({
        'id': item["id"],
        'iconId': item["iconId"],
        'level': item["level"],
        'nameId': item["nameId"],
        'possibleEffects': possibleEffects
    })
    
    
with open("output/items.json", "w") as outfile:
    json.dump(output_data, outfile, indent=4)