from sqlalchemy.orm import sessionmaker
from back_pez.db.model.reseniaAsignatura import ReseniaAsignatura
from negocio import negocioSugerenciaPrograma
from back_pez.db.model.programa import Programa
from back_pez.db.model.subComponente import subComponente
from back_pez.db.model.usuario import Usuario
from db.dbconfig import engine
from sqlalchemy import exists

from sqlalchemy.orm import selectinload

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
                porcentaje_complejidad_alta = sum(1 for rese in resenia if rese.complejidad == 'alta') / total_reseñas * 100
                porcentaje_complejidad_media = sum(1 for rese in resenia if rese.complejidad == 'media') / total_reseñas * 100
                porcentaje_complejidad_baja = sum(1 for rese in resenia if rese.complejidad == 'baja') / total_reseñas * 100
                porcentaje_vida = sum(1 for rese in resenia if rese.vidaOTrabajo == 'vida') / total_reseñas * 100
                porcentaje_trabajo = sum(1 for rese in resenia if rese.vidaOTrabajo == 'trabajo') / total_reseñas * 100
                porcentaje_nivelExigencia_alta = sum(1 for rese in resenia if rese.nivelExigencia == 'alta') / total_reseñas * 100
                porcentaje_nivelExigencia_media = sum(1 for rese in resenia if rese.nivelExigencia == 'media') / total_reseñas * 100
                porcentaje_nivelExigencia_baja = sum(1 for rese in resenia if rese.nivelExigencia == 'baja') / total_reseñas * 100
                porcentaje_incidencia_alta = sum(1 for rese in resenia if rese.incidenciaProfesor == 'alta') / total_reseñas * 100
                porcentaje_incidencia_media = sum(1 for rese in resenia if rese.incidenciaProfesor == 'media') / total_reseñas * 100
                porcentaje_incidencia_baja = sum(1 for rese in resenia if rese.incidenciaProfesor == 'baja') / total_reseñas * 100
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



