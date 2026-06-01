from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.templating import Jinja2Templates
from io import StringIO
import pandas as pd

from benford import analisar_benford

app = FastAPI()

templates = Jinja2Templates(directory="templates")


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