# LCEL (LangChain Expression Language) Demo

Questo README fornisce una spiegazione dettagliata dello script `D03 LCEL.py`, che dimostra l'utilizzo di LCEL (LangChain Expression Language) per la creazione e composizione di catene di elaborazione in LangChain.

## Indice
1. [Setup e Configurazione](#setup-e-configurazione)
2. [Componenti Base](#componenti-base)
3. [Runnables](#runnables)
4. [Configurazione Avanzata](#configurazione-avanzata)
5. [Composizione dei Runnables](#composizione-dei-runnables)
6. [Esempi di Utilizzo](#esempi-di-utilizzo)

## Setup e Configurazione

### Importazioni Necessarie
```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableParallel
from langchain_core.tracers.context import collect_runs
from dotenv import load_dotenv
```

Ogni importazione ha uno scopo specifico:
- `ChatOpenAI`: Interfaccia con il modello linguistico di OpenAI
- `PromptTemplate`: Gestione dei template per i prompt
- `StrOutputParser`: Parsing delle risposte in formato stringa
- `RunnableSequence, RunnableLambda, RunnableParallel`: Componenti per la composizione di catene
- `collect_runs`: Tracciamento delle esecuzioni
- `load_dotenv`: Caricamento delle variabili d'ambiente

### Configurazione del Modello
```python
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```
- `model_name`: Specifica il modello GPT da utilizzare
- `temperature=0.0`: Imposta la deterministica delle risposte
- `openai_api_key`: Chiave API caricata da variabili d'ambiente

## Componenti Base

### Funzione Helper
```python
def double(x: int) -> int:
    return x * 2
```
Funzione di esempio per dimostrare l'uso di `RunnableLambda`

### Template del Prompt
```python
prompt = PromptTemplate(
    template="Tell me a joke about {topic}.",
    input_variables=["topic"]
)
```
- Definisce un template per generare prompt
- Utilizza variabili di input dinamiche
- Richiede la specifica esplicita delle variabili di input

## Runnables

I "Runnables" sono i componenti base di LCEL. Ogni Runnable ha tre metodi principali:
1. `invoke`: Esecuzione sincrona singola
2. `batch`: Esecuzione in batch
3. `stream`: Esecuzione in streaming

### Tipi di Runnables
```python
runnables = [prompt, llm, parser]
```
Ogni runnable ha caratteristiche specifiche:
- `PromptTemplate`: Formatta il testo del prompt
- `ChatOpenAI`: Interagisce con il modello
- `StrOutputParser`: Processa l'output

## Configurazione Avanzata

### Tracciamento delle Esecuzioni
```python
with collect_runs() as run_collection:
    result = llm.invoke(
        "hello",
        config={
            'run_name': 'demo_run',
            'tags': ['demo', 'lcel'],
            'metadata': {'lesson': 2}
        }
    )
```
Permette di:
- Tracciare le esecuzioni
- Aggiungere metadata
- Taggare le esecuzioni
- Raccogliere statistiche

## Composizione dei Runnables

### Sequenze
```python
chain = RunnableSequence(prompt, llm, parser)
```
Crea una catena sequenziale che:
1. Formatta il prompt
2. Lo invia al modello
3. Processa la risposta

### Esecuzione Parallela
```python
parallel_chain = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    triple=RunnableLambda(lambda x: x * 3)
)
```
Permette di:
- Eseguire operazioni in parallelo
- Combinare risultati multipli
- Processare dati in modo efficiente

## Esempi di Utilizzo

### Invocazione Base
```python
print(parser.invoke(llm.invoke(prompt.format_prompt(topic="cats"))))
```
Dimostra l'uso base dei componenti:
1. Formattazione del prompt
2. Invio al modello
3. Parsing della risposta

### Streaming
```python
for chunk in chain.stream({"topic": "birds"}):
    print(chunk, end="", flush=True)
```
Utile per:
- Risposte in tempo reale
- Processamento incrementale
- Feedback immediato

### Batch Processing
```python
print(chain.batch([
    {"topic": "elephants"},
    {"topic": "giraffes"},
    {"topic": "lions"},
]))
```
Permette di:
- Processare multiple richieste
- Ottimizzare le performance
- Gestire set di dati

## Best Practices

1. **Gestione delle Risorse**
   - Utilizzare `load_dotenv()` per le configurazioni
   - Gestire appropriatamente le chiavi API
   - Chiudere correttamente le risorse

2. **Composizione**
   - Preferire la composizione di componenti piccoli
   - Utilizzare `RunnableSequence` per operazioni sequenziali
   - Sfruttare `RunnableParallel` per operazioni indipendenti

3. **Error Handling**
   - Implementare gestione degli errori appropriata
   - Utilizzare try-except dove necessario
   - Validare input e output

4. **Performance**
   - Utilizzare batch processing per multiple richieste
   - Sfruttare lo streaming per risposte immediate
   - Ottimizzare la configurazione del modello

## Conclusione

LCEL fornisce un framework potente e flessibile per:
- Costruire pipeline di elaborazione complesse
- Comporre componenti in modo modulare
- Gestire efficacemente l'interazione con i modelli linguistici
- Tracciare e monitorare le esecuzioni

Lo script dimostra l'uso pratico di questi concetti in un contesto reale.