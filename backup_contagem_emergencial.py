# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 16:48:53 2022

@author: rodrigo.jove
"""

    try:
        cur.execute("SELECT * FROM python.folhas_dia")
    except:
        cur.execute("ROLLBACK") 
        
    dados = cur.fetchall()

pd.DataFrame(dados).to_csv('backup_contagem/{}.csv'.format(date.today().strftime('%d-%m-%Y')))
