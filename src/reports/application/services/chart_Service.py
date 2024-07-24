import base64
import io
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib
import pandas as pd
import seaborn as sns
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
        labels = [causa['_id'] for causa in causas]
        values = [causa['count'] for causa in causas]

        plt.figure(figsize=(12, 6))
        plt.bar(labels, values)
        plt.title('Top Causas de Reportes')
        plt.xlabel('Causa')
        plt.ylabel('Número de reportes')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
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
    
    