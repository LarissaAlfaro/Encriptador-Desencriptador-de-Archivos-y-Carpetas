#-*-coding:utf-8-*-
import os

"""
*Nombre de la clase: HTMLLogGenerator
*Atributos: ----
*Descripción: Se encarga de contruir la estructura de un archivo html y luego crear el archivo en el directorio LOGS HTML.
"""

class HTMLLogGenerator:

    def __init__(self):
        self.content = '<!DOCTYPE html><html><head><style>body{background-color:rgba(0, 179, 179);}h1{color:Black;}table,th,td{background-color: rgba(0,128,128);border:1px solid rgba(0, 179, 179);color:White};</style></head><body><h1>Resumen</h1><table>'

    """
    *Método: generateLog
    *Parámetros: vectorResumen, matriz de la información de cada archivo, proceso(encriptación/desencriptación), tiempo en que se crea el archivo.
    *Descripción: Mediante este método se crea la estructura del archivo html junto a la información obtenida del proceso en el vector y matriz que recibe como parámetro. 
    *Retorno:----
    """

    def generateLog(self,vectorInfo,matrixInfo,process,end):
        self.content+= '<th colspan="2">Proceso Ejecutado: %s</th><tr><td>Archivos Procesados</td><td>%s</td></tr><tr><td>Tiempo</td><td>%s</td></tr><tr><td>Tamaño Total</td><td>%s</td></tr></table><br><br><br><table><th colspan="4">Archivos: %s</th><tr><td>No.</td><td>Nombre</td><td>Tiempo de Procesamiento</td><td>Tamaño</td></tr>' % (process,vectorInfo[0],vectorInfo[1],vectorInfo[2],process) #aqui se usa el vector resumen para la primera tabla del html.

        for row in matrixInfo: #por cada elemento en la matriz se crea una celda en la segunda tabla de información por archivo.
            self.content+='<tr>'
            for elem in row:
                self.content+='<td>%s</td>' % elem
            self.content+='</tr>'
        
        self.content+='</table></body></html>'
        self.createHTML(self.content,end) #manda a crear el archivo html.

    """
    *Método: createHTML
    *Parámetros: el contenido del html a crear, y el tiempo en que se creara el archivo despues de ejecutar el proceso de encriptación/desencriptación.
    *Descripción: Se crea el archivo html en el directorio LOGS HTML con el formato de LOG_AÑO_MES_DÍA_HORA_MINUTO_SEGUNDO.html
    *Retorno: ----
    """
        
    def createHTML(self,content,end):
        docName="LOG_%s_%s_%s_%s_%s_%s.html" % (end.year,end.month,end.day,end.hour,end.minute,end.second)
        with open(r"LOGS/LOGS HTML/ %s" % docName ,"w") as htmlDoc: ########
            htmlDoc.write(content)

        