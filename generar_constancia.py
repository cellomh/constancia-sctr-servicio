"""
Generador de la Constancia SCTR - Salud (Viscaya / Sanitas).

Diseño aprobado por Cello (ver proyecto "Viscaya Desarrollo",
doc claude/sctr-constancia-diseno.md):
  - Solo logo y firma de Sanitas (nada de Protecta, nada de pensión).
  - Subtítulo: SEGURO COMPLEMENTARIO DE TRABAJO DE RIESGO DE SALUD.
  - Recuadro: Contrato SCTR - Salud N°: 1120550.
  - Tabla dinámica de personas aseguradas.
  - QR de validación propio de Viscaya (por ahora, QR de EJEMPLO
    porque el sistema de validación real todavía no existe).
  - Pie legal: no cobertura para actividades no declaradas +
    intermediado por Nakama Corredores de Seguros S.A.C.

Uso:
    from generar_constancia import generar_constancia
    generar_constancia(datos, "salida.pdf")

`datos` es un dict con las llaves que usa DATOS_EJEMPLO más abajo.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(HERE, "logo_sanitas.png")
FIRMA_PATH = os.path.join(HERE, "firma_sanitas.png")
QR_PATH = os.path.join(HERE, "qr_ejemplo.png")

AZUL_SANITAS = HexColor("#00205B")
GRIS_TEXTO = HexColor("#333333")


def _estilos():
    hoja = getSampleStyleSheet()
    hoja.add(ParagraphStyle(
        name="TituloConstancia", parent=hoja["Heading1"],
        fontName="Helvetica-Bold", fontSize=26, leading=30,
        alignment=TA_CENTER, textColor=HexColor("#111111"), spaceAfter=2,
    ))
    hoja.add(ParagraphStyle(
        name="Subtitulo", parent=hoja["Normal"],
        fontName="Helvetica-Bold", fontSize=10.5, leading=13,
        alignment=TA_CENTER, textColor=GRIS_TEXTO, spaceAfter=14,
    ))
    hoja.add(ParagraphStyle(
        name="NombreEmpresa", parent=hoja["Normal"],
        fontName="Helvetica-Bold", fontSize=15, leading=18,
        alignment=TA_CENTER, textColor=HexColor("#111111"), spaceAfter=4,
    ))
    hoja.add(ParagraphStyle(
        name="DatoCentrado", parent=hoja["Normal"],
        fontName="Helvetica-Bold", fontSize=9.5, leading=14,
        alignment=TA_CENTER, textColor=HexColor("#111111"),
    ))
    hoja.add(ParagraphStyle(
        name="Referencia", parent=hoja["Normal"],
        fontName="Helvetica-Bold", fontSize=9.5, leading=13,
        alignment=TA_CENTER, textColor=HexColor("#111111"),
    ))
    hoja.add(ParagraphStyle(
        name="EtiquetaDato", parent=hoja["Normal"],
        fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=GRIS_TEXTO,
    ))
    hoja.add(ParagraphStyle(
        name="ValorDato", parent=hoja["Normal"],
        fontName="Helvetica", fontSize=9, leading=12, textColor=GRIS_TEXTO,
    ))
    hoja.add(ParagraphStyle(
        name="Legal", parent=hoja["Normal"],
        fontName="Helvetica", fontSize=8, leading=11,
        alignment=TA_JUSTIFY, textColor=GRIS_TEXTO, spaceBefore=10,
    ))
    hoja.add(ParagraphStyle(
        name="PieLegal", parent=hoja["Normal"],
        fontName="Helvetica-Oblique", fontSize=7, leading=9.5,
        alignment=TA_JUSTIFY, textColor=HexColor("#555555"),
    ))
    hoja.add(ParagraphStyle(
        name="FirmaNombre", parent=hoja["Normal"],
        fontName="Helvetica-Bold", fontSize=9, leading=11,
        alignment=TA_CENTER, textColor=GRIS_TEXTO,
    ))
    hoja.add(ParagraphStyle(
        name="FirmaCargo", parent=hoja["Normal"],
        fontName="Helvetica", fontSize=8, leading=10,
        alignment=TA_CENTER, textColor=GRIS_TEXTO,
    ))
    hoja.add(ParagraphStyle(
        name="QrEtiqueta", parent=hoja["Normal"],
        fontName="Helvetica-Oblique", fontSize=6.5, leading=8,
        alignment=TA_CENTER, textColor=HexColor("#B00000"),
    ))
    hoja.add(ParagraphStyle(
        name="TablaHeader", parent=hoja["Normal"],
        fontName="Helvetica-Bold", fontSize=8, leading=10,
        alignment=TA_CENTER, textColor=HexColor("#FFFFFF"),
    ))
    hoja.add(ParagraphStyle(
        name="TablaCelda", parent=hoja["Normal"],
        fontName="Helvetica", fontSize=8, leading=10,
        alignment=TA_LEFT, textColor=GRIS_TEXTO,
    ))
    return hoja


def generar_constancia(datos: dict, ruta_salida: str):
    hoja = _estilos()
    doc = SimpleDocTemplate(
        ruta_salida, pagesize=A4,
        topMargin=16 * mm, bottomMargin=14 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
    )
    elementos = []

    # --- Encabezado: logo (solo Sanitas) + título grande ---
    logo = Image(LOGO_PATH, width=30 * mm, height=30 * mm * (73 / 200))
    elementos.append(logo)
    elementos.append(Spacer(1, 2))
    elementos.append(Paragraph("CONSTANCIA", hoja["TituloConstancia"]))
    elementos.append(Paragraph("SEGURO COMPLEMENTARIO DE TRABAJO DE RIESGO DE SALUD", hoja["Subtitulo"]))

    # --- Empresa / RUC / vigencia / actividad, centrado (como el ejemplo) ---
    elementos.append(Paragraph(datos["empresa"], hoja["NombreEmpresa"]))
    elementos.append(Paragraph(f"RUC: {datos['ruc']}", hoja["DatoCentrado"]))
    elementos.append(Paragraph(
        f"VIGENCIA: {datos['vigencia_inicio']} al {datos['vigencia_fin']}", hoja["DatoCentrado"]))
    elementos.append(Paragraph(f"ACTIVIDAD: {datos['actividad'].upper()}", hoja["DatoCentrado"]))
    elementos.append(Spacer(1, 10))

    # --- Párrafo introductorio (solo salud, sin pensión) ---
    intro = (
        "Por medio del presente dejamos constancia que los asegurados detallados líneas abajo, "
        "conforme al Decreto Supremo 003-98-SA, se encuentran amparados bajo la cobertura de salud "
        "de trabajo de riesgo del Seguro Complementario de Trabajo de Riesgo*."
    )
    elementos.append(Paragraph(intro, hoja["Legal"]))
    elementos.append(Spacer(1, 10))

    # --- Recuadro de referencia (solo Salud, sin fila de Pensión) ---
    ref = Table(
        [[Paragraph(f"Contrato SCTR - Salud N°: {datos['contrato_numero']}", hoja["Referencia"])]],
        colWidths=[None],
    )
    ref.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, HexColor("#111111")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elementos.append(ref)
    elementos.append(Spacer(1, 6))
    elementos.append(Paragraph(f"Sede: {datos.get('sede', 'PRINCIPAL')}", hoja["EtiquetaDato"]))
    elementos.append(Spacer(1, 8))

    # --- Tabla de personas aseguradas ---
    encabezado = ["Nro.", "Nombres", "Apellido Paterno", "Apellido Materno", "Nro. Documento"]
    filas = [[Paragraph(h, hoja["TablaHeader"]) for h in encabezado]]
    for i, persona in enumerate(datos["asegurados"], start=1):
        filas.append([
            Paragraph(str(i), hoja["TablaCelda"]),
            Paragraph(persona["nombres"], hoja["TablaCelda"]),
            Paragraph(persona["apellido_paterno"], hoja["TablaCelda"]),
            Paragraph(persona["apellido_materno"], hoja["TablaCelda"]),
            Paragraph(persona["numero_documento"], hoja["TablaCelda"]),
        ])
    tabla_asegurados = Table(filas, colWidths=[12 * mm, 46 * mm, 36 * mm, 36 * mm, 30 * mm], repeatRows=1)
    tabla_asegurados.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL_SANITAS),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#AAAAAA")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#FFFFFF"), HexColor("#F5F7FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla_asegurados)

    # --- Nota al pie del asterisco de la intro ---
    nota_asterisco = "* Cobertura exclusiva de salud de trabajo de riesgo (Viscaya no comercializa SCTR Pensión)."
    elementos.append(Paragraph(nota_asterisco, hoja["PieLegal"]))
    elementos.append(Spacer(1, 16))

    # --- Firma + QR ---
    firma_img = Image(FIRMA_PATH, width=32 * mm, height=32 * mm * (189 / 299))
    bloque_firma = [
        firma_img,
        Paragraph("Carlos Alfredo Chavarriaga Ceballos", hoja["FirmaNombre"]),
        Paragraph("Representante Legal<br/>Sanitas Perú S.A. EPS", hoja["FirmaCargo"]),
    ]
    qr_img = Image(QR_PATH, width=22 * mm, height=22 * mm)
    bloque_qr = [
        qr_img,
        Paragraph("Escanea para validar esta constancia", hoja["FirmaCargo"]),
        Paragraph("QR DE EJEMPLO — pendiente desarrollar el propio", hoja["QrEtiqueta"]),
    ]

    tabla_firma_qr = Table(
        [[bloque_firma, bloque_qr]],
        colWidths=[None, 45 * mm],
    )
    tabla_firma_qr.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elementos.append(KeepTogether(tabla_firma_qr))
    elementos.append(Spacer(1, 14))

    # --- Pie legal ---
    pie = (
        "No se brindará cobertura para actividades, labores o procesos que no hayan sido declarados "
        "explícitamente a la aseguradora. El presente contrato SCTR es intermediado por Nakama "
        "Corredores de Seguros S.A.C."
    )
    elementos.append(Paragraph(pie, hoja["PieLegal"]))

    doc.build(elementos)


DATOS_EJEMPLO = {
    "contrato_numero": "1120550",
    "sede": "PRINCIPAL",
    "empresa": "ACMA RESEARCH S.A.C.",
    "ruc": "20601234567",
    "vigencia_inicio": "17/10/2026 00:00",
    "vigencia_fin": "16/11/2026",
    "actividad": "Gasfitería independiente",
    "asegurados": [
        {
            "nombres": "Juan",
            "apellido_paterno": "Pérez",
            "apellido_materno": "Quispe",
            "numero_documento": "DNI - 45678912",
        },
    ],
}

if __name__ == "__main__":
    generar_constancia(DATOS_EJEMPLO, os.path.join(HERE, "constancia_ejemplo.pdf"))
    print("Listo: constancia_ejemplo.pdf")
