from OxiPulso import app, db
from OxiPulso.Mediciones.models import Mediciones
from OxiPulso.Autenticacion.models import Usuario
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import datetime

def calcular_edad(fecha_nacimiento):
    today = datetime.date.today()
    return today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

def basicos():
    with app.app_context():
        datos = db.session.query(Usuario, Mediciones).join(
            Mediciones, Usuario.id == Mediciones.usuario_id
        ).with_entities(
            Usuario.nombre, Usuario.fechaNacimiento, Mediciones.bpm, Mediciones.spo2, Mediciones.hora, Mediciones.fecha
        ).all()
        
        df = pd.DataFrame(datos, columns=['Nombre', 'FechaNacimiento', 'BPM', 'SPO2', 'Hora', 'Fecha'])
        
       
        df['BPM'] = pd.to_numeric(df['BPM'], errors='coerce')
        df['SPO2'] = pd.to_numeric(df['SPO2'], errors='coerce')
        
        df = df.dropna(subset=['BPM', 'SPO2'])
        
        
        df['Edad'] = df['FechaNacimiento'].apply(calcular_edad).astype(int)
        
       
        bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100]
        labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
        df['RangoEdad'] = pd.cut(df['Edad'], bins=bins, labels=labels, right=False)
        
       
        df['Hora'] = df['Hora'].apply(lambda x: x.strftime('%H:%M:%S'))
        df['Fecha_Hora'] = pd.to_datetime(df['Fecha'].astype(str) + ' ' + df['Hora'])

        bpm_max = df['BPM'].max()
        bpm_min = df['BPM'].min()
        spo2_max = df['SPO2'].max()
        spo2_min = df['SPO2'].min()

        bpm_max_data = df[df['BPM'] == bpm_max].to_dict(orient='records')
        bpm_min_data = df[df['BPM'] == bpm_min].to_dict(orient='records')
        spo2_max_data = df[df['SPO2'] == spo2_max].to_dict(orient='records')
        spo2_min_data = df[df['SPO2'] == spo2_min].to_dict(orient='records')

        fig_timeline, ax_timeline = plt.subplots(figsize=(10, 5))
        ax_timeline.plot(df['Hora'], df['BPM'], label='BPM', color='blue')
        ax_timeline.plot(df['Hora'], df['SPO2'], label='SPO2', color='red')
        ax_timeline.set_xlabel('Hora')
        ax_timeline.set_ylabel('Valor')
        ax_timeline.set_title('Línea de tiempo de BPM y SPO2')
        ax_timeline.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

      
        timeline_img = io.BytesIO()
        fig_timeline.savefig(timeline_img, format='png')
        timeline_img.seek(0)
        timeline_base64 = base64.b64encode(timeline_img.getvalue()).decode('utf-8')

        
        df_grouped = df.groupby('RangoEdad')[['BPM', 'SPO2']].mean()

        fig_barras, ax_barras = plt.subplots(figsize=(10, 6))
        df_grouped.plot(kind='bar', ax=ax_barras, color=['skyblue', 'salmon'])
        ax_barras.set_xlabel('Rango de Edad')
        ax_barras.set_ylabel('Promedio')
        ax_barras.set_title('Promedio de BPM y SPO2 por rango de edad')
        ax_barras.grid(True)
        ax_barras.legend(['BPM', 'SPO2'])

        # Convertir la figura a imagen y codificarla en base64
        barras_img = io.BytesIO()
        fig_barras.savefig(barras_img, format='png')
        barras_img.seek(0)
        barras_base64 = base64.b64encode(barras_img.getvalue()).decode('utf-8')

        return (
            bpm_max_data,
            bpm_min_data,
            spo2_max_data,
            spo2_min_data,
            timeline_base64,
            barras_base64
        )
