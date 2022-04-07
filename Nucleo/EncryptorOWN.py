#-*- encodin:utf-8 -*-
import math
import os
import errno
from shutil import rmtree
from pathlib import Path
from pathlib import PurePath
from datetime import datetime
from Nucleo.obtainInfo import *
from Nucleo.HTMLLogGenerator import *


class Encryptor:
    def __init__(self):
        pass

    def encryptFile(self, pathFile, finalPath, password, dir=None):
        textBin=self.readFile(pathFile)
        
        if len(textBin)%2==0:
            block_1=textBin[:int(len(textBin)/2)]
            block_2=textBin[int(len(textBin)/2):]

            block_1=self.permut(block_1, password, 'e')
            block_2=self.clasic(block_2, password)

            finalBlock=block_2+block_1

            pathSplit = PurePath(pathFile).parts #obtenemos la ruta en segmentos
            fileName=pathSplit[-1]+".enc" #obtenemos el último elemento en la ruta, que es el nombre del archivo, luego le concatenamos la extensión '.enc'.

            if not dir: #si el método no recibio un directorio entonces se esta encriptando un solo archivo
                directory = "OWN_Algorthm" 
                finalPath= os.path.join(finalPath,directory) #unimos la ruta 'destino' con la carpeta "AES_256" donde se tiene que guardar el archivo encriptado.
                if not os.path.exists(finalPath): #si la carpeta no existe en tal ruta
                    os.mkdir(finalPath) #se crea.
            else:
                pass

            newFilePath=os.path.join(finalPath,fileName) #creamos la ruta completa con el nombre del archivo.
                
            self.writeInFile(newFilePath, finalBlock)
        
        else:
            block_1=textBin[:int(len(textBin)/2)+1]
            block_2=textBin[int(len(textBin)/2)+1:]
            
            block_1=self.permut(block_1, password, 'e')
            block_2=self.clasic(block_2, password)

            finalBlock=block_2+block_1

            pathSplit = PurePath(pathFile).parts #obtenemos la ruta en segmentos
            fileName=pathSplit[-1]+".enc" #obtenemos el último elemento en la ruta, que es el nombre del archivo, luego le concatenamos la extensión '.enc'.

            if not dir: #si el método no recibio un directorio entonces se esta encriptando un solo archivo
                directory = "OWN_Algortms" 
                finalPath= os.path.join(finalPath,directory) #unimos la ruta 'destino' con la carpeta "AES_256" donde se tiene que guardar el archivo encriptado.
                if not os.path.exists(finalPath): #si la carpeta no existe en tal ruta
                    os.mkdir(finalPath) #se crea.
            else:
                pass

            newFilePath=os.path.join(finalPath,fileName) #creamos la ruta completa con el nombre del archivo.
                
            self.writeInFile(newFilePath, finalBlock)

    def decryptFile(self, path, finalPath, password, dir=None):
        textBin=self.readFile(path)
        
        block_1=textBin[:int(len(textBin)/2)]
        block_2=textBin[int(len(textBin)/2):]

        block_1=self.clasic(block_1, password)
        block_2=self.permut(block_2, password,'d')

        finalBlock=block_2+block_1

        pathSplit = PurePath(path).parts
        fileName=pathSplit[-1] #obtenemos el último elemento en la ruta, que es el nombre del archivo.
        fileName=fileName[:-4] #al nombre del archivo se le elimina la extensión .enc 
    
        if not dir:
            directory = "DES_OWN_Algorithm"
            finalPath=os.path.join(finalPath,directory) #unimos ruta 'destino' con la carpeta "DES_AES_256" donde se tiene que guardar el archivo en texto plano.
            if not os.path.exists(finalPath):
                os.mkdir(finalPath)
        else:
            pass

        newFilePath=os.path.join(finalPath,fileName)
        self.writeInFile(newFilePath, finalBlock)
 
    def permut(self, block, password, mode):
        
        newBlock=[]
        count=0
        if(mode == 'e'):
            for num in block:
                newBlock.append((num+ord(password[count%len(password)]))%256)
                count+=1
                
            t=self.permut(newBlock, password, 'e1')
            
            for i in range(len(t)):
                newBlock[i]=t[i]
            return bytes(newBlock)
        
        elif(mode == 'd'):
            for num in block:
                newBlock.append((num-ord(password[count%len(password)]))%256)
                count+=1

            t=self.permut(newBlock, password, 'd1')
            for i in range(len(t)):
                newBlock[i]=t[i]
            return bytes(newBlock)
            

        elif(mode == 'e1'):
            newBlock=[]
            for i in range(len(password)):
                try:
                    newBlock.append((block[i]+ord(password[i%len(password)]))%256)
                except IndexError as e:
                    pass

            return newBlock
                
        elif mode == 'd1':
            newBlock=[]
            for i in range(len(password)):
                try:
                    newBlock.append((block[i]-ord(password[i%len(password)]))%256)
                except IndexError as e:
                    pass
            return newBlock
    
    def clasic(self, block, password):
        array=[]
        for i in block:array.append(i)
        array=list(map(lambda x:-x+255, array))
        return bytes(list(map(lambda y, i: y^ord(password[i%len(password)]), array, [i for i in range(len(array))])))

    def readFile(self, path):
        f=open(path, 'rb')
        c=f.read()
        f.close()
        return c
    
    def writeInFile(self, path, content):
       
        f=open(path, 'wb')
        f.write(content)
        f.close()
        return True
    


"""
e=Encryptor()

e.encrypFile("karaoke-usted-al-estilo-de-luis-miguel.mp3", "1")
"""