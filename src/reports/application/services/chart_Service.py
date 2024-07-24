import base64
import io
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.colors as mcolors
matplotlib.use('Agg')


from src.reports.domain.repositores.estadistica_repository import EstadisticaRepository

class ChartService:
    def __init__(self, estadistica_repository: EstadisticaRepository):
        self.estadistica_repository = estadistica_repository

    def generar_serie_tiempo(self, estadisticas) -> bytes:
        fechas = [est.fecha_creacion for est in estadisticas]
        fechas.sort()

        plt.figure(figsize=(12, 6))
        plt.plot(fechas, range(len(fechas)))
        plt.title('Número acumulado de reportes a lo largo del tiempo')
        plt.xlabel('Fecha')
        plt.ylabel('Número de reportes')
        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        return buf.getvalue()

    def generar_grafico_circular_tipos(self, tipos) -> bytes:
        labels = [tipo['_id'] for tipo in tipos]
        sizes = [tipo['count'] for tipo in tipos]

        plt.figure(figsize=(10, 10))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Distribución de tipos de reportes')

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        return buf.getvalue()

    def generar_grafico_barras_causas(self, causas) -> bytes:
        # Mantener el orden original de las causas
        descripciones_largas = [causa['_id'] for causa in causas]
        valores = [causa['count'] for causa in causas]

        # Crear etiquetas cortas manteniendo el orden
        etiquetas_cortas = [
            "Construcción",
            "Acuario",
            "Basura parque",
            "Qué pasó",
            "Nuevo edificio",
            "Derrame químico",
            "Basura barrio",
            "Acumulación basura",
            "Construcción ruido",
            "Fábrica cemento"
        ]

        # Crear colores
        colores = plt.cm.get_cmap('tab10')(np.linspace(0, 1, len(etiquetas_cortas)))

        # Crear la figura y los ejes
        fig, ax = plt.subplots(figsize=(12, 6))

        # Crear las barras
        bars = ax.bar(range(len(valores)), valores, color=colores)

        # Configurar el título y las etiquetas
        ax.set_title('Top Causas de Reportes', fontsize=16)
        ax.set_ylabel('Número de reportes', fontsize=12)

        # Configurar el eje x
        ax.set_xticks(range(len(etiquetas_cortas)))
        ax.set_xticklabels(etiquetas_cortas, rotation=45, ha='right')

        # Añadir los valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}', ha='center', va='bottom')

        # Crear la leyenda
        handles = [plt.Rectangle((0,0),1,1, color=colores[i]) for i in range(len(etiquetas_cortas))]
        plt.legend(handles, descripciones_largas, title="Descripciones", 
                loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)

        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
        plt.close(fig)
        return buf.getvalue()
    
    def generar_analisis_serie_tiempo(self, result) -> bytes:
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 16))
        
        result.observed.plot(ax=ax1)
        ax1.set_title('Observado')
        result.trend.plot(ax=ax2)
        ax2.set_title('Tendencia')
        result.seasonal.plot(ax=ax3)
        ax3.set_title('Estacionalidad')
        result.resid.plot(ax=ax4)
        ax4.set_title('Residuos (Ruido)')

        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)

        return buf.getvalue()
    
    def _fig_to_base64(self, fig):
        img = io.BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()

    def generar_grafico_regresion_lineal(self, df, y_pred, columna_objetivo):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x=df[columna_objetivo], y=y_pred, ax=ax)
        ax.set(xlabel='Valor real', ylabel='Valor predicho', 
               title=f'Regresión Lineal Múltiple - {columna_objetivo}')
        ax.plot([df[columna_objetivo].min(), df[columna_objetivo].max()], 
                [df[columna_objetivo].min(), df[columna_objetivo].max()], 
                'r--', lw=2)
        return self._fig_to_base64(fig)

    def generar_grafico_descomposicion(self, resultado, titulo):
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 16))
        resultado.observed.plot(ax=ax1)
        ax1.set_title('Observado')
        resultado.trend.plot(ax=ax2)
        ax2.set_title('Tendencia')
        resultado.seasonal.plot(ax=ax3)
        ax3.set_title('Estacionalidad')
        resultado.resid.plot(ax=ax4)
        ax4.set_title('Residuos')
        fig.suptitle(titulo, fontsize=16)
        fig.tight_layout()
        return self._fig_to_base64(fig)

    def generar_grafico_suavizado_exponencial(self, df, predicciones):
        fig, ax = plt.subplots(figsize=(12, 6))
        df.plot(ax=ax, label='Observado')
        predicciones.plot(ax=ax, label='Predicho')
        ax.set_title('Suavizado Exponencial')
        ax.legend()
        return self._fig_to_base64(fig)

    def generar_grafico_importancia_caracteristicas(self, importancia, titulo):
        fig, ax = plt.subplots(figsize=(10, 6))
        importancia = pd.Series(importancia).sort_values(ascending=True)
        importancia.plot(kind='barh', ax=ax)
        ax.set_title(f'Importancia de características - {titulo}')
        ax.set_xlabel('Importancia')
        ax.set_ylabel('Características')
        return self._fig_to_base64(fig)

    def generar_grafico_lstm(self, y_test, predicciones):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(y_test, label='Real')
        ax.plot(predicciones, label='Predicho')
        ax.set_title('Predicciones LSTM vs Valores Reales')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Valor')
        ax.legend()
        return self._fig_to_base64(fig)
    
    