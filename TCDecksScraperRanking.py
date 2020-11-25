# -*- coding: utf-8 -*-
import unicodedata,urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, date, time, timedelta
import calendar
import csv, operator
import glob
 
#Método para analizar una dirección web
def descargaInfo(archivo,conexion):
    html = conexion.read()
    soup = BeautifulSoup(html)
    #Obtenemos una lista de string con los datos de cada fila
    datos = soup.find_all('td')
    for each in datos:
        texto = str(each.get_text())
        #cadena = NomCamp+hrefe+texto
        cadena = texto
        #adaptamos unicode a utf-8
        normalizado = unicodedata.normalize('NFKD', cadena).encode('ascii','ignore').decode('ascii')
        TextoFormateado = ""
        #Buscamos las / para encontrar la fecha, nos servirá de campo de corte
        encontrarbarras = normalizado.count("/")
        if encontrarbarras == 2:
            TextoFormateado = normalizado + "\n"
        else:
            TextoFormateado = normalizado + ";"
            
        print(TextoFormateado)
        archivo.write(TextoFormateado)
         
#Este método se conectará con la web y establece un timeout que obliga a reintentar el fallo
def preparacionDatos(archivo,web):
    #try:
        print(web)
        conector = urllib.request.urlopen(web,timeout=10)#timeout de 10 segundos
        #conector = requests.get(web)
        descargaInfo(archivo,conector)
    #except:
        #print("Tiempo de espera agotado, volviendo a intentar")
        #preparacionDatos(archivo,web)
        
#Comprueba si la fecha es válida
def comprobar_fecha(a, m, d):
    #Array que almacenara los dias que tiene cada mes (si el anyo es bisiesto, sumaremos +1 al febrero)
    dias_mes = [31, 28, 31, 30,31, 30, 31, 31, 30, 31, 30, 31]
                
    #Comprobar si el anyo es bisiesto y anadir dia en febrero en caso afirmativo
    if((a%4 == 0 and a%100 != 0) or a%400 == 0):
        dias_mes[1] += 1
 
    #Comprobar que el mes sea valido
    if(m < 1 or m > 12):
        return False
                    
    #Comprobar que el dia sea valido
    m -= 1
    if(d <= 0 or d > dias_mes[m]):
        return False
                        
    #Si ha pasado todas estas condiciones, la fecha es valida
    return True
                
#Programa principal
print('Comienza el programa')
archivo=open('BaseDatosTCDecks.csv','w')
archivo.write("Archetype;"+"Format;"+"Player;"+"Tournament Name;"+"Position;"+"Date\n")
#El CSV separa las columnas por medio de tabuladores
# Introducir fecha inicial utilizando el formato definido
fecha_desde_teclado = input('Introducir fecha inicial (dd-mm-aaaa): ')
fecha_desde = datetime.strptime(fecha_desde_teclado, '%d-%m-%Y')
if fecha_desde_teclado == "":
    print('Fecha erronea')
fecha_hasta_teclado = input('Introducir fecha final   (dd-mm-aaaa): ')
fecha_hasta = datetime.strptime(fecha_hasta_teclado, '%d-%m-%Y')
if fecha_hasta_teclado == "":
    print('Fecha erronea')
       
currentDate = fecha_desde
        
while currentDate <= fecha_hasta: 
    comprobacion = comprobar_fecha(currentDate.year,currentDate.month,currentDate.day)
    if comprobacion != True:
        break
    else:
        if fecha_hasta >= currentDate:
            print("Preparando conexion...")
            anyo = str(currentDate.year)
            if(currentDate.month >= 1 and currentDate.month < 10):
                mes = '0'+str(currentDate.month)
            else:
                mes = str(currentDate.month)
            if(currentDate.day >= 1 and currentDate.day < 10):
                dia = '0'+str(currentDate.day)
            else:
                dia = str(currentDate.day)
                
            #Ruta de la página web     
            url = 'https://www.tcdecks.net/results.php?token=Decks&tname=&nlow=&nhigh=&from='+anyo+'%2F'+mes+'%2F'+dia+'&to='+anyo+'%2F'+mes+'%2F'+dia+'&player=&aname=&dname=&format=Noformat&main=&nomain=&side=&noside=&strict=on'
            print("Conexion establecida")
            print("Creando/Modificando fichero csv")
            preparacionDatos(archivo,url)
        else:
            print("La fecha fecha final debe ser mayor o igual que la inicial")
            break
    currentDate += timedelta(days=1)
            
archivo.close()
print('Fin del programa')