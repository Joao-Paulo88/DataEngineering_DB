from pyspark.sql.functions import *
import os
import shutil 

def get_file(file_path):
    print("buscando arquivo mais recente...")
    
    dir = (f"{file_path}")
    aqvs = os.listdir(dir)

    lista_arquivos = []
    
    if len(aqvs) == 0:
        print("Não há arquivos no diretório selecionado")
        return
    else:
        for arquivo in aqvs:
            caminho = os.path.join(dir, arquivo)
            data_arquivos = os.path.getctime(f"{caminho}")
            lista_arquivos.append((data_arquivos, arquivo))
            
        lista_arquivos.sort(reverse= True)
        utlimo_arquivo = lista_arquivos[0]
        nome_arquivo = utlimo_arquivo[1]

        print(f"Arquivo mais recente encontrado")
        print(f"{nome_arquivo}")

        for arquivo in aqvs:
            return nome_arquivo
            
    
def list_files(file_path):
    print("listando arquivos...")
    
    dir = (f"{file_path}")
    aqvs = os.listdir(dir)

    lista_arquivos = []
    
    if len(aqvs) == 0:
        print("Não há arquivos no diretório selecionado")
        return
    else:
        for arquivo in aqvs:
            caminho = os.path.join(dir, arquivo)
            data_arquivos = os.path.getctime(f"{caminho}")
            lista_arquivos.append((data_arquivos, arquivo))
    

        for item in lista_arquivos:
            print(item)
        return lista_arquivos 
    
    
def mover_arquivos(origem, destino):
    print ("Movendo arquivos para a pasta de destino...")

    if not os.path.isdir(origem):
        raise Exception (f"Origem não existe ou não é um diretório: {origem}")
    
    if not os.path.exists(destino):
        print(f"Diretório de destino não existe. Criando...")
        os.makedirs(destino)
    
    arquivos = os.listdir(origem)
    
    if len(arquivos) == 0:
        print("Não há arquivos no diretório")
        return 0
    
    movidos = 0
    
    for arquivo in arquivos:
        
        caminho_origem = os.path.join(origem, arquivo)
        caminho_destino = os.path.join(destino, arquivo)
        
        if os.path.exists(caminho_destino):
            print(f"Arquivo já existe: {arquivo}")
            continue    
        
        if os.path.isfile(caminho_origem):
            try:
                shutil.move(caminho_origem, caminho_destino)
                print(f"Ok: {arquivo}")
                movidos += 1
            except Exception as e:
                print(f"Erro ao moover arquivo {arquivo} : {e} ")
                
    print(f"Total de arquivos movidos: {movidos}")
    return movidos