#!/usr/bin/env python3
# coding: utf-8

'''
Created on June 18, 2022
@author: BalthMhs
@society: BossaMuffinConnected
'''
# constants available in the whole app
import global_constants as g_const
# MVC 
from model import Model
from view import TkView
# # #
import lib_display as ds
ds.printn()
from datetime import datetime
from time import strftime, sleep
import sys


class Controller:
    '''
    Classdocs
    '''
    
    def __init__(self, p_model, p_view):
        self.model = p_model
        self.view = p_view

    def start(self):
        print(">> Joana's patch is begining")
        print(">> Setup the window")
        self.view.setupWindow(self)
        print(">> Setup the first view")
        self.view.setupMainView(self)
        print(">> Start to loop")
        self.view.startMainLoop()
    
    def stopApp(self):
        self.view.destroy
        sys.exit(0)
    
    def getDictRecettes(self):
        return self.model.getDictRecettes()
    
    def updateDictRecettes(self, p_new_recettes):
        self.model.g_temp_recettes = p_new_recettes
    
    def _getAskedDay(self):
        return self.g_asked_day

    def _updateAskedDay(self, p_int_day):
        self.model.g_asked_day = p_int_day
    
    def getAskedDayInPortionsApp(self):
        return self.model.g_asked_day_in_app

    def _updateAskedDayInPortionsApp(self, p_int_day):
        self.model.g_asked_day_in_app = p_int_day
    
    def setRecettesDatas(self):
        print(">> Start the model")
        self.view.var_message_to_show.set("... Attendons, fais-toi un café et reviens dans quelques minutes ...")
        self.view.update()
        e_results = self.model.start()
        self.view.var_message_to_show.set(e_results['text'])
        if e_results['bool']:
            self.view.addScrapBtnToNavBar()
            self.view.hideStartButton()
            self.view.makeDaysFrames()
            self.view.showNavButtons()
            self.view.var_message_to_show.set(self.view.CONTENT_MESSAGE[1])
            e_week_dates = self.model.formatDatesToShowInStr()
            self.view.var_subtitle_to_show.set(e_week_dates)
        else:
            self.view.var_start_btn_txt.set("Réessayer")
        
    
    def showWeekMenu(self):
        self.view.showDaysButtons()
        e_text_result = self.model.showMealsByDay()
        self.view.var_message_to_show.set(e_text_result)
    
    def downloadJoanaPngMenu(self):
        self.view.var_message_to_show.set("Téléchargement en cours ...")
        self.view.update()
        e_text_result = self.model.downloadJoanaPngMenu()
        self.view.var_message_to_show.set(e_text_result)
    
    # App to change portions of meals
    def showPortionsApp(self):
        self.view.hideDaysButtons()
        self.view.hideNavButtons()
        self.view.hideContentMessage()
        self.view.btn_hide_portionsApp.pack(fill='x', pady=2) 
        self.view.showDaysButtonsInApp()
        self.view.showPortionsScalesByDay(self.model.g_asked_day_in_app)
        self.view.frame_portionsApp.pack(side='left', fill='y', ipady=10, ipadx=50)
    
    def showIngredientsList(self):
        self.view.hideDaysButtons()
        e_text_result = self.model.showIngredients()
        self.view.var_message_to_show.set(e_text_result)
        
    def exportIngredientsInFile(self):
        e_horaire = str(datetime.now())
        self.model.exportIngredientsInFile(e_horaire)
        e_text_result = f'Fichier bien enregistré :\n {self.model.getFilesPath("ingredients")} \n à {e_horaire} '
        self.view.var_message_to_show.set(e_text_result)
    
    def forceScrapping(self):
        self.view.var_message_to_show.set("...\nSoyons patients, car cela prendra environ 5 minutes. \nTu seras prévenue à la fin.\n...")
        self.view.update()
        e_text_result = self.model.forceScrapping()
        self.view.var_message_to_show.set(e_text_result)
            
    def chooseDayToShow(self, p_day_id, p_current_view='menu'):
        print(self.model.g_asked_day)
        self.model.g_asked_day = p_day_id
        print(self.model.g_asked_day)
        if p_current_view == 'menu':
            e_text_result = self.model.showMealsByDay()
            self.view.var_message_to_show.set(e_text_result)
            
    def chooseDayToShowInApp(self, p_day_id):
        self.view.hidePortionsScalesByDay()
        self.model.g_asked_day_in_app = p_day_id
        self.view.showPortionsScalesByDay(self.model.g_asked_day_in_app)
        
    def hidePortionsApp(self):
        self.view.frame_portionsApp.pack_forget()
        self.view.btn_hide_portionsApp.pack_forget()
        self.view.showNavButtons()
        self.view.hideDaysButtonsInApp()
        self.view.showContentMessage()
    
    def updatePortion(self, p_day_id, p_meal_id, p_meal_scale, p_var_btn_txt):    
        e_temp_recettes = self.getDictRecettes()
        p_meal_id += 1
        self.model.update1Portion(p_day_id, p_meal_id, p_meal_scale.get())
        e_new_text_btn = "Jude, c'est ok pour " + str(p_meal_scale.get())
        p_var_btn_txt.set(e_new_text_btn)
        print(">> ", e_temp_recettes[str(p_day_id)][str(p_meal_id)]['name'], " to ", str(p_meal_scale.get()))

