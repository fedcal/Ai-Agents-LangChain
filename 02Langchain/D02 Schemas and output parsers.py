import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from typing_extensions import Annotated, TypedDict

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

class UserInfo(TypedDict):
    name: Annotated[str, "", "User's name. default is 'Guest'"]
    country: Annotated[str, "", "User's country of residence. default is 'Unknown'"]

def parse_boolean(response_text: str) -> bool:
    """Parser boolean manuale"""
    clean_response = response_text.lower().strip()
    return clean_response in ['true', 'yes', 'sì', 'si', '1']

if __name__ == '__main__':
    parser = StrOutputParser()
    print(parser.invoke(
        llm.invoke("Hello, world! Give me a short greeting.")
    ))

    print("\n=== Date Output ===")
    date = parser.invoke(
        llm.invoke("Give me today's date in YYYY-MM-DD format. Return only the date.")
    )
    print(f"Date: {date}")

    print("\n=== Boolean Output ===")
    bool_response = parser.invoke(
        llm.invoke("Is the sky blue? Answer with true or false only.")
    )
    print(f"Raw response: {bool_response}")
    print(f"Parsed boolean: {parse_boolean(bool_response)}")

