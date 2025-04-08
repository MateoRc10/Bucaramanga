#Se pueden modificar, se accede por indice
lista = ["Pedro", 56.5, True,"Juan"]
lista[0]= False

#No se pueden modificar, se accede por indice
Tupla = ("Pedro", True, 5, 7.5)

#Se Reconstruir pero no modificar, No se pueden repetir valores, no se puede aceder por indice
conjunto = {5, True, False, "Mateo"}
conjunto = {5, 6 ,"Pedro" , 8.2} #Reconstruccion

#Llamamos los datos por sus llaves
Diccionario = {
    "Nombre" : "Mateo Restrepo",
    "Edad" : 18,
    "Musica" : "Tame Impala"
}

print("Pedro" not in lista)

print(Tupla[0])
print(conjunto)
print(Diccionario["Edad"])