import json
import requests
import os

def cargueCompetencias():
    file_path = os.path.join(os.path.dirname(__file__), 'Competencias.json')

    with open(file_path, 'r') as f:
        datos = json.load(f)

    for datos_competencia in datos['competencias']:
        response = requests.post('http://localhost:8000/competencia', json=datos_competencia)
        print(response.json())

def cargueContenido():
    file_path = os.path.join(os.path.dirname(__file__), 'Contenido.json')

    with open(file_path,'r') as f:
        datos = json.load(f)

    for contenido in datos['contenidos']:
        response = requests.post('http://localhost:8000/tematica', json=contenido)
        print(response.json())

def cargueDatosGenerales():
    file_path = os.path.join(os.path.dirname(__file__), 'datos.json')

    with open(file_path,'r') as f:
        datos = json.load(f)
    
    for actividad in datos['actividades']:
        response = requests.post('http://localhost:8000/actividad', json=actividad)
        print(response.json())
    
    for modo in datos['ModoEnsenianza']:
        print(modo)
        response = requests.post('http://localhost:8000/modoEnsenianza', json=modo)
        print(response.json())

    for componente in datos['ComponenteClase']:
        response = requests.post('http://localhost:8000/componenteClase', json=componente)
        print(response.json())

    for horario in datos['Horario']:
        response = requests.post('http://localhost:8000/horario', json=horario)
        print(response.json())

def cargueAsignaturas():
    file_path = os.path.join(os.path.dirname(__file__), 'Asignaturas.json')

    with open(file_path,'r') as f:
        datos = json.load(f)

    for asignatura in datos['Asignaturas']:
        response = requests.post('http://localhost:8000/asignatura', json=asignatura)
        print(response.json())

def cargueMAINN():
    file_path = os.path.join(os.path.dirname(__file__), 'MAINN.json')

    with open(file_path,'r') as f:
         datos = json.load(f)

    for subComponente in datos['subComponentes']:
        response = requests.post('http://localhost:8000/subcomponente', json=subComponente)
        print(response.json())

    for componente in datos['componentes']:
        response = requests.post('http://localhost:8000/componente', json=componente)
        print(response.json())

    for programa in datos['programa']:
        print(programa)
        response = requests.post('http://localhost:8000/programa', json=programa)
        print(response.json())

def cargueMINSC():
    file_path = os.path.join(os.path.dirname(__file__), 'MINSC.json')

    with open(file_path,'r') as f:
         datos = json.load(f)

    for componente in datos['componentes']:
        response = requests.post('http://localhost:8000/componente', json=componente)
        print(response.json())

    for programa in datos['programa']:
        response = requests.post('http://localhost:8000/programa', json=programa)
        print(response.json())

def cargueMINSCDistri():
    file_path = os.path.join(os.path.dirname(__file__), 'MINSCDistri.json')

    with open(file_path,'r') as f:
         datos = json.load(f)

    for componente in datos['componentes']:
        response = requests.post('http://localhost:8000/componente', json=componente)
        print(response.json())

    for programa in datos['programa']:
        response = requests.post('http://localhost:8000/programa', json=programa)
        print(response.json())

def cargueSeguridad():
    file_path = os.path.join(os.path.dirname(__file__), 'seguridad.json')
    with open(file_path,'r') as f:
         datos = json.load(f)

    for subComponente in datos['subComponentes']:
        response = requests.post('http://localhost:8000/subcomponente', json=subComponente)
        print(response.json())

    for componente in datos['componentes']:
        response = requests.post('http://localhost:8000/componente', json=componente)
        print(response.json())

    for programa in datos['programa']:
        response = requests.post('http://localhost:8000/programa', json=programa)
        print(response.json())

def main():
    
    print("--------------------")
    print("Cargar competencias")
    cargueCompetencias()
    print("--------------------")
    print("Cargar contenido")
    cargueContenido()
    print("--------------------")
    print("Cargar datos generales")
    cargueDatosGenerales()
    print("--------------------")
    print("Cargar Asignaturas")
    cargueAsignaturas()
    print("--------------------")
    print("Cargar MAINN")
    cargueMAINN()
    print("--------------------")
    print("Cargar MINSC")
    cargueMINSC()
    print("--------------------")
    print("Cargar MINSC seguridad")
    cargueMINSCDistri()
    print("--------------------")
    print("Cargar Seguridad Digital")
    cargueSeguridad()



