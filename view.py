'''
Created on June 18, 2022
@author: BalthMhs
@society: BossaMuffinConnected
'''
import tkinter as tk
from tkinter import ttk
import lorem
import lib_display as ds

class TkView(tk.Tk):
    '''
    Classdocs
    '''
    def __init__(self):
        super().__init__()
        
    def setup(self, p_controller):
        self.controller  = p_controller
        self.g_WEEK_DAYS = self.controller.getListWeekDays()
        #Set the global parameters
        self.LOREM = lorem.get_word(count=100)
        self.BG_CLR = 'white'
        self.BG_CLR_1 = "#41B77F"
        self.BG_CLR_2 = "#f2f2f2"
        self.TXT_CLR = 'white'
        self.GTRY = '1080x'+str(self.winfo_screenheight())
        self.MIN_WIDTH = 720
        self.MIN_HEIGHT = 720
        self.WIDTH_BTN = 20
        self.IPADY_CONTENT = 20
        self.WIDTH_CONTENT_AREA=self.MIN_WIDTH
        self.LOGO_ICO = 'logo.ico'
        self.BORDER = 1
        #Init local attributes
        self.btn_choosing_day = {}
        self.btn_choosing_day_in_app = {}
        self.frame_by_day = {}
        self.label_by_day = {}
        # Make the window and the frames
        self._initView()
        self._makeMainWidgets()
        self._makeMainEntries()
        # Show first visible widgets
        self.showNavButtons()
        self._showContent()
        self.showContentMessage()

    def startMainLoop(self):
        self.mainloop()
        
    def _initView(self):
        #Create the main window
        self.title("Joana's patch")
        self.geometry(self.GTRY)
        #self.iconbitmap("img/icon_checked.ico")
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.config(background=self.BG_CLR)
        self.resizable(width=True, height=True)
        #self.attributes('-fullscreen', True) 
        self.frame_title = tk.Frame(self, 
                                bg="blue", 
                                width=self.MIN_WIDTH, 
                                height=self.MIN_HEIGHT)
        self.label_title = tk.Label(self.frame_title, 
                                text='MENU DE LA SEMAINE', 
                                bg=self.BG_CLR_1, 
                                fg=self.TXT_CLR)
        self.label_subtitle = tk.Label(self.frame_title, 
                                   text='Hello my Jude', 
                                   bg=self.BG_CLR_1, 
                                   fg=self.TXT_CLR)
        self.frame_title.pack(fill='x')
        self.label_title.pack(fill='x')
        self.label_subtitle.pack(fill='x')

    def _makeMainWidgets(self):
        self._makeMainButtons()
        self._makeDaysButtons()
        self._makeContentWidgets()
        self._makePortionsAppWidgets()
        self._makeDaysFrames()
    
    def _makeMainEntries(self):
        pass

    def _makeContentWidgets(self):
        self.frame_content = tk.Frame(self,
                                       width=self.WIDTH_CONTENT_AREA,
                                       bg=self.BG_CLR_2)
        self.var_message_to_show = tk.StringVar()
        #e_bourrage = self.LOREM
        e_bourrage = ''
        self.var_message_to_show.set("Coucou Jude \n Qu'est-ce qu'on mange ? \n Tu vas pouvoir personnaliser ton menu de la semaine à partir des propositions de Joana. \n"+e_bourrage)
        self.message_content = tk.Message(self.frame_content, 
                                      text="Text par défaut", 
                                      textvariable=self.var_message_to_show, 
                                      width=self.WIDTH_CONTENT_AREA, 
                                      justify="left")
        
    def _makeMainButtons(self):
        self.frame_buttons = tk.Frame(self, bg=self.BG_CLR_1)
        self.frame_buttons.pack(side="left", fill='y', padx= 30, ipadx=10, ipady=20)
        self.btn_opt_menu = tk.Button(self.frame_buttons, 
                                  text="Qu'est-ce qu'on mange ?", 
                                  command=self.controller.showWeekMenu, 
                                  width=self.WIDTH_BTN)
        self.btn_opt_portionsApp = tk.Button(self.frame_buttons, 
                                      text="Changer les portions", 
                                      command=self.controller.showPortionsApp, 
                                      width=self.WIDTH_BTN)
        self.btn_opt_ingredients = tk.Button(self.frame_buttons, 
                                         text="Voir les ingrédients", 
                                         command=self.controller.showIngredientsList, 
                                         width=self.WIDTH_BTN)
        self.btn_opt_exportIngredients = tk.Button(self.frame_buttons, 
                                         text="Exporter les ingrédients", 
                                         command=self.controller.exportIngredientsInFile, 
                                         width=self.WIDTH_BTN)
        self.label_space = tk.Label(self.frame_buttons, 
                                     bg=self.BG_CLR_1, 
                                     text='')

    def _makeDaysButtons(self):
        for l0_i, l0_day in enumerate(self.g_WEEK_DAYS) :
            self.btn_choosing_day[l0_i] = tk.Button(self.frame_buttons, 
                                                     text=l0_day, 
                                                     width=self.WIDTH_BTN,
                                                     command=lambda day_id=l0_i : self.controller.chooseDayToShow(p_day_id=day_id, p_current_view='menu'))
            
            self.btn_choosing_day_in_app[l0_i] = tk.Button(self.frame_buttons,
                                                            text=l0_day, 
                                                            width=self.WIDTH_BTN,
                                                            command=lambda day_id=l0_i : self.controller.chooseDayToShowInApp(day_id))
    
    def _makePortionsAppWidgets(self):
        # these elements are not displayed at the begining
        self.btn_hide_portionsApp = tk.Button(self.frame_buttons, 
                                           text="Retour", 
                                           command=self.controller.hidePortionsApp, 
                                           width=self.WIDTH_BTN)

        self.frame_portionsApp = tk.Frame(self.frame_content, 
                                            bg=self.BG_CLR_2,  
                                            width=self.WIDTH_CONTENT_AREA)   
        #self.showPortionsScalesByDay(0)

    def _makeDaysFrames(self):
        e_temp_recettes = self.controller.getDictRecettes()
        for l0_i, l0_day in enumerate(self.g_WEEK_DAYS):
            self.frame_by_day[l0_i] = tk.Frame(self.frame_portionsApp, 
                                       width=self.WIDTH_CONTENT_AREA)
            self.label_by_day[l0_i] = tk.Label(self.frame_by_day[l0_i], 
                                       text=self.g_WEEK_DAYS[l0_i],
                                       width=self.WIDTH_CONTENT_AREA)
            self.label_by_day[l0_i].pack(pady=2)
            for l1_i, l1_day_meal in enumerate(e_temp_recettes[str(l0_i)].values()):
                e_var_current_btn_txt = tk.StringVar()
                ds.separator()
                e_frame_slider_by_meal = tk.Frame(self.frame_by_day[l0_i], 
                                                   width=self.WIDTH_CONTENT_AREA)
                e_btn_by_meal = tk.Button(e_frame_slider_by_meal, 
                                                       text="Valider",
                                                       textvariable=e_var_current_btn_txt)
                e_var_current_btn_txt.set("Valider")
                e_scale_by_meal = tk.Scale(e_frame_slider_by_meal, 
                                        orient='horizontal', 
                                        from_=0, to=3,
                                        resolution=1, 
                                        tickinterval=1, 
                                        length=self.WIDTH_CONTENT_AREA/2, 
                                        label=l1_day_meal['name'])  
                e_scale_by_meal.set(e_temp_recettes[str(l0_i)][str(l1_i+1)]["portions"])
                e_btn_by_meal['command'] = lambda day_id=l0_i, meal_id=l1_i, scale=e_scale_by_meal, btn_text=e_var_current_btn_txt: self.controller.updatePortion(day_id, meal_id, scale, btn_text)
                e_frame_slider_by_meal.pack(pady=2)
                e_scale_by_meal.pack()
                e_btn_by_meal.pack() 

    def _showEmptySpace(self):
        self.label_space.pack(fill='x', pady=2)
    
    def _hideEmptySpace(self):
        self.label_space.pack_forget()
    
    def showNavButtons(self):
        self.btn_opt_menu.pack(fill='x', pady=2)
        self.btn_opt_portionsApp.pack(fill='x', pady=2)
        self.btn_opt_ingredients.pack(fill='x', pady=2)
        self.btn_opt_exportIngredients.pack(fill='x', pady=2)
        
    def hideNavButtons(self):
        self.btn_opt_menu.pack_forget()
        self.btn_opt_portionsApp.pack_forget()
        self.btn_opt_ingredients.pack_forget()
        self.btn_opt_exportIngredients.pack_forget()
    
    def showDaysButtons(self):
        self._showEmptySpace()
        for l0_i in range(len(self.g_WEEK_DAYS)):
            self.btn_choosing_day[l0_i].pack(fill='x', pady=2)
    
    def hideDaysButtons(self):
        self._hideEmptySpace()
        for l0_i in range(len(self.g_WEEK_DAYS)):
            self.btn_choosing_day[l0_i].pack_forget()

    def showDaysButtonsInApp(self):
        self._showEmptySpace()
        for l0_i in range(len(self.g_WEEK_DAYS)):
            self.btn_choosing_day_in_app[l0_i].pack(fill='x', pady=2)
    
    def hideDaysButtonsInApp(self):
        self._hideEmptySpace()
        for l0_i in range(len(self.g_WEEK_DAYS)):
            self.btn_choosing_day_in_app[l0_i].pack_forget()
    
    def _showContent(self):
        self.frame_content.pack(side='left', fill='both')

    def showContentMessage(self):
        self.message_content.pack(fill='both', ipady=10, ipadx=50)
        
    def hideContentMessage(self):
        self.message_content.pack_forget()
    
    def showPortionsScalesByDay(self, p_asked_day):
        self.frame_by_day[p_asked_day].pack(pady=2)
        
    def hidePortionsScalesByDay(self):
        e_asked_day_in_app = self.controller.getAskedDayInPortionsApp()
        self.frame_by_day[e_asked_day_in_app].pack_forget()
