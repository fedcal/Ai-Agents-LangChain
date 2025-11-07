### Scenario

# Immagina di lavorare come sviluppatore per una startup tecnologica che desidera integrare funzionalità basate sull'intelligenza artificiale nella propria piattaforma.
# Il tuo compito è configurare l'infrastruttura di base per comunicare con un LLM, perfezionarne le risposte e garantire che generi output significativi.
# Questo è un primo passo fondamentale prima di passare ad applicazioni di intelligenza artificiale più avanzate.

### Sfida

# In questo esercizio, ti verrà chiesto di creare un'applicazione che aiuti gli analisti di marketing a creare contenuti.

# Lavorate tutti per CultPass, un'azienda B2B fittizia che ha sviluppato una carta benefit per le aziende, al fine di offrire ai propri
# dipendenti più esperienze culturali, come musei, gallerie d'arte, concerti, ecc.


from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=api_key
)


# Una volta impostati tutti i parametri, è necessario accettare l'input dell'utente da inviare all'API OpenAI.
#
# Per accettarlo, aggiungi un nuovo elemento all'elenco `messages` all'interno della funzione `create_content`.
# Si tratta di un dizionario simile al primo elemento, ma questa volta il ruolo è `user`.
def create_content(query: str,
                   client: OpenAI,
                   system_prompt: str,
                   model: str,
                   temperature: float) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )

    # Experiment returning the full response to understand the object
    content = response.choices[0].message.content

    return content

if __name__ == '__main__':
    # Modello LLM da utilizzare
    model = "gpt-4o-mini"

    # Rappresenta quanto la risposta deve essere randomica. Range tra 0.0 e 1.0
    temperature = 0.3

    # E' uno dei parametri più potenti, dice infatti come L'LLM deve comportarsi. Deve essere scritto in maniera chiara e concisa.
    # Ad esempio supponendo di lavorare per un'azienda B2B che sviluppa una carta benefit per le altre aziende per offrire ai loro impiegati esperienze culturali.
    system_prompt = """
        Agisci come creatore di contenuti B2B. Crea testi per campagne di marketing per raggiungere il pubblico dell'azienda CultPass,
        che ha sviluppato una carta benefit per le aziende che vogliono offrire ai propri dipendenti più opportunità culturali, come musei, gallerie d'arte,
        concerti ed esperienze simili. Non fornire spiegazioni, solo il materiale da inviare.
    """

    # Input
    analyst_query = "Create an instagram post for clients in the automotive industry"

    content = create_content(
        query=analyst_query,
        client=client,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature
    )

    print(content)




