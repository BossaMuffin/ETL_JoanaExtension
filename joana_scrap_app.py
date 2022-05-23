#!/usr/bin/env python
# coding: utf-8

# # SCRAPPING JOANA&VOUS 

from fake_useragent import UserAgent 
import requests
import json
import random
import lib_display as ds

url_login = 'https://api.joanaetvous.com/auth/jwt/create/'
url_api = 'https://api.joanaetvous.com/'
url_app = 'https://app.joanaetvous.com/'
email = 'your email'
password = 'your password'

week_days = [
    'lundi', 
    'mardi', 
    'mercredi', 
    'jeudi', 
    'vendredi', 
    'samedi',
    'dimanche',
]
week_datas = {}
week_datas = week_datas.fromkeys(week_days, 'np_matrix')

recettes= {}

# Add a header giving a random user agent
ua = UserAgent().random
headers = {'user-agent': ua}

# Log to Joann&vous
def login(mail, pwd):
    s = requests.Session()
    payload = {
        'email' : mail,
        'password' : pwd
    }
    with s.post(url_login, json = payload, headers=headers) as res:
        s.headers.update({'authorization': 'Bearer '+ json.loads(res.content)['access']})
        #print(res.content)
    return s

# Get json answer from Joana API
def get_json_answer(session, target, uuid=''):
    r = ''
    with session.get(url_api+target+uuid, headers=headers) as resp:
        r = resp.json()
        #resp.headers
        #print(type(resp))
    return r

# Connexion
current_session = login(email, password)

print('JOANA - SESSION CONNEXION :')
print('\n')
print('Login : ', email)
print('@     :', url_api)
print('\n')
print('Headers : ', current_session.headers)

menu_semaine = get_json_answer(current_session, 'meal-plan/')

# Get meta datas of the week
week_date_deb = menu_semaine['beginning_date'].split(':', 1)[0]
week_pdf = menu_semaine['pdf']
uuid_jours = [day['uuid'] for day in menu_semaine['weekdays']]

infos_week = [get_json_answer(current_session, 'weekday/', uuid) for uuid in uuid_jours]

# jours de 0 à 7 // meals de 1 à 3 // dish de 1 à ?
ds.printn(2)
print('###', week_date_deb, '###')
ds.printn(2)

recette_uuid = ''

for i, day in enumerate(week_days):
    print('\n\n\n------------\n', day, '\n------------')
    recettes[i] = {}
    k = 0
    for meals in infos_week[i]['meals'][1:]:
        ds.printn(1)
        print(meals['category']['name'])
        for temp, dish in enumerate(meals['meal']['dishes']):
            # Add to the recettes global list
            k+=1
            recettes[i][k] = {}
            recettes[i][k]['id'] = dish['dish']['uuid']
            recettes[i][k]['display'] = dish['dish']['display']
            recettes[i][k]['name'] = dish['dish']['name']
            recettes[i][k]['portions'] = dish['dish']['portions']
            recettes[i][k]['cooking_time'] = dish['dish']['cooking_time']
            recettes[i][k]['preparation_time'] = dish['dish']['preparation_time']
            
            recettes[i][k]['days'] = day
            recettes[i][k]['category'] = meals['category']['name']
            print('\n')
            print(k, ' : ', dish['dish']['name'], ' > add to the list (', recettes[i][k]['display'], ')')

            infos_dish = get_json_answer(current_session, 'dish/', recettes[i][k]['id'])
            recettes[i][k]['instructions'] = infos_dish['instructions']
            recettes[i][k]['ingredients'] = {}
            
            for j, ingredient in enumerate(infos_dish['ingredients']):
                recettes[i][k]['ingredients'][j] = {}
                recettes[i][k]['ingredients'][j]['name'] = ingredient['ingredient']['name']
                recettes[i][k]['ingredients'][j]['category'] = ingredient['ingredient']['category']
                recettes[i][k]['ingredients'][j]['quantity'] = ingredient['quantity']
                recettes[i][k]['ingredients'][j]['unit_of_measure'] = {}
                recettes[i][k]['ingredients'][j]['unit_of_measure'] = ingredient['unit_of_measure']
                temp_time = random.randrange(3)
                ds.countdown(temp_time, step=1, show=False, space=0)
                print('    > "', recettes[i][k]['ingredients'][j]['name'], '"')
            
# Format the exported datas
json_object = json.dumps(recettes, indent = 4)

#recettes["36939721-b559-4512-ad7e-2160f13acdd1"]
with open("joanna_scrap_" + week_date_deb + '.json', "w") as outfile:
    outfile.write(json_object)

# End of scrapping
