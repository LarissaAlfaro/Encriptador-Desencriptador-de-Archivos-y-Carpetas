#-*-coding:utf-8-*-
import os
import errno
from shutil import rmtree
from pathlib import Path
from pathlib import PurePath
from Nucleo.AES256 import AES256
from Nucleo.EncryptorOWN import *
from datetime import datetime
from Nucleo.obtainInfo import *
from Nucleo.HTMLLogGenerator import *


"""
*Nombre de la clase: encryptDecrypt
*Atributos: ----
*Descripción: Desde esta clase se recibe la ruta del archivo o directorio y se hace uso de la clase AES256 para encriptar o desencriptar. Si se encripta o desencripta un directorio esta clase se encarga de crear la estructura interna de este en la ruta destino.
"""

class encryptDecrypt:

    def __init__(self):
        self.enc=Encryptor() #instancia de clase para encriptación desarrollada por los alumnos
        self.AES = AES256() #instancia de clase para encriptación AES256
        self.info = obtainInfo() #instancia de clase que obtiene la informacion para generar el html log y json log
        self.HTMLLog = HTMLLogGenerator() #instancia de clase que genera el HTML Log
        

    """
    *Método: encryptFileOrDir
    *Parámetros: ruta del archivo o directorio a encriptar, ruta destino, contraseña.
    *Descripción: Evalua si la ruta ingresada es un archivo o un directorio. Si se es un archivo se manda a encriptar, si no, el método obtiene el nombre de la carpeta a encriptar y una lista de todos los archivos dentro del directorio(incluyendo subdirectorios) y con cada ruta de archivo se manda a llamar al método encryptDir. Además desde este método se mandan a llamar las funciones que crean los HTML y json logs cuando se ha encriptado.
    *Retorno: vector y matriz que contienen la información del proceso.
    """

    def encryptFileOrDir(self,_path,destiny,password):

        initTimes=[] #en este arreglo se ira guardando el tiempo inicial de encriptación de cada uno de los archivos.
        finalTimes=[] #en este arreglo se ira guardando el tiempos final de encriptación de cada uno de los archivos.
        fileSize=[] #en este arreglo se ira guardando el tamaño de cada archivo 
        
        if os.path.isfile(_path): #se evalua si la ruta pertenece a un archivo
            now=datetime.now() #tiempo en que inicia la encriptación del archivo.
            initTimes.append(now) 
            size=(os.stat(os.path.realpath(_path)).st_size)/1024 #se obtiene el tamaño del archivo en bytes y lo convertimos a KB
            fileSize.append(round(size,2)) #redonde el tamaño a dos cifras decimales.
            self.enc.encryptFile(_path, destiny, password)
            self.AES.encryptFile(_path,destiny,password) #se llama al método de la clase AES256 para encriptar el archivo.
            end=datetime.now() #tiempo en que finaliza la encriptación.
            finalTimes.append(end) 
            singleFile=[] #guardara en un arreglo la ruta del archivo
            singleFile.append(_path)
            
            vectorInfo, matrixInfo = self.info.filesReport(initTimes,finalTimes,fileSize,singleFile) #vectorInfo guarda el resumen de todo el proceso, matrixInfo guarda la información de cada archivo procesado. 
            self.HTMLLog.generateLog(vectorInfo,matrixInfo,"Encriptación",datetime.now()) #se encarga de crear el log de este proceso de encriptacion.

            return vectorInfo,matrixInfo

        else: #la ruta pertenece a un directorio
            dir= PurePath(_path).parts #obtentemos todos los fragementos de la ruta del directorio.
            dir=dir[-1] #debemos guardar el último elemento de la ruta, que es el directorio, para su posterior creación.
            listOfFiles = []
            for (dirpath, dirnames, filenames) in os.walk(_path): 
                listOfFiles+=[os.path.join(dirpath, file) for file in filenames]#obtenemos una lista de todas las rutas de los archivos dentro del directorio y subdirectorios.
            for path in listOfFiles: #por cada archivo en la lista mandamos a llamar al método encryptDir.
                now=datetime.now() #tiempo en que inicia la encriptación del archivo.
                initTimes.append(now)
                size=(os.stat(os.path.realpath(path)).st_size)/1024
                fileSize.append(round(size,2))
                self.encryptDir(path,destiny,dir, "e",password) #llamamos a el método encryptDir que se encarga de crear la estructura del directorio en la que se encuentra el archivo, y luego lo encripta.
                end=datetime.now()
                finalTimes.append(end) 
              
            rmtree(_path, ignore_errors=True) #eliminamos todas las carpetas que han quedado en la ruta origen.
            rmtree(_path, ignore_errors=True) 


            vectorInfo,matrixInfo=self.info.filesReport(initTimes,finalTimes,fileSize,listOfFiles) 
            self.HTMLLog.generateLog(vectorInfo, matrixInfo,"Encriptación",datetime.now())
            
            return vectorInfo, matrixInfo
                        
    """
    *Método: decryptFileOrDir
    *Parámetros: ruta del archivo o directorio a desencriptar, ruta destino, contraseña.
    *Descripción: Evalua si la ruta ingresada es un archivo o un directorio. Si se es un archivo se manda a desencriptar, si no, el método obtiene el nombre de la carpeta a desencriptar y una lista de todos los archivos dentro del directorio(incluyendo subdirectorios) y con cada ruta de archivo se manda a llamar al método encryptDir.
    *Retorno: vector y matriz que contienen la información del proceso.
    """

    def decryptFileOrDir(self,_path,destiny,password):
        
        initTimes=[]
        finalTimes=[]
        fileSize=[]

        if "AES_256" in (_path.split("/")):
            if os.path.isfile(_path):
                now=datetime.now()
                initTimes.append(now) 
                size=(os.stat(os.path.realpath(_path)).st_size)/1000
                fileSize.append(round(size,2))
                #self.enc.decryptFile(_path, destiny, password)
                self.AES.decryptFile(_path,destiny,password)
                end=datetime.now()
                finalTimes.append(end) 
                singleFile=[]
                singleFile.append(_path)
                
                vectorInfo, matrixInfo=self.info.filesReport(initTimes,finalTimes,fileSize,singleFile)##
                self.HTMLLog.generateLog(vectorInfo,matrixInfo,"Desencriptación",datetime.now())##
                
                return vectorInfo,matrixInfo

            else:
                dir= PurePath(_path).parts
                dir=dir[-1]
                listOfFiles = [] 
                for (dirpath, dirnames, filenames) in os.walk(_path):
                    listOfFiles+=[os.path.join(dirpath, file) for file in filenames]
                for path in listOfFiles:
                    now=datetime.now()
                    initTimes.append(now) 
                    size=(os.stat(os.path.realpath(path)).st_size)/1000
                    fileSize.append(round(size,2))
                    self.encryptDir(path,destiny,dir,"d",password)
                    end=datetime.now()
                    finalTimes.append(end) 

                rmtree(_path,ignore_errors=True)
                rmtree(_path,ignore_errors=True)

                vectorInfo, matrixInfo=self.info.filesReport(initTimes,finalTimes,fileSize,listOfFiles) 
                self.HTMLLog.generateLog(vectorInfo,matrixInfo,"Desencriptación",datetime.now())
                
                return vectorInfo,matrixInfo
        elif "OWN_Algorithm" in (_path.split("/")):
            if os.path.isfile(_path):
                now=datetime.now()
                initTimes.append(now) 
                size=(os.stat(os.path.realpath(_path)).st_size)/1000
                fileSize.append(round(size,2))
                self.enc.decryptFile(_path, destiny, password)
                #self.AES.decryptFile(_path,destiny,password)
                end=datetime.now()
                finalTimes.append(end) 
                singleFile=[]
                singleFile.append(_path)
                
                vectorInfo, matrixInfo=self.info.filesReport(initTimes,finalTimes,fileSize,singleFile)##
                self.HTMLLog.generateLog(vectorInfo,matrixInfo,"Desencriptación",datetime.now())##
                
                return vectorInfo,matrixInfo

            else:
                dir= PurePath(_path).parts
                dir=dir[-1]
                listOfFiles = [] 
                for (dirpath, dirnames, filenames) in os.walk(_path):
                    listOfFiles+=[os.path.join(dirpath, file) for file in filenames]
                for path in listOfFiles:
                    now=datetime.now()
                    initTimes.append(now) 
                    size=(os.stat(os.path.realpath(path)).st_size)/1000
                    fileSize.append(round(size,2))
                    self.encryptDir(path,destiny,dir,"d",password)
                    end=datetime.now()
                    finalTimes.append(end) 

                rmtree(_path,ignore_errors=True)
                rmtree(_path,ignore_errors=True)

                vectorInfo, matrixInfo=self.info.filesReport(initTimes,finalTimes,fileSize,listOfFiles) 
                self.HTMLLog.generateLog(vectorInfo,matrixInfo,"Desencriptación",datetime.now())
                
                return vectorInfo,matrixInfo

    """
    *Método: encryptDir
    *Parámetros: ruta del archivo a encriptar, ruta destino, nombre del directorio principal que se mandó a encriptar/desencriptar, proceso ("e"=encriptar / "d"=desencriptar) y contraseña.
    *Descripción: Este método se encarga de la creación de todos los subdirectorios, desde la carpeta principal, dentro de los cuales esta el archivo a encriptar o desencriptar. Luego se manda a llamar el método de la clase AES256 para encriptar/desencriptar el archivo en la nueva ruta destino del archivo.
    *Retorno: ----
    """

    def encryptDir(self, path, destiny, dir, process, password):

        originalDir=dir
        fileName=PurePath(path).parts #se fragmenta la ruta del archivo.
        fileName=fileName[-1] #el último elemento es el nombre del archivo.
        
        destiny1=destiny
        destiny2=destiny

        directory1 = "AES_256" if process=="e" else "DES_AES_256" #si en el párametro proceso se recibe una "e" el contenido encriptado se guardará en una carpeta llamada "AES_256", de lo contrario en una llamada "DES_AES_256"
        directory2 = "OWN_Algorithm" if process=="e" else "DES_OWN_Algorithm" #si en el párametro proceso se recibe una "e" el contenido encriptado se guardará en una carpeta llamada "AES_256", de lo contrario en una llamada "DES_AES_256"
        

        if process=="e":
            destiny1 = os.path.join(destiny1, directory1) #une la ruta destino con el nombre del directorio.
            destiny2 = os.path.join(destiny2, directory2) #une la ruta destino con el nombre del directorio.
            if not os.path.exists(destiny1): 
                os.mkdir(destiny1) #si no existe la nueva ruta destino la crea.
            if not os.path.exists(destiny2): 
                os.mkdir(destiny2) #si no existe la nueva ruta destino la crea.

            newDestiny1=PurePath(path).parts #se fragmenta la ruta del archivo
            index1=newDestiny1.index(originalDir) #se busca en la ruta fragmentada el directorio original que se mando a encriptar o desencriptar y retorna su índice.
            dirs1=newDestiny1[index1:-1] #en dirs se obtendra todos los subdirectorios desde la carpeta principal hasta llegar al archivo
            dirs1="/".join(dirs1) #se unen todos estos subdirectorios en una sola ruta. ############
            
            newDestiny1=os.path.join(destiny1,dirs1) #nueva ruta destino  

            newDestiny2=PurePath(path).parts #se fragmenta la ruta del archivo
            index2=newDestiny2.index(originalDir) #se busca en la ruta fragmentada el directorio original que se mando a encriptar o desencriptar y retorna su índice.
            dirs2=newDestiny2[index2:-1] #en dirs se obtendra todos los subdirectorios desde la carpeta principal hasta llegar al archivo
            dirs2="/".join(dirs2) #se unen todos estos subdirectorios en una sola ruta. ############
            newDestiny2=os.path.join(destiny2,dirs2) #nueva ruta destino


            if not os.path.exists(newDestiny1): 
                try:
                    os.makedirs(newDestiny1,0o700) #si no existe cualquiera de las directorios en la ruta, con 'os.makedirs' se crearan. 
                except OSError as e:
                    if e.errno!= errno.EEXIST: #solo se pasaran por alto los errores a causa de la ya existencia de las carpetas.
                        raise
            if not os.path.exists(newDestiny2):
                try:
                    os.makedirs(newDestiny2,0o700) #si no existe cualquiera de las directorios en la ruta, con 'os.makedirs' se crearan. 
                except OSError as e:
                    if e.errno!= errno.EEXIST: #solo se pasaran por alto los errores a causa de la ya existencia de las carpetas.
                        raise
            
        if process=="d":
            
            if ("AES_256" in (path.split("/"))):
                destiny1 = os.path.join(destiny1, directory1) #une la ruta destino con el nombre del directorio.
                if not os.path.exists(destiny1): 
                    os.mkdir(destiny1) #si no existe la nueva ruta destino la crea.
                newDestiny1=PurePath(path).parts #se fragmenta la ruta del archivo
                index1=newDestiny1.index(originalDir) #se busca en la ruta fragmentada el directorio original que se mando a encriptar o desencriptar y retorna su índice.
                dirs1=newDestiny1[index1:-1] #en dirs se obtendra todos los subdirectorios desde la carpeta principal hasta llegar al archivo
                dirs1="/".join(dirs1) #se unen todos estos subdirectorios en una sola ruta. ############
                
                newDestiny1=os.path.join(destiny1,dirs1) #nueva ruta destino  

                if not os.path.exists(newDestiny1): 
                    try:
                        os.makedirs(newDestiny1,0o700) #si no existe cualquiera de las directorios en la ruta, con 'os.makedirs' se crearan. 
                    except OSError as e:
                        if e.errno!= errno.EEXIST: #solo se pasaran por alto los errores a causa de la ya existencia de las carpetas.
                            raise
            if ("OWN_Algorithm" in (path.split("/"))):
                destiny2 = os.path.join(destiny2, directory1) #une la ruta destino con el nombre del directorio.
                if not os.path.exists(destiny2): 
                    os.mkdir(destiny2) #si no existe la nueva ruta destino la crea.
                newDestiny2=PurePath(path).parts #se fragmenta la ruta del archivo
                index2=newDestiny2.index(originalDir) #se busca en la ruta fragmentada el directorio original que se mando a encriptar o desencriptar y retorna su índice.
                dirs2=newDestiny2[index2:-1] #en dirs se obtendra todos los subdirectorios desde la carpeta principal hasta llegar al archivo
                dirs2="/".join(dirs2) #se unen todos estos subdirectorios en una sola ruta. ############
                
                newDestiny2=os.path.join(destiny2,dirs2) #nueva ruta destino  
                if not os.path.exists(newDestiny2):
                    try:
                        os.makedirs(newDestiny2,0o700) #si no existe cualquiera de las directorios en la ruta, con 'os.makedirs' se crearan. 
                    except OSError as e:
                        if e.errno!= errno.EEXIST: #solo se pasaran por alto los errores a causa de la ya existencia de las carpetas.
                            raise

        if process == "e": #si el proceso es "e" el archivo se manda a encriptar, de lo contrario se manda a desencriptar.
            self.enc.encryptFile(path,newDestiny2,password,originalDir)
            self.AES.encryptFile(path,newDestiny1,password,originalDir)
        else:
            if "OWN_Algorithm" in (path.split("/")):
                self.enc.decryptFile(path,newDestiny2,password,originalDir)
            elif "AES_256" in (path.split("/")):
                self.AES.decryptFile(path,newDestiny1,password,originalDir)

        
    

    

   
