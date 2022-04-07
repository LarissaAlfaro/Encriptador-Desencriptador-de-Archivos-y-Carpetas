#-*-coding:utf-8-*-
from datetime import datetime
import os
import math

"""
*Nombre de la clase: obtainInfo
*Atributos: ----
*Descripción: Esta clase obtiene la información para generar los HTML y json log.
"""

class obtainInfo:
    def __init__(self):
        pass

    """
    *Método: executionTime
    *Parámetros: tiempo inicial de encriptación/desencriptación de archivo, tiempo final de encriptación/desencriptación de archivo.
    *Descripción: Mediante operaciones básicas de conversión y uso de los atributos de datetime.datetime se obtiene el tiempo de procesamiento del archivo en segundos.
    *Retorno: Tiempo de procesamiento en segundos.
    """

    def executionTime(self,initTime,finalTime):

        diff=finalTime-initTime 
        t=diff.days*24*60*60 #se convierten los dias a segundos y se acumulan a la variable t.
        t+=diff.seconds #se acumulan los segundos
        t+=diff.microseconds/1000/1000 #se convierten los microsegundos a segundos y se acumulan.
        return t

    """
    *Método: filesReport
    *Parámetros: un arreglo que contiene el tiempo inicial del proceso de cada uno de los archivos, un arreglo que contiene el tiempo final del proceso de cada uno de los archivos, un arreglo con los tamaños de cada archivo, un arreglo con las rutas de cada uno de los archivos.
    *Descripción: Mediante operaciones básicas de conversión y uso de los atributos de datetime.datetime se obtiene el tiempo de procesamiento del archivo en segundos.
    *Retorno: Tiempo de procesamiento en segundos.
    """

    def filesReport(self,initTime,finalTime,fileSize,paths):

        names=[] #guardaran todos los nombres.
        exeTime=[] #se guardaran todos los tiempos de encriptación/desencriptación.
        size=[] #guarda todos los tamaños de los archivos.
        count=[] #un arreglo con el número de archivo en el proceso.
        fileCount=totalTime=totalSize=0 #variable contador y variables acumuladoras de las cantidades totales.

        for i in range(len(paths)): #se recorre para la cantidad de rutas que se han encriptado/desencriptado.

            fileCount+=1 #se cuentan los archivos.
            count.append(fileCount) #se agrega el contador al arreglo.
            
            pathParts=paths[i].split("/") #se fragmenta la ruta de cada archivo   ###########
            names.append(pathParts[-1]) #se obtiene el nombre de cada archivo, que es el último elemento de la ruta, y se agrega al arreglo de nombres.
            
            totalSize+=fileSize[i] #acumula el tamaño de cada archivo.
            size.append("%s KB" % fileSize[i]) #agrega el tamaño de cada archivo al arreglo que contiene los tamaños.

            time=round(self.executionTime(initTime[i],finalTime[i]),3) #se calcula el tiempo de ejecución de cada archivo con la función executionTime y se redondea a 3 cifras decimales.
            totalTime+=time #acumla el tiempo de ejecución al tiempo total.
            exeTime.append("%ss" % time) #agrega el tiempo actual al arreglo que contiene los tiempos de cada archivo.
        
    
        filesInfo=[[count[i],names[i],exeTime[i],size[i]]for i in range(len(paths))] #se crea una matriz con toda la información contenida en los 3 arreglos de información que se han construido.

        generalInfo=[] #contendra la información resumen del proceso.
        generalInfo.append(fileCount) #agrega al arreglo de resumen el número total de archivos que se han procesado.

        if totalTime>60 or False: #en este ciclo se evalua si el tiempo total de procesamiento de todos los archivos es mayor a un minuto o no, para poder guardar de manera correcta el tiempo total de procesamiento de la operación en el vector de información resumen. 
            totalTime=totalTime/60
            totalTime=round(totalTime,1)
            decimal,integer=math.modf(totalTime)
            totalTime="%s minutos %s segundos" % (int(integer), int(decimal*10)*6)
            generalInfo.append(totalTime)
        else:
            generalInfo.append(round(totalTime,3))

        generalInfo.append(round(totalSize,3)) #agrega el tamaño en conjunto de todos los archivos al arreglo resumen.
        

        print(filesInfo)##
        print("\n\n")
        print(generalInfo)##

        return generalInfo,filesInfo #retorna el arreglo resumen de la operación, y la matriz de información de cada archivo procesado para la creación de los logs.

    