from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad 
from Crypto.Hash import SHA256
from pathlib import Path
from pathlib import PurePath
import os


"""
*Nombre de la clase: AES256
*Atributos: ----
*Descripción: Con esta clase podemos encriptar y desencriptar archivos haciendo uso del esquema de cifrado por bloques AES256
"""

class AES256: 

    def __init__(self):
        self.bSize=16 #el tamaño de bloque de este cifrado es de 16 bytes.

    """
    *Método: encrypt
    *Parámetros: mensaje a encriptar, contraseña para generar llave de enciptación.
    *Descripción: El método se encarga de generar un nuevo cifrado AES que recibe una llave, y el modo de operación para cifrar 'ECB'. Mediante el método 'encrypt' se encripta el mensaje ya rellenado.
    *Retorno: texto encriptado
    """

    def encrypt(self,message,password): 
        key=SHA256.new(password.encode('utf-8')).digest() #se genera una llave para encriptar con la contraseña ingresada.
        encrypter=AES.new(key, AES.MODE_ECB)
        encrypted=encrypter.encrypt(pad(message,self.bSize))
        return encrypted

    """
    *Método: decrypt
    *Parámetros: mensaje a desencriptar, contraseña para generar llave de desencriptación.
    *Descripción: El método se encarga de generar un nuevo cifrado AES que recibe una llave, y el modo de operación para cifrar 'ECB'. Mediante el método 'decrypt' se desencripta el mensaje encriptado. Luego de esto remueven los caracteres que se utilizaron de relleno.
    *Retorno: mensaje en texto plano.
    """

    def decrypt(self,message,password):
        key=SHA256.new(password.encode('utf-8')).digest() #se genera una llave para desencriptar con la contraseña ingresada. Debe ser la misma contraseña con la cual se encriptó el archivo, si no se generará un error.
        decrypter=AES.new(key, AES.MODE_ECB) 
        plainText=decrypter.decrypt(message)
        decyphered=unpad(plainText, self.bSize)
        return decyphered

    """
    *Método: encryptFile
    *Parámetros: recibe la ruta donde se encuentra el archivo en texto plano, ruta donde se quiere guardar el archivo encriptado, contraseña y en caso de encriptarse una carpeta, entonces también recibe el nombre de la carpeta principal.
    *Descripción: Abre el archivo, lo lee y su contenido lo guarda para posteriormente encriptarlo mediante el método 'encrypt'. Luego se obtiene el nombre del archivo y se agrega la extensión '.enc'. Si esta encriptando solamente un archivo individual y no una carpeta, entonces el método crea el directorio 'AES_256' y genera la nueva ruta destino. Por último se crea el archivo con el contenido encriptado en la nueva ruta y se elimina el archivo original.
    *Retorno: ----
    """

    def encryptFile(self,filePath,destiny,password,dir=None): 
    
        with open(filePath, 'rb') as inputFile: #utilizamos la sentencia with para abrir el archivo de manera efectiva (manejo de errores, cierra archivo, etc.) Lee en 'rb' ya que al encriptar se opera en binario.
            plainText=inputFile.read()
        encrypted=self.encrypt(plainText,password)


        pathSplit = PurePath(filePath).parts #obtenemos la ruta en segmentos
        fileName=pathSplit[-1]+".enc" #obtenemos el último elemento en la ruta, que es el nombre del archivo, luego le concatenamos la extensión '.enc'.

        if not dir: #si el método no recibio un directorio entonces se esta encriptando un solo archivo
            directory = "AES_256" 
            destiny= os.path.join(destiny,directory) #unimos la ruta 'destino' con la carpeta "AES_256" donde se tiene que guardar el archivo encriptado.
            if not os.path.exists(destiny): #si la carpeta no existe en tal ruta
                os.mkdir(destiny) #se crea.
        else:
            pass
        
        newFilePath=os.path.join(destiny,fileName) #creamos la ruta completa con el nombre del archivo.
  
        with open(newFilePath, 'wb') as outputFile: #se crea el archivo en la ruta destino y escribe en binario.  
            outputFile.write(encrypted) #escribe el contenido encriptado.
        os.remove(filePath) #elimina el archivo original.

    """
    *Método: decryptFile
    *Parámetros: recibe la ruta donde se encuentra el archivo a desencriptar, ruta donde se quiere guardar el archivo en texto plano, contraseña, y en caso de desencriptarse una carpeta, entonces también recibe el nombre de la carpeta principal.
    *Descripción: Abre el archivo, lo lee y su contenido lo guarda para posteriormente desencriptarlo mediante el método 'decrypt'. Luego se obtiene el nombre del archivo y se elimina la extensión '.enc'. Si esta desencriptando solamente un archivo individual y no una carpeta, entonces el método crea el directorio 'DES_AES_256' y genera la nueva ruta destino. Por último se crea el archivo con el contenido desencriptado en la nueva ruta y se elimina el archivo encriptado.
    *Retorno: ----
    """

    def decryptFile(self,filePath,destiny,password,dir=None):
        
        with open(filePath, 'rb') as inputFile:
            encryptedText=inputFile.read()
        dec=self.decrypt(encryptedText,password)

        pathSplit = PurePath(filePath).parts
        fileName=pathSplit[-1] #obtenemos el último elemento en la ruta, que es el nombre del archivo.
        fileName=fileName[:-4] #al nombre del archivo se le elimina la extensión .enc 
    
        if not dir:
            directory = "DES_AES_256"
            destiny=os.path.join(destiny,directory) #unimos ruta 'destino' con la carpeta "DES_AES_256" donde se tiene que guardar el archivo en texto plano.
            if not os.path.exists(destiny):
                os.mkdir(destiny)
        else:
            pass

        newFilePath=os.path.join(destiny,fileName) 

        with open(newFilePath, 'wb') as fileOutput:
            fileOutput.write(dec)
        os.remove(filePath)

