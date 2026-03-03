from google import genai
from google.api_core import exceptions
from dataclasses import dataclass
from fastapi import HTTPException, status
from typing import List
from app.models.resource import TipoResource
from pydantic import BaseModel, ValidationError
from app.infra.config import settings
from loguru import logger


class IaResponse(BaseModel):
    descricao: str
    tags: List[str]


@dataclass
class IaService:

    def sugerir_descricao_e_tags(self, titulo: str, tipo: TipoResource):
        prompt = f"""
            CONTEXTO: Você é um assistente especializado em um sistema de gerenciamento de recursos (vídeos, links e PDFs).
            ENTRADA: Você irá receber um titulo e um tipo(vídeo, link, PDF).
            TAREFA: Sua tarefa é gerar descrições curtas e profissionais e sugerir 3 tags de uma única palavra com base no titulo e na tag.
            FORMATO: Retorne SEMPRE um JSON válido seguindo o schema fornecido.

            titulo: {titulo}
            tipo: {tipo}
            """  # noqa: E501
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": IaResponse.model_json_schema(),
                },
            )

            return IaResponse.model_validate_json(response.text)
        except exceptions.DeadlineExceeded:

            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Tempo limite foi atingido",
            )
        except exceptions.ServiceUnavailable:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Serviço do gemini está indisponível",
            )
        except ValidationError as ve:
            logger.error(f"Erro de validação Pydantic: {ve.json()}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Ocorreu um erro na descrição do gemini",
            )
