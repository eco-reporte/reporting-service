
import openai
from src.reports.domain.entities.estadistica_reporte import EstadisticaReporte
from src.reports.domain.repositores.estadistica_repository import EstadisticaRepository
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configura tu clave de API desde la variable de entorno
openai.api_key = os.getenv('key_openai')

class NLPService:
    def __init__(self, estadistica_repository: EstadisticaRepository):
        self.estadistica_repository = estadistica_repository

    def analizar_reporte(self, reporte):
        try:
            descripcion = reporte.descripcion
            tipo_reporte = reporte.tipo_reporte
            fecha_creacion = reporte.fecha_creacion

            causa, ubicacion, afectado = self.extraer_informacion(descripcion)

            estadistica = EstadisticaReporte(
                categoria=tipo_reporte,
                que_paso=causa,
                donde_paso=ubicacion,
                a_quien_paso=afectado,
                fecha=fecha_creacion
            )

            return self.estadistica_repository.save(estadistica)
        except Exception as e:
            print(f"Error en analizar_reporte: {str(e)}")
            return None

    def extraer_informacion(self, texto):
        prompt = f"""
        Texto: {texto}
        
        Extrae la siguiente información:
        1. ¿Qué pasó?
        2. ¿Dónde pasó?
        3. ¿A quién le pasó?
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # O usa "gpt-4" si está disponible
                messages=[
                    {"role": "system", "content": "Eres un asistente que extrae información de textos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )

            respuestas = response.choices[0].message['content'].strip().split('\n')

            causa = respuestas[0].split('1. ')[1] if len(respuestas) > 0 and '1. ' in respuestas[0] else ""
            ubicacion = respuestas[1].split('2. ')[1] if len(respuestas) > 1 and '2. ' in respuestas[1] else ""
            afectado = respuestas[2].split('3. ')[1] if len(respuestas) > 2 and '3. ' in respuestas[2] else ""

            return causa, ubicacion, afectado
        except Exception as e:
            print(f"Error en extraer_informacion: {str(e)}")
            return "", "", ""