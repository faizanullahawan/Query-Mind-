
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "openai/gpt-oss-20b"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")


llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0,
    max_retries=2
)


def test_llm():
    try:
        response = llm.invoke(
            "Explain what an SQL database is in one simple sentence."
        )

        print("Groq connection successful!")
        print("\nLLM Response:")
        print(response.content)

        return True

    except Exception as error:
        print(f"Groq connection failed: {error}")
        return False


if __name__ == "__main__":
    test_llm()
