# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 08:06:40 2022

@author: Geral
"""


from os import chdir, listdir, startfile, mkdir, remove, rename, close
from shutil import copyfile
import pyautogui
from time import sleep, ctime
import tifffile
from itertools import combinations
import pytesseract
import PIL
import psycopg2
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import threading
from tkinter import   messagebox, Toplevel
from datetime import date
import psycopg2
import psutil

conn = psycopg2.connect(host='10.10.0.15', database='eunapio',user='cartorio', password='Cartorio.300@',port='7432')
cur = conn.cursor()
VERSAO = '2.2'
SCANNER = 'NAPS2'
CAMINHO_DB = 'M:/MATRICULAS' #provisório, efetico = M
SERVIDOR = 'M'
RAIZ='{}:/REGISTRE/ext/scripts/DIGITALIZACAO'.format(SERVIDOR)
chdir(RAIZ)

from digitalizacao_basico import *
from digitalizacao_credenciais import *


