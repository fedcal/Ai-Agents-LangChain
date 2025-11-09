import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_community.output_parsers import PydanticOutputParser
from langchain.chains.openai_functions import convert_to_openai_function
from typing_extensions import Annotated
from dotenv import load_dotenv
from typing_extensions import Annotated, TypedDict
from pydantic import BaseModel, Field 

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

class UserInfo(TypedDict):
    name: Annotated[str, "", "User's name. default is 'Guest'"]
    country: Annotated[str, "", "User's country of residence. default is 'Unknown'"]

class PydanticUserInfo(BaseModel):
    name: Annotated[str, Field(default="Guest", description="User's name. Default is 'Guest'")]
    country: Annotated[str, Field(default="Unknown", description="User's country of residence. Default is 'Unknown'")]

class Performer(BaseModel):
    name: Annotated[str, Field(description="Name of the performer")]
    film_names: Annotated[list[str], Field(description="List of film names the performer has acted in")]

def parse_boolean(response_text: str) -> bool:
    """Parser boolean manuale"""
    clean_response = response_text.lower().strip()
    return clean_response in ['true', 'yes', 'sì', 'si', '1']

if __name__ == '__main__':
    """parser = StrOutputParser()
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

    llm_with_structure = llm.with_structured_output(UserInfo)
    print(llm_with_structure.invoke("My name is Alice and I live in Canada."))

    print(llm_with_structure.invoke("Ciao"))"""

    print("\n=== Pydantic Model Output ===")

    llm_with_structure = llm.with_structured_output(PydanticUserInfo)

    structured_output = llm_with_structure.invoke("My name is John and I live in USA.")
    print(structured_output.name)

    llm_with_structure = llm.with_structured_output(Performer)
    response = llm_with_structure.invoke("Tell me about the actor Tom Hanks and list some of his movies.")
    print(response)

    # Restituisce il JSON grezzo
    print(response.json())

    parser = PydanticOutputParser(pydantic_object = Performer)
    print (parser.parse(response.json()))

    misformatted_json = "{'name': 'Tom Hanks', 'film_names': ['Forrest Gump', 'Cast Away']}"
    try:
        print (parser.parse(misformatted_json))
    except OutputParserException as e:
        print(f"Parsing error: {e}")

    new_parser = OutputFixingParser.from_llm(llm, parser)
    print(new_parser.parse(misformatted_json))

