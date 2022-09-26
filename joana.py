#!/usr/bin/env python3
# coding: utf-8

"""
Created on September 13, 2022
@author: BalthMhs
@society: BossaMuffinConnected
"""

# MVC 
from controller import Controller
from model import Model
from view import TkView

if __name__ == "__main__":
    # # SCRAPPING JOANA&VOUS 
    joana_patch = Controller(Model(), TkView())
    joana_patch.start()
