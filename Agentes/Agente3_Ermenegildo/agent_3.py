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
    "fields": "NCTId,BriefTitle,OverallStatus,LeadSponsorName,CollaboratorName,StartDate,Phase,HasResults,Condition",
 # las columnas que quieres, tú decides cuáles
    "pageSize": 1000 #maximo que permite la api
}

#nombre largo que devuelve la api -> nombre limpio
columnas_ensayos={
    "protocolSection.identificationModule.nctId":"nct_id",
    "protocolSection.identificationModule.briefTitle":"title",
    "protocolSection.statusModule.overallStatus":"status",
    "protocolSection.statusModule.startDateStruct.date":"start_date",
    "protocolSection.sponsorCollaboratorsModule.leadSponsor.name":"sponsor",
    "protocolSection.sponsorCollaboratorsModule.collaborators":"collaborators",
    "protocolSection.conditionsModule.conditions":"conditions",
    "protocolSection.designModule.phases":"phase",
    "hasResults":"has_results"
}

#max() sobre strings ordena alfabeticamente, asi que el orden se define a mano
orden_fases={"NA":0,"EARLY_PHASE1":1,"PHASE1":2,"PHASE2":3,"PHASE3":4,"PHASE4":5}


#url_mercado=
#params1=#igual biosimilares?
#url_prevalencia=
#params2=#biosimilares

def obtencion_datos_ensayos(url,params):
    try:
        #la api pagina los resultados: se repite la peticion hasta que no haya nextPageToken
        params=dict(params)
        estudios=[]
        while True:
            respuesta=requests.get(url,params,timeout=15)
            respuesta.raise_for_status()
            datos=respuesta.json()
            estudios.extend(datos["studies"])
            token=datos.get("nextPageToken")
            if not token:
                break
            params["pageToken"]=token

        datos_ensayos=pd.json_normalize(estudios)
        #reindex garantiza todas las columnas aunque ningun estudio traiga alguna
        datos_ensayos=datos_ensayos.reindex(columns=list(columnas_ensayos)).rename(columns=columnas_ensayos)

        #collaborators llega como lista de dicts [{"name":...}] o NaN si no hay
        datos_ensayos["collaborators"]=datos_ensayos["collaborators"].apply(lambda lista:"; ".join(c["name"] for c in lista) if isinstance(lista,list) and lista else None)
        datos_ensayos["conditions"]=datos_ensayos["conditions"].apply(lambda lista:"; ".join(lista) if isinstance(lista,list) and lista else None)
        datos_ensayos["phase"]=datos_ensayos["phase"].apply(lambda lista:max(lista,key=lambda fase:orden_fases.get(fase,-1)) if isinstance(lista,list) and lista else None)
        #las fechas vienen como "2018-12-12" o solo "2013-05"
        datos_ensayos["start_date"]=pd.to_datetime(datos_ensayos["start_date"],format="ISO8601",errors="coerce")
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



def analisis_panoramico(tabla):
    print(tabla.shape)
    print(tabla.dtypes)
    print(tabla.describe())
    print(tabla.isnull())
    print( tabla["conditions"].describe()) 
    print(tabla["collaborators"].describe())
    return
tabla = obtencion_datos_ensayos(url_ensayos, params)
resultado = analisis_panoramico(tabla)



#obtener=obtencion_datos_ensayos(url_ensayos,params)
#print(obtener.head())
#obtener.info()