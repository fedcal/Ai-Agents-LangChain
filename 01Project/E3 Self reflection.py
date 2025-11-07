### Scenario

# Immagina di lavorare su un chatbot basato sull'intelligenza artificiale che deve fornire risposte raffinate e di alta qualità agli utenti di un sistema di assistenza clienti. A volte, le risposte generate dall'intelligenza artificiale potrebbero mancare di contesto o di chiarezza.

# Il tuo compito è aggiornare il tuo agente:

# - Permettendogli di riflettere sulle sue risposte prima di fornirle.
# - Permettendo un perfezionamento iterativo per migliorare la qualità delle risposte.
# - Tenendo traccia delle conversazioni per una migliore consapevolezza del contesto.

# Alla fine di questo esercizio, avrai un agente basato sull'intelligenza artificiale che impara da sé stesso, identifica gli errori e migliora iterativamente le sue risposte.

### Sfida

# In questo esercizio, ti verrà chiesto di aggiornare la classe Agente esistente aggiungendo:

# 1. Un livello di memoria per tenere traccia delle interazioni precedenti.
# 2. Un meccanismo di autoriflessione che critica e perfeziona le risposte.

# Il tuo agente dovrebbe:

# - Memorizzare la cronologia delle conversazioni per un migliore processo decisionale.
# - Criticare le proprie risposte utilizzando un feedback strutturato.
# - Perfezionare i propri output in modo iterativo, seguendo regole predefinite.

# In questo esercizio, migliorerai l'agente AI con funzionalità di autoriflessione, consentendogli di criticare le proprie risposte e perfezionarle iterativamente. Questa funzionalità consente all'agente di valutare il proprio output e migliorare la qualità della risposta prima di fornire una risposta definitiva.

# **Obiettivo**

# Il tuo compito è modificare l'agente in modo che possa:

# - Memorizzare la cronologia delle conversazioni – Implementare un meccanismo di memoria per tracciare le interazioni.
# - Generare una risposta iniziale – Elaborare l'input dell'utente e restituire una risposta utilizzando il modello linguistico.
# - Criticare la propria risposta quando abilitata – Se l'autoriflessione è attivata, l'agente dovrebbe generare un feedback sulla propria risposta.
# - Perfezionare la propria risposta iterativamente – Sulla base dell'autocritica, l'agente dovrebbe adattare la propria risposta, migliorandone chiarezza, accuratezza e pertinenza.

# **Passaggi**

# - Implementare un livello di memoria per conservare la cronologia delle conversazioni.
# - Introdurre un meccanismo di autoriflessione che consenta all'agente di analizzare la propria risposta e perfezionarla. - Limitare il numero di iterazioni di auto-riflessione per evitare loop eccessivi (minimo 1, massimo 3).
# - Garantire flessibilità consentendo agli utenti di attivare o disattivare l'auto-riflessione.

# **Considerazioni**

# - L'agente dovrebbe sempre generare almeno una risposta prima dell'auto-riflessione.
# - Se l'auto-riflessione è abilitata, dovrebbe essere eseguita almeno un'altra volta per analizzare e migliorare il suo output.
# - Il numero di iterazioni dovrebbe essere controllato e non superare i tre perfezionamenti.
# - Implementare la funzionalità di registrazione (modalità dettagliata) per tracciare il processo di perfezionamento.

# **Invoke**

# Rifattorizzare il metodo `invoke()`. Questo metodo ora dovrebbe includere:
# - parametro self_reflection (predefinito: False);
# - parametro max_iter (predefinito: 1);

# Se self_reflection è impostato su True, dovrebbe utilizzare un loop per generare una risposta iniziale. Quindi, criticare e perfezionare la risposta nelle iterazioni successive fino al numero di iterazioni definito in max_iter.

# Utilizzare self.memory per memorizzare ogni passaggio.

# Regole per l'auto-riflessione:

# - Non consentire valori inferiori a 1
# - Non consentire valori superiori a 3
# - Max iter è controllato dal flag self_reflection.
# - Se impostato su true, deve chiamare l'LLM almeno un'altra volta per la critica.

# Il prompt di auto-critica dovrebbe iniziare con qualcosa del tipo: `Rifletti sulla tua risposta precedente`.
# Estendilo per assicurarti che identifichi gli errori e fornisca una versione rivista.

import json
import os
from typing import List, Dict, Literal
from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from dotenv import load_dotenv

load_dotenv()

SELF_CRITIQUE_PROMPT = """
Reflect on your previous response...
Identify any mistakes, areas for improvement, or ways to clarify the answer, making it more concise. 
Provide a revised response if necessary in a Json Output structure:
{
    "original_response": "",
    "revisions_needed": "",
    "updated_response": ""
}
"""

class Memory:
    def __init__(self):
        self._messages: List[Dict[str, str]] = []

    def add_message(self, role: Literal['user', 'system', 'assistant'], content: str):
        self._messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self) -> List[Dict[str, str]]:
        return self._messages

    def last_message(self) -> None:
        if self._messages:
            return self._messages[-1]


class Agent:
    """A self-reflection AI Agent"""

    def __init__(
            self,
            name: str = "Agent",
            role: str = "Personal Assistant",
            instructions: str = "Help users with any question",
            model: str = "gpt-4o-mini",
            temperature: float = 0.0,
            critique_prompt: str = SELF_CRITIQUE_PROMPT
    ):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.model = model
        self.temperature = temperature

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.memory = Memory()
        self.memory.add_message(
            role="system",
            content=f"You're an AI Agent, your role is {self.role}, "
                    f"and you need to {self.instructions}",
        )

        self.critique_prompt = critique_prompt

    def invoke(self,
               user_message: str,
               self_reflection: bool = False,
               max_iter: int = 1,
               verbose: bool = False) -> str:

        # Rules
        # - Non consentire valori inferiori a 1
        # - Non consentire valori superiori a 3
        # - Il valore massimo dell'iter è controllato dal flag self_reflection.
        # - Se impostato su true, è necessario chiamare l'LLM almeno un'altra volta per la critica

        self.memory.add_message(
            role="user",
            content=user_message
        )
        if verbose:
            self._log_last_message()

        max_iter = max_iter if max_iter >= 1 else 1
        max_iter = max_iter if max_iter <= 3 else 3
        max_iter = max_iter if self_reflection else 0.5
        loops = 2 * max_iter

        for i in range(loops):
            ai_message = self._get_completion(
                messages=self.memory.get_messages()
            )

            self.memory.add_message(
                role="assistant",
                content=ai_message.content,
            )
            """"if verbose:
                self._log_last_message()"""

            if i < loops - 1:
                self.memory.add_message(
                    role="user",
                    content=self.critique_prompt
                )
                """"if verbose:
                    self._log_last_message()"""

                ai_message = self._get_completion(
                    messages=self.memory.get_messages()
                )

    def _get_completion(self, messages: List[Dict]) -> ChatCompletionMessage:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages
        )

        return response.choices[0].message

    def _log_last_message(self):
        print(f"### {self.memory.last_message()['role']} message ###\n".upper())
        print(f"{self.memory.last_message()['content']} \n")
        print("\n________________________________________________________________\n")

if __name__ == '__main__':
    '''client = OpenAI(
        api_key = os.getenv("OPENAI_API_KEY")
    )

    ## SENZA MEMORY LAYER, IMPOSTATO MANUALMENTE
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer all user questions"},
            {"role": "user", "content": "What have I asked?"},
        ],
        temperature=0.0,
    )
    response.choices[0].message.content

    memory = [
        {"role": "system", "content": "Answer all user questions"},
        {"role": "user", "content": "What's an API"},
    ]

    new_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=memory,
        temperature=0.0,
    )

    memory.append(
        {"role": "assistant", "content": new_response.choices[0].message.content}
    )

    print("[1] Memory", memory)

    memory.append(
        {"role": "user", "content": "What have I asked?"}
    )

    print("[2] Memory", memory)

    new_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=memory,
        temperature=0.0,
    )

    memory.append(
        {"role": "assistant", "content": new_response.choices[0].message.content}
    )

    print("[3] Memory", memory)'''

    ### Con Layer
    agente = Agent()

    agente.invoke("Ciao, come va?",True,2,True)
    print(agente.memory.last_message())