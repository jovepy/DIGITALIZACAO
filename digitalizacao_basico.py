# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 08:06:49 2022

@author: Geral
"""

from digitalizacao_config import *




def kill_process(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            proc.kill()

def cria_nome_matricula(n='matricula'):
    aux = '00000000'
    if len(str(n)) <8:        
        nome = str(aux[len(str(n))-8:])+str(n)
    else:
        nome = str(n)
    return(nome)


def pastas_inicias():
    aux = '00000000'
    n = 0
    for i in list(range(145)):
        nome = str(aux[len(str(n))-8:])+str(n)
        mkdir(CAMINHO_DB+'/{}'.format(nome))
        n+=1
        
def criador_pasta(pasta=str):
    if pasta not in listdir(CAMINHO_DB):
        mkdir(CAMINHO_DB+'/{}'.format(pasta))
        
def encontra_pasta(matricula=str):
    n= int(matricula)//1000
    aux = '00000000'
    pasta = str(aux[len(str(n))-8:])+str(n)
    criador_pasta(pasta=pasta)
    return(pasta)

def transforma_tiffa4(diretorio_perfil,ficha=str):
    ficha =diretorio_perfil+'/Temp/'+ficha
    arquivos = []
    with PIL.Image.open(ficha) as im:            
        largura,altura = im.size
        frames = im.n_frames
        if frames == 1:            
            im.save(diretorio_perfil+'/Temp/page1.tiff', dpi=(200,200))
            arquivos.append('page1.tiff')
            del(im)    
        else:
            for i, page in enumerate(PIL.ImageSequence.Iterator(im)):
                page.save(diretorio_perfil+'/Temp/page%d.tiff' % i, dpi=(200,200))
                arquivos.append('page%d.tiff' % i)
            del(page,im)

    df_aux = pd.DataFrame(arquivos)
    df_aux.index = df_aux.index %2
    df_aux['n'] = list(range(1,len(df_aux)+1))
    new_im = PIL.Image.new('L', (largura,altura*2),color='white')
    
    multitiff = []
    sleep(1)
    for i,arquivoo ,n in zip(df_aux.index,df_aux[0], df_aux['n']):
        if frames == 1:
            new_im.paste(PIL.Image.open(diretorio_perfil+'/Temp/'+arquivoo),(0,0))
            remove(diretorio_perfil+'/Temp/'+arquivoo)
            aux = new_im
            multitiff.append(aux)
        else:
            if len(df_aux)%2 != 0:
                if n != len(df_aux):
                    if i == 0:
                        new_im.paste(PIL.Image.open(diretorio_perfil+'/Temp/'+arquivoo),(0,0))
                        remove(diretorio_perfil+'/Temp/'+arquivoo)
                    else:
                        new_im.paste(PIL.Image.open(diretorio_perfil+'/Temp/'+arquivoo),(0,altura))
                        remove(diretorio_perfil+'/Temp/'+arquivoo)
                        aux = new_im
                        multitiff.append(aux)
                        new_im = PIL.Image.new('L', (largura,altura*2),color='white')
                        
                        
                else:
                    new_im.paste(PIL.Image.open(diretorio_perfil+'/Temp/'+arquivoo),(0,0))
                    remove(diretorio_perfil+'/Temp/'+arquivoo)
                    aux = new_im
                    multitiff.append(aux)
            else:
                if i == 0:
                    new_im.paste(PIL.Image.open(diretorio_perfil+'/Temp/'+arquivoo),(0,0))
                    remove(diretorio_perfil+'/Temp/'+arquivoo)
                else:
                    new_im.paste(PIL.Image.open(diretorio_perfil+'/Temp/'+arquivoo),(0,altura))
                    remove(diretorio_perfil+'/Temp/'+arquivoo)
                    aux = new_im
                    multitiff.append(aux)
                    new_im = PIL.Image.new('L', (largura,altura*2),color='white')
    remove(ficha)     
    multitiff[0].save(ficha, save_all=True, append_images=multitiff[1:],format='TIFF', dpi=(200,200)) 



def unir_tiffs(diretorio_perfil,matricula=str):
    
    nome_base = cria_nome_matricula(n=matricula)
    
    pasta = encontra_pasta(matricula=matricula)    
    caminho_base = CAMINHO_DB+'/{}/{}.tiff'.format(pasta,nome_base)
    
    
    for arquivo in listdir(diretorio_perfil+'/Temp/'):        
        
        im = tifffile.imread(diretorio_perfil+'/Temp/{}'.format(arquivo))
        
        tifffile.imwrite(caminho_base, im, append=True,photometric='minisblack',compress=6)
        del(im)
    startfile(CAMINHO_DB+'/{}/{}.tiff'.format(pasta,nome_base))
        
LIVROS_2 = []
LIVRO2 = list(combinations(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 2))
for i in LIVRO2:
    livro = '2'+i[0]+i[1]
    LIVROS_2.append(livro)
for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
    LIVROS_2.append('2'+i)

def ler_livro_folha(caminho=str):
    image = PIL.Image.open(caminho)
    l,h = image.size
    livro_folha = image.crop((1500, 110, 2500, 550)) #image.crop((1000, 55, 1620, 320))
    texto = pytesseract.image_to_string(livro_folha).replace('\n',' ').lower()
    livro = ''
    for i in texto.split(' '):
        if '2' in i:
            try:
                int(i)
            except:
                livro=i.upper().replace('0','O').replace('1','I')
                break
    if livro =='':
        for i in texto.split('livro:',1)[-1].split(' '):
            if '2' in i:
                try:
                    int(i)
                    if i == '20':
                        livro = '2O'
                    elif i == '21':
                        livro = '2I'
                except:
                    livro=i.upper().replace('0','O').replace('1','I')
                    break
    if livro == '':
        livro = texto.split('livro: ',1)[-1].split(' ',1)[0]
    
    
    folha = ''
    for i in texto.split(' '): #era espaco
        try:
            int(i)
            folha = i.upper()
            break
        except:
            pass
    if folha == '20' or folha == '21':
        folha = texto.split('folha: ',1)[-1].split(' ')[0]
    
    if len(livro) == 4: # VER ISSO EM FUNCIONAMENTO
        livro = livro[:-1]+'1'

    del(image)
    return(livro,folha)    
        

def inserir_nfolhas(usuario,numero=int):
    valores = [numero,date.today().strftime('%d/%m/%Y'),usuario]
    try:
        sql = ''
        
        for valor in valores: #INSERIR NA TABELA DAS GUIAS PARA ABASTECER SELO
            sql = sql+"'"+str(valor)+"',"
        
        cur.execute("insert into python.folhas_dia(numero,data, usuario) values ({})".format(sql[:-1]))
        conn.commit()
    except:
        try:
            cur.execute("ROLLBACK")
            cur.execute("insert into python.folhas_dia(numero,data, usuario) values ({})".format(sql[:-1]))
        except:
            pyautogui.alert(text='PROBLEMA NO BANCO DE DADOS - FOLHAS DIA',title='ERRO')
            

def ler_matricula_ficha(usuario,caminho=str):
    #caminho='J:/REGISTRE/EXT/Scripts/DIGITALIZACAO/perfis/rodrigo/Temp/temp.tiff'
    image = PIL.Image.open(caminho)
    inserir_nfolhas(usuario,numero=image.n_frames) #MODIIFICACAO 
    matricula = image.crop((200, 100, 1000, 468))#image.crop((0, 0, 450, 320))   para 200x200
    texto = pytesseract.image_to_string(matricula).replace('\n',' ').replace('.','').upper()
    matricula = ''
    for i in (texto.split(' ')):
        try:
            int(i)
            matricula = i            
            break
        except:
            pass
        
    if matricula == '' or len(matricula) <=1 or matricula == '11':
         matricula = image.crop((200, 100, 1000, 650))#image.crop((0, 0, 450, 320))   para 200x200            
         texto = pytesseract.image_to_string(matricula).replace('\n',' ').replace('.','').upper()
         matricula = ''
         for i in (texto.split(' ')):
             try:
                 int(i)
                 matricula = i
                 break
             except:
                 pass
             
    if matricula == '' or len(matricula) <=1 or matricula == '11':
        aux = PIL.ImageSequence.Iterator(image)
        for page in aux:
            matricula = image.crop((200, 150, 800,468 ))#image.crop((0, 0, 450, 320))   para 200x200            
            texto = pytesseract.image_to_string(matricula).replace('\n',' ').replace('.','').upper()
            matricula = ''
            for i in texto.split(' '):
                try:
                    int(i)
                    matricula = i
                    candidatos.append(matricula)
                except:
                    pass
            if matricula != '':
                break
        del(page)
        del(aux)
    
   
    if matricula == '' or len(matricula) <=1 or matricula == '11':
        aux = PIL.ImageSequence.Iterator(image)
        for page in aux:
            matricula = page.crop((200, 150, 800, 650))#image.crop((0, 0, 450, 320))   para 200x200            
            texto = pytesseract.image_to_string(matricula).replace('\n',' ').replace('.','').upper()
            matricula = ''
            for i in (texto.split(' ')):
                try:
                    int(i)
                    if i != '11' and i != '4' or matricula == '7' or matricula == '1':
                        matricula = i
                        break
                except:
                    pass
            if matricula != '':
                break
        del(page)
        del(aux)
    del(image)
    return(matricula)

valores = ['9999999999999','sn','sn']
def inserir_ficha_db(valores=list):
    try:
        sql = ''
        
        for valor in valores: #INSERIR NA TABELA DAS GUIAS PARA ABASTECER SELO
            sql = sql+"'"+str(valor)+"',"
        
        cur.execute("insert into python.fichas(matricula, livro, folha, usuario) values ({})".format(sql[:-1]))
        conn.commit()
    except:
        try:
            cur.execute("ROLLBACK")    
            cur.execute("insert into python.fichas(matricula, livro, folha, usuario) values ({})".format(sql[:-1]))
        except:
            pyautogui.alert(text='PROBLEMA NO BANCO DE DADOS - fichas',title='ERRO')
            
    
def consultar_ficha_duplicidade_db(matricula=str, cur=conn.cursor()):
    try:
        cur.execute("SELECT * FROM python.fichas WHERE matricula = '{}'".format(matricula))
    except:
        cur.execute("ROLLBACK") 
        cur.execute("SELECT * FROM python.fichas WHERE matricula = '{}'".format(matricula))
    dados = cur.fetchall()
    
    dados = pd.DataFrame(dados)[[0,1,2]].drop_duplicates()    
    if len(dados) >1:
        
        duplicada = True
    else:
        duplicada=False
    return(duplicada)

def inserir_produtividade_db(valores=list):
    try:
        sql = ''
        
        for valor in valores: #INSERIR NA TABELA DAS GUIAS PARA ABASTECER SELO
            sql = sql+"'"+str(valor)+"',"
        
        cur.execute("insert into python.produtividade_fichas(data, quantidade) values ({})".format(sql[:-1]))
        conn.commit()
    except:
        try:
            cur.execute("ROLLBACK")    
            cur.execute("insert into python.produtividade_fichas(data, quantidade) values ({})".format(sql[:-1]))
        except:
            pyautogui.alert(text='PROBLEMA NO BANCO DE DADOS - produtividade',title='ERRO')
          
def inserir_eficiencia(valores=list):
    try:
        sql = ''
        
        for valor in valores: #INSERIR NA TABELA DAS GUIAS PARA ABASTECER SELO
            sql = sql+"'"+str(valor)+"',"
        
        cur.execute("insert into python.eficiencia_ocr(data, status, categoria) values ({})".format(sql[:-1]))
        conn.commit()
    except:
        try:
            cur.execute("ROLLBACK")    
            cur.execute("insert into python.eficiencia_ocr(data, status, categoria) values ({})".format(sql[:-1]))
        except:
            pyautogui.alert(text='PROBLEMA NO BANCO DE DADOS - eficiencia ocr',title='ERRO')

    
          
def confirma_matricula(usuario,diretorio_perfil,arquivo=str):
    matricula = ler_matricula_ficha(usuario,caminho=diretorio_perfil+'/Temp/{}'.format(arquivo))
    matricula = str(matricula).replace(' ','')
    rename(diretorio_perfil+'/Temp/{}'.format(arquivo),diretorio_perfil+'/Temp/{}.tiff'.format(matricula))                                   
    confirmacao = pyautogui.confirm(text='Matricula: {}'.format(matricula), title='Conferência da matrícula', buttons=['Correto', 'Corrigir'])  
    
    if confirmacao == 'Correto':
        inserir_eficiencia(valores=[date.today().strftime("%d-%m-%Y"),'ok','mat'])
        
    else:
        while confirmacao != 'Correto':
            correcao_nome = pyautogui.prompt(text='Corrija o nome do arquivo.\n\nInsira a matrícula correta', title='ATENÇÃO!' , default='').upper()
            rename(diretorio_perfil+'/Temp/{}.tiff'.format(matricula),diretorio_perfil+'/Temp/{}.tiff'.format(correcao_nome))
            sleep(1)
            matricula = correcao_nome
            confirmacao = pyautogui.confirm(text='Matricula: {}'.format(matricula), title='Conferência da matrícula', buttons=['Correto', 'Corrigir'])
        inserir_eficiencia(valores=[date.today().strftime("%d-%m-%Y"),'fail','mat'])    
    return(matricula)
            
def confirma_livro_folha(livro=str,folha=str):
    confirmacao_lf = pyautogui.confirm(text='Os dados estão corretos?\nLivro: {}\nFolha: {}'.format(livro,folha), title='MUITA ATENÇÃO!', buttons=['Correto', 'Corrigir'])
    if confirmacao_lf == 'Correto':
        inserir_eficiencia(valores=[date.today().strftime("%d-%m-%Y"),'ok','lf'])
    else:
        while confirmacao_lf != 'Correto':
            livro = pyautogui.prompt(text='LIVRO', title='ATENÇÃO!' , default='').upper()
            folha = pyautogui.prompt(text='FOLHA', title='ATENÇÃO!' , default='').upper()
            confirmacao_lf = pyautogui.confirm(text='Os dados estão corretos?\nLivro: {}\nFolha: {}'.format(livro,folha), title='MUITA ATENÇÃO!', buttons=['Correto', 'Corrigir'])
        inserir_eficiencia(valores=[date.today().strftime("%d-%m-%Y"),'fail','lf'])
    return(livro,folha)

def principal(diretorio_perfil,arquivo=str,n=int,matricula=str,livro=str,folha=str):
    try:        
        if int(matricula) <= 47350: #se a matricula possuir livro e folha
            duplicada = consultar_ficha_duplicidade_db(matricula=matricula)
            if duplicada == True:
                pyautogui.alert(text='ENCERRE A MATRÍCULA E REIMPRIMA A FICHA',title='MATRÍCULA REPETIDA!')
                remove(diretorio_perfil+'/Temp/{}.tiff'.format(matricula))
                digi.destroy() #erro será o gatilho para não passar daqui caso a ficha esteja duplicada
                
            else:
                pass
        
                           
        pasta = encontra_pasta(matricula=matricula)
        
        unir_tiffs(diretorio_perfil,matricula=matricula)
        remove(diretorio_perfil+'/Temp/{}.tiff'.format(matricula)) #exclui, pois os tiff unidos nao modifica o temporario
        n+=1
        encerrar = pyautogui.confirm(text='digitalização n.º {} realizada.'.format(n), title='N.º DE DIGITALIZAÇÕES', buttons=['Continuar','Encerrar'])        
        
        
    except Exception as e:        
        encerrar = 'Encerrar'
        messagebox.showerror('Erro',e)
    
    
    
    return(encerrar,n)

def formacao_tiff_df(matricula=str):
    pasta = encontra_pasta(matricula=matricula)    
    bases = listdir(CAMINHO_DB+'/{}'.format(pasta))
    base = str(cria_nome_matricula(n=matricula))+'.tiff'
    if base in bases:
        remove(CAMINHO_DB+'/{}/{}'.format(pasta,base))
        while base in bases:
            bases = listdir(CAMINHO_DB+'/{}'.format(pasta))
            sleep(1)
    else:
        pass




            
        
