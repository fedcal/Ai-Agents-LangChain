# Schema e Output Parsers in LangChain

Questo documento spiega in dettaglio l'utilizzo di schemi e parser di output in LangChain, basandosi sul file `D02 Schemas and output parsers.py`.

## Indice
1. [Setup Iniziale](#setup-iniziale)
2. [Definizione delle Strutture Dati](#definizione-delle-strutture-dati)
3. [Parser di Base](#parser-di-base)
4. [Parser Strutturati](#parser-strutturati)
5. [Gestione degli Errori](#gestione-degli-errori)

## Setup Iniziale

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_community.output_parsers import PydanticOutputParser
```

Il codice inizia importando le librerie necessarie:
- `os`: Per gestire le variabili d'ambiente
- `ChatOpenAI`: Il modello di linguaggio di OpenAI
- `StrOutputParser`: Parser base per output in formato stringa
- `BaseModel` e `Field` da Pydantic: Per definire modelli di dati strutturati
- `PydanticOutputParser`: Per parsare output in modelli Pydantic

La configurazione del modello LLM viene fatta così:
```python
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```
- `temperature=0.0`: Rende le risposte più deterministiche
- L'API key viene caricata dalle variabili d'ambiente

## Definizione delle Strutture Dati

### TypedDict per Informazioni Utente
```python
class UserInfo(TypedDict):
    name: Annotated[str, "", "User's name. default is 'Guest'"]
    country: Annotated[str, "", "User's country of residence. default is 'Unknown'"]
```
Questa classe utilizza `TypedDict` per definire una struttura dati tipizzata con:
- `name`: Nome dell'utente (stringa)
- `country`: Paese di residenza (stringa)
Le annotazioni forniscono metadati aggiuntivi per ciascun campo.

### Modello Pydantic per Informazioni Utente
```python
class PydanticUserInfo(BaseModel):
    name: Annotated[str, Field(default="Guest", description="User's name. Default is 'Guest'")]
    country: Annotated[str, Field(default="Unknown", description="User's country of residence. Default is 'Unknown'")]
```
Versione Pydantic della stessa struttura che aggiunge:
- Validazione dei dati
- Valori predefiniti
- Descrizioni dei campi
- Serializzazione/deserializzazione automatica

### Modello Performer
```python
class Performer(BaseModel):
    name: Annotated[str, Field(description="Name of the performer")]
    film_names: Annotated[list[str], Field(description="List of film names the performer has acted in")]
```
Modello per gestire informazioni su attori/performer:
- `name`: Nome del performer
- `film_names`: Lista di film in cui ha recitato

## Parser di Base

### Parser Booleano Personalizzato
```python
def parse_boolean(response_text: str) -> bool:
    clean_response = response_text.lower().strip()
    return clean_response in ['true', 'yes', 'sì', 'si', '1']
```
Funzione utility per convertire risposte testuali in booleani:
- Pulisce e normalizza il testo (lowercase e rimozione spazi)
- Supporta multiple forme di "vero" in diverse lingue

### StrOutputParser
```python
parser = StrOutputParser()
```
Parser base che:
- Gestisce output testuali semplici
- Converte la risposta del LLM in una stringa
- Utilizzato per risposte non strutturate

Esempi di utilizzo:
1. Saluto semplice:
```python
parser.invoke(llm.invoke("Hello, world! Give me a short greeting."))
```

2. Formattazione data:
```python
date = parser.invoke(
    llm.invoke("Give me today's date in YYYY-MM-DD format. Return only the date.")
)
```

3. Risposta booleana:
```python
bool_response = parser.invoke(
    llm.invoke("Is the sky blue? Answer with true or false only.")
)
```

## Parser Strutturati

### Utilizzo di with_structured_output
```python
llm_with_structure = llm.with_structured_output(PydanticUserInfo)
```
Questo metodo:
- Configura il LLM per produrre output strutturati
- Usa il modello Pydantic per validare e parsare le risposte
- Converte automaticamente il testo in oggetti strutturati

Esempio con UserInfo:
```python
structured_output = llm_with_structure.invoke("My name is John and I live in USA.")
print(structured_output.name)  # Accesso diretto ai campi strutturati
```

### PydanticOutputParser
```python
parser = PydanticOutputParser(pydantic_object=Performer)
```
Parser specializzato per modelli Pydantic che:
- Valida il JSON rispetto al modello
- Converte JSON in oggetti Pydantic
- Fornisce gestione degli errori

## Gestione degli Errori

### Gestione JSON Malformato
```python
misformatted_json = "{'name': 'Tom Hanks', 'film_names': ['Forrest Gump', 'Cast Away']}"
```
Il codice mostra come gestire JSON malformato:
1. Tentativo di parsing diretto
2. Cattura delle eccezioni
3. Utilizzo di OutputFixingParser per correggere errori

### OutputFixingParser
```python
new_parser = OutputFixingParser.from_llm(llm, parser)
```
Questo parser avanzato:
- Tenta di correggere automaticamente JSON malformato
- Utilizza il LLM per "riparare" l'output
- Mantiene la struttura del modello Pydantic

## Best Practices

1. **Validazione dei Dati**
   - Utilizzare modelli Pydantic per validazione automatica
   - Definire tipi e vincoli chiari
   - Fornire valori predefiniti quando possibile

2. **Gestione Errori**
   - Implementare try-except per gestire errori di parsing
   - Utilizzare OutputFixingParser per dati malformati
   - Fornire feedback utili in caso di errore

3. **Strutturazione Output**
   - Preferire output strutturati per dati complessi
   - Usare TypedDict per strutture semplici
   - Utilizzare Pydantic per validazione avanzata

4. **Documentazione**
   - Annotare i campi con descrizioni chiare
   - Specificare valori predefiniti
   - Documentare i tipi di dati attesi