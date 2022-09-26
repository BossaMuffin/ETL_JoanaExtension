"""
Created on June 28, 2022
@author: BalthMhs
@society: BossaMuffinConnected
"""
URL_LOGIN = 'https://api.joanaetvous.com/auth/jwt/create/'
URL_API = 'https://api.joanaetvous.com/'
URL_APP = 'https://app.joanaetvous.com/'
WEEK_DAYS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi","dimanche")
OPTIONS = {
    'show_menu' : "La liste des recettes de la semaine, par jour",
    'change_portions' : "Modifier les portions par repas",
    'list_ingredients' : "Afficher les ingredients",
    'download_menu' : "Télécharger le menu",
    'export_ingredients' : "Exporter la liste d'ingrédients",
    'force_scrap' : "Force to scrap /!\\", 
    'quit_app' : "Quitter",
    }
SCRAPPED_FOLDER = "scrapped"
WEEK_FILE_PREFIXE = SCRAPPED_FOLDER + "/joanna_scrap_"