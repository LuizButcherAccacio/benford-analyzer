from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.templating import Jinja2Templates
from io import StringIO
import pandas as pd
from fastapi.responses import FileResponse
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from benford import analisar_benford

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Armazena o último resultado analisado
ultimo_resultado = None


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/analisar")
async def analisar(
    request: Request,
    coluna: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        conteudo = await file.read()

        df = pd.read_csv(
            StringIO(conteudo.decode("utf-8"))
        )

        resultado = analisar_benford(
            df,
            coluna
        )

        global ultimo_resultado
        ultimo_resultado = resultado

        return templates.TemplateResponse(
            request=request,
            name="resultado.html",
            context={
                "resultado": resultado
            }
        )

    except ValueError as erro:
        return {
            "erro": str(erro)
        }

    except Exception as erro:
        return {
            "erro": f"Erro interno: {str(erro)}"
        }


@app.get("/exportar-pdf")
async def exportar_pdf():

    global ultimo_resultado

    if not ultimo_resultado:
        return {
            "erro": "Nenhuma análise disponível"
        }

    resultado = ultimo_resultado

    nome_pdf = "benford_report.pdf"

    doc = SimpleDocTemplate(nome_pdf)

    estilos = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph(
            "Benford Analysis Report",
            estilos["Title"]
        )
    )

    elementos.append(Spacer(1, 12))

    elementos.append(
        Paragraph(
            f"Analyzed Column: {resultado['coluna']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Valid Records: {resultado['registros_validos']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Total Deviation: {resultado['desvio_total']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Conclusion: {resultado['conclusao']}",
            estilos["Normal"]
        )
    )

    elementos.append(Spacer(1, 20))

    elementos.append(
        Paragraph(
            "Statistical Tests",
            estilos["Heading2"]
        )
    )

    elementos.append(
        Paragraph(
            f"MAD: {resultado['mad']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"MAD Classification: {resultado['classificacao_mad']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Chi-Square: {resultado['qui_quadrado']}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Critical Value: {resultado['valor_critico']}",
            estilos["Normal"]
        )
    )

    elementos.append(Spacer(1, 20))

    dados_tabela = [
        ["Digit", "Observed (%)", "Benford (%)"]
    ]

    for digito in resultado["digitos"]:

        dados_tabela.append([
            str(digito),
            resultado["observado"][str(digito)],
            resultado["benford"][str(digito)]
        ])

    tabela = Table(dados_tabela)

    tabela.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.blue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ])
    )

    elementos.append(tabela)

    doc.build(elementos)

    return FileResponse(
        nome_pdf,
        media_type="application/pdf",
        filename=nome_pdf
    )