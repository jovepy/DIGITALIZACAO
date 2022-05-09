# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 14:19:38 2022

@author: Geral
"""

from digitalizacao_config import *


def inserir_primeiro_login(LOGIN, SENHA):
    try:
        
        comando = """
        INSERT INTO python.perfis_digitalizacao(login,senha)
        VALUES('{}','{}');
        """.format(LOGIN,SENHA)
        cur.execute(comando)  
        conn.commit()
    except:
        try:
            cur.execute("ROLLBACK")    
            cur.execute(comando)
            conn.commit() 
        except Exception as e:
            messagebox.showerror(title='Erro de conexão primária'.encode('latin-1'), message=e)
            cur.execute('ROLLBACK')
            
            
    
def confere_existencia_credencial(LOGIN):
    try:
        comando = """
        SELECT * FROM python.perfis_digitalizacao WHERE login='{}'
        """.format(LOGIN)
        cur.execute(comando)
        aux = cur.fetchall()
        conn.commit()
        if len(aux) != 0:
            return(True)
        else:
            return(False)
    except Exception as e:
        messagebox.showerror(title='Erro de retorno de conexão'.encode('latin-1'), message=e)
        cur.execute('ROLLBACK')
        

def autentica(LOGIN,SENHA):
    try:
        comando = """
        SELECT * FROM python.perfis_digitalizacao WHERE login='{}'
        """.format(LOGIN)
        cur.execute(comando)
        credenciais = cur.fetchall()
        conn.commit()
        if SENHA == credenciais[0][1]:
            return(True)
        else:
            return(False)
    except Exception as e:
        messagebox.showerror(title='Erro de autentificação'.encode('latin-1'), message=e)
        cur.execute('ROLLBACK')

def cria_diretorio_perfil(LOGIN):
    if LOGIN not in listdir(RAIZ+'/perfis'):
        mkdir(RAIZ+'/perfis/'+LOGIN)
        mkdir(RAIZ+'/perfis/'+LOGIN+'/Temp')
    diretorio_perfil = RAIZ+'/perfis/'+LOGIN
    copyfile('{}/MANUAL_USO_DIGITALIZACAO.pdf'.format(RAIZ), '{}/MANUAL_USO_DIGITALIZACAO.pdf'.format(diretorio_perfil))
    return(diretorio_perfil)