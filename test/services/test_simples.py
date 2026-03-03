import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


def testar():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    try:
        print("Tentando conectar ao Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Oi, responda apenas 'OK' se estiver me ouvindo.",
        )
        print("Sucesso:", response.text)
    except Exception as e:
        print("Erro detalhado:", type(e).__name__, "-", e)


if __name__ == "__main__":
    testar()
