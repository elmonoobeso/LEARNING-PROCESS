import pandas as pd
import numpy as np
import requests
import json
from pathlib import Path
import os
from dotenv import load_dotenv
#import google.generativeai as genai

#load_dotenv()
#genai.configure(api_key=os.environ["Gemini_API_KEY"])



url_ensayos="https://clinicaltrials.gov/api/v2/studies"

params = {
    "query.intr": "biosimilar",
    "fields": "NCTId,BriefTitle,OverallStatus,LeadSponsorName,CollaboratorName,StartDate,Phase,HasResults,Condition"
 # las columnas que quieres, tú decides cuáles
}


#url_mercado=
#params1=#igual biosimilares?
#url_prevalencia=
#params2=#biosimilares

def obtencion_datos_ensayos(url,params):
    try:
        respuesta=requests.get(url,params,timeout=15)
        respuesta.raise_for_status()
        datos=respuesta.json()
        
        datos_ensayos=pd.json_normalize(datos, record_path="studies")
        comprueba=datos["studies"][0]["protocolSection"].keys()
        datos_ensayos["phases"]=datos_ensayos["protocolSection.designModule.phases"].apply(lambda lista:max(lista) if isinstance(lista,list) and lista else None)
        #datos_ensayos["collaborators"]=datos_ensayos["protocolSection.sponsorCollaboratorsModule.collaborators"].apply(if: isinstance(lista,list) and lista else None)
        print(comprueba)
        return datos_ensayos
       
    
    except requests.exceptions.Timeout:
        print("la respuesta tardo demasiado")
    except requests.exceptions.HTTPError as error:
        print(f"Error HTTP: {error}")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con la A")

def obtencion_datos_mercado(url_mercado,params1):
    try:
        respuesta=requests.get(url_mercado,params1,timeout=15)
        respuesta.raise_for_status()
        datos=respuesta.json()
        return datos["results"]
    except requests.exceptions.Timeout:
        print("la respuesta tardo demasiado")
    except requests.exceptions.HTTPError as error:
        print(f"Error HTTP: {error}")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con la A")

def obtencion_datos_prevalencia(url_prevalencia,params2):
    try:
        headers = {"X-App-Token": os.environ["CDC_APP_TOKEN"]}
        respuesta=requests.get(url_prevalencia, params2, headers=headers)
        respuesta.raise_for_status()
        datos=respuesta.json()
        return datos["results"][0]
    except requests.exceptions.Timeout:
        print("la respuesta tardo demasiado")
    except requests.exceptions.HTTPError as error:
        print(f"Error HTTP: {error}")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con la A")

obtener=obtencion_datos_ensayos(url_ensayos,params)
print(obtener)


