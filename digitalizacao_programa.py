# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 08:06:29 2022

@author: Geral
"""
from digitalizacao_config import *

def iniciar(diretorio_perfil,v): #programa pezinho
    global n

    startfile(SCANNER,'open')    
    encerrar = 'Continuar'
    aux_perfil = v.get()
    usuario = diretorio_perfil.split('/')[-1]
    n=1
    try:

        while encerrar != 'Encerrar':
            perfil = aux_perfil
            arquivos = listdir(diretorio_perfil+'/Temp')#(RAIZ+'/Temp')
            if len(arquivos) == 0:
                sleep(2)
            else:
                if '.tiff' not in str(arquivos):
                    arquivos = listdir(diretorio_perfil+'/Temp')
                else:
                    
                    for arquivo in arquivos:       
                        startfile(diretorio_perfil+'/Temp/{}'.format(arquivo))#(RAIZ+'/Temp/{}'.format(arquivo))
                        
                        confirmacao = messagebox.askyesno('Confirme','O arquivo esta no formato correto?')
                        
                        if  confirmacao  == True:                        
                            confirmacao_dados = False
                            while confirmacao_dados != True:                            
                                try:                                
                                    matricula = confirma_matricula(usuario,diretorio_perfil,arquivo=arquivo)
                                except Exception as e:
                                    permissao_aguarda = False
                                    while permissao_aguarda != True:
                                        try:
                                            matricula = confirma_matricula(usuario,diretorio_perfil,arquivo=arquivo)
                                            permissao_aguarda=True
                                        except:
                                            permissao_aguarda = False
                                            messagebox.showinfo(message=e,title='Erro')
                                        
                                if int(matricula) <= 47350:
                                    livro,folha = ler_livro_folha(caminho ='{}/temp/{}.tiff'.format(diretorio_perfil,matricula))
                                    livro, folha = confirma_livro_folha(livro=livro,folha=folha)
                                else:
                                    livro,folha = ('SN','SN')
                                
                                confirmacao_dados = messagebox.askyesno('MUITA ATENCAO!','Todos os dados estão corretos?\n\nMATRICULA: {}\n\nLIVRO: {}\n\n FOLHA: {}'.format(matricula,livro,folha))
                                arquivo = '{}.tiff'.format(matricula)
                                
                            
                            
                            inserir_ficha_db([matricula,livro,folha,usuario,date.today().strftime('%d/%m/%Y'),perfil]) #computa para sabermos se há duplicidade                            
                            
                            transforma_tiffa4(diretorio_perfil, ficha='{}.tiff'.format(matricula)) #antes arquivo quandoa4 era a 1 a formar
                            
                            if perfil == 'rotina':
                                pass                
                            else:
                                formacao_tiff_df(matricula=matricula) #se for diferente da rotina, como o usuario pegará as fichas, ele deve apagar todas as existentes                    
                            encerrar, n = principal(diretorio_perfil,arquivo='{}.tiff'.format(matricula),n=n,matricula=matricula,livro=livro,folha=folha)
                            del(matricula,livro,folha)
                        
                        else:
                            remove(diretorio_perfil+'/Temp/{}'.format(arquivo))
                            #kill_process('dllhost.exe')
                            messagebox.showwarning('ATENÇÃO'.encode('latin-1'),'Repita a digitalizacao, reescaneie a ficha'.encode('latin-1'))                         

                del(arquivo,arquivos)        
                   
    except Exception as e:
        messagebox.showerror(title='Erro',message=e)
        
    inserir_produtividade_db(valores=[date.today().strftime("%d-%m-%Y"),str(n)])
    digi.destroy()
    

        
def logar():
    """
    app: janela de credencial
    hofa: janela do menu principal
    LOGIN e SENHA: credenciais retornadas dos campos de entrada
    """
    global app
    global digi
    global LOGIN
    global SENHA
    global v
    global diretorio_perfil
    
    LOGIN= str(vlogin.get()).lower()
    SENHA= vsenha.get()

    existencia = confere_existencia_credencial(LOGIN)
    if existencia == False:
        inserir_primeiro_login(LOGIN,SENHA)
    
    autorizacao = autentica(LOGIN,SENHA)
    if autorizacao == True:
        diretorio_perfil = cria_diretorio_perfil(LOGIN)
        app.destroy()

        digi = Tk()
        digi.title('Setor de Digitalizacao - Versao {}'.format(VERSAO))
        digi.geometry("500x80")
        digi.iconbitmap(r'digi.ico')
        
        def abrir_manual():
            startfile(r'{}/MANUAL_USO_DIGITALIZACAO.pdf'.format(diretorio_perfil),'open')

        my_menu=Menu(digi)
        m1=Menu(my_menu,tearoff=0)
        m1.add_command(label="ABRIR MANUAL",command=abrir_manual)
        my_menu.add_cascade(label="MANUAL DO USUÁRIO",menu=m1)
        digi.config(menu=my_menu)
        
        v = StringVar(digi, "1")
       
        def chama_iniciar():
            iniciar(diretorio_perfil,v)
            
            

        Button(
            digi, height=2,
            text="Iniciar", 
            command=chama_iniciar
            ).pack(side=RIGHT, expand=True, fill=X, padx=5,pady=10)
        
         
        values = {"inicial" : "formacao_df",
                  "normal" : "rotina"}

        for (text, value) in values.items():
            Radiobutton(digi, text = text, variable = v,
                value = value).pack(side = TOP, ipady = 5)

        digi.mainloop()
    else:
        messagebox.showerror(title='Atenção',message='Senha incorreta')
        

        
app = Tk()
app.geometry('500x100')
app.title('Setor de Digitalizacao - Versao {}'.format(VERSAO))
app.iconbitmap(r'digi.ico')
vlogin=StringVar()
p_vlogin=Entry(app, textvariable=vlogin)
p_vlogin.pack(pady=5, padx=5, side=TOP, fill=X,expand=True)

vsenha=StringVar()
p_senha=Entry(app, textvariable=vsenha,show='*')
p_senha.pack(pady=5, padx=5, side=TOP, fill=X,expand=True)

entrar=Button(app, height=1, text='Entrar',command=logar)
entrar.pack(pady=5, padx=5, side=TOP, fill=X,expand=True)

app.mainloop()
