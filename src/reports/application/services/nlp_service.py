from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from src.reports.domain.repositores.estadistica_repository import EstadisticaRepository
from src.reports.domain.entities.estadistica_reporte import EstadisticaReporte

class NLPService:
    def __init__(self, estadistica_repository: EstadisticaRepository):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.estadistica_repository = estadistica_repository
    
    def analizar_reporte(self, reporte):
        try:
            descripcion = reporte.descripcion
            tipo_reporte = reporte.tipo_reporte
            fecha_creacion = reporte.fecha_creacion

            causa, ubicacion, afectado = self.extraer_informacion(descripcion)

            estadistica = EstadisticaReporte(
                causa=causa,
                ubicacion=ubicacion,
                afectado=afectado,
                fecha_creacion=fecha_creacion,
                tipo_reporte=tipo_reporte
            )

            return self.estadistica_repository.save(estadistica)
        except Exception as e:
            print(f"Error en analizar_reporte: {str(e)}")
            # Decide si quieres propagar el error o manejarlo aquí
            return None


    def extraer_informacion(self, texto):
        prompt = f"Analiza el siguiente texto y responde las preguntas:\n\nTexto: {texto}\n\n1. ¿Qué pasó?\n2. ¿Dónde pasó?\n3. ¿A quién le pasó?\n\nResponde en formato:\n1. [lo que pasó]\n2. [dónde pasó]\n3. [a quién le pasó]"

        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        outputs = self.model.generate(inputs, max_length=200, num_return_sequences=1, temperature=0.7, do_sample=True)
        respuestas = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        respuestas = respuestas.split('\n')[5:]  # Ignorar las primeras líneas del prompt
        respuestas = [respuesta.strip() for respuesta in respuestas if respuesta.strip()]
        
        causa = respuestas[0].split('1. ')[1] if len(respuestas) > 0 and '1. ' in respuestas[0] else ""
        ubicacion = respuestas[1].split('2. ')[1] if len(respuestas) > 1 and '2. ' in respuestas[1] else ""
        afectado = respuestas[2].split('3. ')[1] if len(respuestas) > 2 and '3. ' in respuestas[2] else ""
    
        return causa, ubicacion, afectado