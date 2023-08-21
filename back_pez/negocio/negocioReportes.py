from sqlalchemy.orm import sessionmaker
from back_pez.db.model.reseniaAsignatura import ReseniaAsignatura
from negocio import negocioSugerenciaPrograma
from back_pez.db.model.programa import Programa
from back_pez.db.model.subComponente import subComponente
from back_pez.db.model.usuario import Usuario
from db.dbconfig import engine
from sqlalchemy import exists

from sqlalchemy.orm import selectinload

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

from openpyxl import Workbook
from openpyxl.styles import Alignment

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


Session = sessionmaker(bind=engine)

import json

def reportePrograma(id_programa):
    try:
        session = Session()

        programa = session.query(Programa).filter(Programa.id == id_programa).first()
        asignaturas = negocioSugerenciaPrograma.obtener_asignaturas_requeridas_programa(programa.id)

        reporte = []

        for asignatura in asignaturas:
            resenia = session.query(ReseniaAsignatura).filter(ReseniaAsignatura.asignatura_id == asignatura.id).all()

            total_reseñas = len(resenia)
            
            if total_reseñas > 0:
                porcentaje_aprendizaje = sum(1 for rese in resenia if rese.aprendizaje) / total_reseñas * 100
                porcentaje_tematicaRequeridas = sum(1 for rese in resenia if rese.tematicaRequeridas) / total_reseñas * 100
                porcentaje_estrategiasPedagogicasProfesor = sum(1 for rese in resenia if rese.estrategiasPedagogicasProfesor) / total_reseñas * 100
                porcentaje_actividadesAsignatura = sum(1 for rese in resenia if rese.actividadesAsignatura) / total_reseñas * 100
                porcentaje_agradoProfesor = sum(1 for rese in resenia if rese.agradoProfesor) / total_reseñas * 100
                porcentaje_cargaAsigantura = sum(1 for rese in resenia if rese.cargaAsigantura) / total_reseñas * 100
                porcentaje_entregaNotas = sum(1 for rese in resenia if rese.entregaNotas) / total_reseñas * 100
                porcentaje_retroalimentacion = sum(1 for rese in resenia if rese.retroalimentacion) / total_reseñas * 100
                porcentaje_complejidad_alta = sum(1 for rese in resenia if rese.complejidad == 'alto') / total_reseñas * 100
                porcentaje_complejidad_media = sum(1 for rese in resenia if rese.complejidad == 'medio') / total_reseñas * 100
                porcentaje_complejidad_baja = sum(1 for rese in resenia if rese.complejidad == 'bajo') / total_reseñas * 100
                porcentaje_vida = sum(1 for rese in resenia if rese.vidaOTrabajo == 'vida') / total_reseñas * 100
                porcentaje_trabajo = sum(1 for rese in resenia if rese.vidaOTrabajo == 'trabajo') / total_reseñas * 100
                porcentaje_nivelExigencia_alta = sum(1 for rese in resenia if rese.nivelExigencia == 'alto') / total_reseñas * 100
                porcentaje_nivelExigencia_media = sum(1 for rese in resenia if rese.nivelExigencia == 'medio') / total_reseñas * 100
                porcentaje_nivelExigencia_baja = sum(1 for rese in resenia if rese.nivelExigencia == 'bajo') / total_reseñas * 100
                porcentaje_incidencia_alta = sum(1 for rese in resenia if rese.incidenciaProfesor == 'alto') / total_reseñas * 100
                porcentaje_incidencia_media = sum(1 for rese in resenia if rese.incidenciaProfesor == 'medio') / total_reseñas * 100
                porcentaje_incidencia_baja = sum(1 for rese in resenia if rese.incidenciaProfesor == 'nada') / total_reseñas * 100
                comentarios = [rese.comentarios for rese in resenia]

                asignatura_info = {
                    'nombre_asignatura': asignatura.nombre,
                    'id_asignatura': asignatura.id,
                    'porcentaje_aprendizaje': porcentaje_aprendizaje,
                    'porcentaje_tematicaRequeridas': porcentaje_tematicaRequeridas,
                    'porcentaje_estrategiasPedagogicasProfesor': porcentaje_estrategiasPedagogicasProfesor,
                    'porcentaje_actividadesAsignatura': porcentaje_actividadesAsignatura,
                    'porcentaje_agradoProfesor': porcentaje_agradoProfesor,
                    'porcentaje_cargaAsigantura': porcentaje_cargaAsigantura,
                    'porcentaje_entregaNotas': porcentaje_entregaNotas,
                    'porcentaje_retroalimentacion': porcentaje_retroalimentacion,
                    'porcentaje_complejidad_alta': porcentaje_complejidad_alta,
                    'porcentaje_complejidad_media': porcentaje_complejidad_media,
                    'porcentaje_complejidad_baja': porcentaje_complejidad_baja,
                    'porcentaje_vida': porcentaje_vida,
                    'porcentaje_trabajo': porcentaje_trabajo,
                    'porcentaje_nivelExigencia_alta': porcentaje_nivelExigencia_alta,
                    'porcentaje_nivelExigencia_media': porcentaje_nivelExigencia_media,
                    'porcentaje_nivelExigencia_baja': porcentaje_nivelExigencia_baja,
                    'porcentaje_incidencia_alta': porcentaje_incidencia_alta,
                    'porcentaje_incidencia_media': porcentaje_incidencia_media,
                    'porcentaje_incidencia_baja': porcentaje_incidencia_baja,
                    'comentarios': comentarios
                }
                
                reporte.append(asignatura_info)
            else:
                asignatura_info = {
                    'nombre_asignatura': asignatura.nombre,
                    'id_asignatura': asignatura.id,
                    'porcentaje_aprendizaje': 0,
                    'porcentaje_tematicaRequeridas': 0,
                    'porcentaje_estrategiasPedagogicasProfesor': 0,
                    'porcentaje_actividadesAsignatura': 0,
                    'porcentaje_agradoProfesor': 0,
                    'porcentaje_cargaAsigantura': 0,
                    'porcentaje_entregaNotas': 0,
                    'porcentaje_retroalimentacion': 0,
                    'porcentaje_complejidad_alta': 0,
                    'porcentaje_complejidad_media': 0,
                    'porcentaje_complejidad_baja': 0,
                    'porcentaje_vida': 0,
                    'porcentaje_trabajo': 0,
                    'porcentaje_nivelExigencia_alta': 0,
                    'porcentaje_nivelExigencia_media': 0,
                    'porcentaje_nivelExigencia_baja': 0,
                    'porcentaje_incidencia_alta': 0,
                    'porcentaje_incidencia_media': 0,
                    'porcentaje_incidencia_baja': 0,
                    'comentarios': []
                }
                
                reporte.append(asignatura_info)

        return reporte

    except Exception as error:
        print(f"Error al generar el reporte de reseñas: {error}")
        return None


def generar_pdf_reporte(id_programa):
    reporte = reportePrograma(id_programa)
    doc = SimpleDocTemplate("reporte.pdf", pagesize=landscape(letter))
    story = []

    # Crear una tabla con los datos del reporte
    data = []  # Los datos de la tabla

    # Definir los nombres de las columnas en el encabezado
    column_names = [
        "Nombre Asignatura", 
        "ID Asignatura", 
        "Porcentaje Aprendizaje", 
        "Tematicas con lo que requeria",
        "Estrategias pedagogicas",
        "Actividades asignatura",
        "Agrado profesor",
        "Carga de trabajo adecuada",
        "Entrga notas a tiempo",
        "Retroalimentación adecuada",
        "Complejidad alta",
        "Complejidad media",
        "Complejidad baja",
        "Util para la vida",
        "Util para el trabajo",
        "Nivel exigencia alto",
        "Nivel exigencia medio",
        "Nivel exigencia bajo",
        "Incidencia profesor alta",
        "Incidencia profesor media",
        "Incidencia profesor baja",
        "Comentarios"
    ]

    # Agregar una fila para el encabezado a los datos
    data.insert(0, column_names)

    for asignatura_info in reporte:
        style = getSampleStyleSheet()['Normal']  # Puedes ajustar esto según tus necesidades

        # ... Código para crear la tabla y agregarla al story ...

        comentarios = [Paragraph(comentario, style) for comentario in asignatura_info['comentarios']]

        fila = [
            asignatura_info['nombre_asignatura'],
            asignatura_info['id_asignatura'],
            asignatura_info['porcentaje_aprendizaje'],
            asignatura_info['porcentaje_tematicaRequeridas'],
            asignatura_info['porcentaje_estrategiasPedagogicasProfesor'],
            asignatura_info['porcentaje_actividadesAsignatura'],
            asignatura_info['porcentaje_agradoProfesor'],
            asignatura_info['porcentaje_cargaAsigantura'],
            asignatura_info['porcentaje_entregaNotas'],
            asignatura_info['porcentaje_retroalimentacion'],
            asignatura_info['porcentaje_complejidad_alta'],
            asignatura_info['porcentaje_complejidad_media'],
            asignatura_info['porcentaje_complejidad_baja'],
            asignatura_info['porcentaje_vida'],
            asignatura_info['porcentaje_trabajo'],
            asignatura_info['porcentaje_nivelExigencia_alta'],
            asignatura_info['porcentaje_nivelExigencia_media'],
            asignatura_info['porcentaje_nivelExigencia_baja'],
            asignatura_info['porcentaje_incidencia_alta'],
            asignatura_info['porcentaje_incidencia_media'],
            asignatura_info['porcentaje_incidencia_baja'],
            comentarios
        ]
        data.append(fila)

    # Configurar estilo de tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('ROTATE', (0, 0), (-1, 0), 90)])

    # Calcular el ancho aproximado de cada columna
    num_columns = len(column_names)
    page_width, page_height = landscape(letter)
    column_width = page_width / num_columns

    # Ajustar los anchos de las columnas si es necesario
    column_widths = [column_width] * num_columns

    # Crear la tabla con los anchos de columna calculados
    t = Table(data, colWidths=column_widths)
    t.setStyle(style)
    story.append(t)

    # Agregar espacio en blanco
    story.append(Spacer(1, 12))

    # Crear el documento PDF
    doc.build(story)

    print("PDF generado exitosamente!")

def generar_excel_reporte(id_programa, correo):
    reporte = reportePrograma(id_programa)
    
    wb = Workbook()
    ws = wb.active
    
    # Agregar encabezados
    encabezados = [
        "Nombre Asignatura", 
        "ID Asignatura", 
        "Porcentaje Aprendizaje", 
        "Tematicas con lo que requeria",
        "Estrategias pedagogicas",
        "Actividades asignatura",
        "Agrado profesor",
        "Carga de trabajo adecuada",
        "Entrga notas a tiempo",
        "Retroalimentación adecuada",
        "Complejidad alta",
        "Complejidad media",
        "Complejidad baja",
        "Util para la vida",
        "Util para el trabajo",
        "Nivel exigencia alto",
        "Nivel exigencia medio",
        "Nivel exigencia bajo",
        "Incidencia profesor alta",
        "Incidencia profesor media",
        "Incidencia profesor baja",
        "Comentarios"
    ]
    ws.append(encabezados)

    # Agregar los datos
    for asignatura_info in reporte:
        fila = [
            asignatura_info['nombre_asignatura'],
            asignatura_info['id_asignatura'],
            asignatura_info['porcentaje_aprendizaje'],
            asignatura_info['porcentaje_tematicaRequeridas'],
            asignatura_info['porcentaje_estrategiasPedagogicasProfesor'],
            asignatura_info['porcentaje_actividadesAsignatura'],
            asignatura_info['porcentaje_agradoProfesor'],
            asignatura_info['porcentaje_cargaAsigantura'],
            asignatura_info['porcentaje_entregaNotas'],
            asignatura_info['porcentaje_retroalimentacion'],
            asignatura_info['porcentaje_complejidad_alta'],
            asignatura_info['porcentaje_complejidad_media'],
            asignatura_info['porcentaje_complejidad_baja'],
            asignatura_info['porcentaje_vida'],
            asignatura_info['porcentaje_trabajo'],
            asignatura_info['porcentaje_nivelExigencia_alta'],
            asignatura_info['porcentaje_nivelExigencia_media'],
            asignatura_info['porcentaje_nivelExigencia_baja'],
            asignatura_info['porcentaje_incidencia_alta'],
            asignatura_info['porcentaje_incidencia_media'],
            asignatura_info['porcentaje_incidencia_baja'],
            ", ".join(asignatura_info['comentarios'])  # Convertir la lista de comentarios a una cadena
        ]
        ws.append(fila)


    # Alinear el texto al centro en todas las celdas
    for row in ws.iter_rows(min_row=1, max_row=1):  # Alinea solo la primera fila (encabezados)
        for cell in row:
            cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # Guardar el archivo
    wb.save("reporte.xlsx")
    
    print("Archivo de Excel generado exitosamente!")
    enviar_correo_reporte("reporte.xlsx",correo)


def enviar_correo_reporte(archivo_adjunto, correo):
    # Datos de configuración del correo
    remitente = 'lalis.mora98@gmail.com'
    contraseña = 'wtksfmxjegqagtpx'
    servidor_smtp = 'smtp.gmail.com'
    puerto = 587

    destinatario = correo
    #destinatario ='lalis.mora98@gmail.com'
    asunto = 'Reporte programa'
    mensaje = 'Buenos días, adjunto el reporte del programa.'

    # Crear objeto MIME para el correo
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Agregar cuerpo del mensaje
    msg.attach(MIMEText(mensaje, 'plain'))

    # Agregar archivo adjunto
    with open(archivo_adjunto, "rb") as adjunto:
        part = MIMEApplication(adjunto.read(), Name=archivo_adjunto)
        part['Content-Disposition'] = f'attachment; filename="{archivo_adjunto}"'
        msg.attach(part)

    # Establecer conexión con el servidor SMTP
    server = smtplib.SMTP(host=servidor_smtp, port=puerto)
    server.starttls()
    server.login(remitente, contraseña)

    # Enviar correo
    server.sendmail(remitente, destinatario, msg.as_string())
    server.quit()



