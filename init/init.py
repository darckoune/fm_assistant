import sqlite3
import json

connection = sqlite3.connect('../database.sqlite')
c = connection.cursor()

#Supression des tables deja existantes
try:
    c.execute('DROP TABLE item')
    c.execute('DROP TABLE effect_line')
    c.execute('DROP TABLE item_effect_line')
    c.execute('DROP TABLE effect')
    c.execute('DROP TABLE description')
except:
    print ('No tables to drop')

#Creation des tables
c.execute('CREATE TABLE item (id INTEGER PRIMARY KEY ASC, description_id INTERGER, level INTEGER, icon_id INTEGER, FOREIGN KEY (description_id) REFERENCES description(id))')
c.execute('CREATE TABLE effect_line (id INTEGER PRIMARY KEY ASC, effect_id INTEGER, min INTEGER, max INTEGER, FOREIGN KEY (effect_id) REFERENCES effect(id))')
c.execute('CREATE TABLE item_effect_line (item_id INTEGER, effect_line_id INTEGER, FOREIGN KEY (item_id) REFERENCES item(id), FOREIGN KEY (effect_line_id) REFERENCES effect_line(id))')
c.execute('CREATE TABLE effect (id INTEGER PRIMARY KEY ASC, description_id INTEGER, weight INTEGER, FOREIGN KEY (description_id) REFERENCES description(id))')
c.execute('CREATE TABLE description (id INTEGER PRIMARY KEY ASC, description_text TEXT)')

connection.commit()

#Remplissage de la table description
data_description = json.loads(open("raw_data/i18n_fr.json", encoding="utf8").read())
descriptions = data_description["texts"]

command = 'INSERT INTO description VALUES (?,?)'
for (description_id, description_text) in descriptions.items():
    c.execute(command, [description_id, description_text])

connection.commit()

#Remplissage de la table effect
effects = json.loads(open("raw_data/output/effects.json", encoding="utf8").read())

command = 'INSERT INTO effect VALUES (?,?,?)'
for effect in effects:
    c.execute(command, [effect["id"], effect["description_id"], effect["weight"]])

connection.commit()

#Remplissage des items
items = json.loads(open("raw_data/output/items.json", encoding="utf8").read())

command_item = 'INSERT INTO item VALUES (?,?,?,?)'
command_effect_line = 'INSERT INTO effect_line (effect_id, min, max) VALUES (?,?,?)'
command_association = 'INSERT INTO item_effect_line VALUES (?,?)'

for item in items:
    c.execute(command_item, [item["id"], item["nameId"], item["level"], item["iconId"]])
    for effect_line in item["possibleEffects"]:
        c.execute(command_effect_line, [effect_line["effectId"], effect_line["min"], effect_line["max"]])
        c.execute(command_association, [item["id"],c.lastrowid])

#Supression des champs inutiles dans la table description

command_retrieve_item = 'SELECT * FROM item WHERE description_id=?'
command_retrieve_effect = 'SELECT * FROM effect WHERE description_id=?'
command_delete_description = 'DELETE FROM description WHERE id=?'

for (description_id, description_text) in descriptions.items():
    if c.execute(command_retrieve_item, [description_id]).fetchone() is None:
        if c.execute(command_retrieve_effect, [description_id]).fetchone() is None:
            c.execute(command_delete_description, [description_id])
    if int(description_id)%1000 == 0:
        print (description_id)

connection.commit()
