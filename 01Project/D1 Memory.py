# Aggiunta del layer Memory all'agente

from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Literal
import os

class Memory:
    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: Literal['user', 'system', 'assistant'], content: str):
        self.messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages

# 1. Aggiunge il messaggio alla memoria
# 2. Chiama l'LLM con la lista dei messaggi presenti in memoria
# 3. Aggiunge la risposta dell' LLM nella memoria
# 4. Restituisce il messaggio dell'assistente
def chat(user_message: str = None, memory: Memory = None) -> str:
    messages = [{"role": "user", "content": user_message}]
    if memory:
        if user_message:
            memory.add_message(role="user", content=user_message)
        messages = memory.get_messages()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=messages,
    )

    ai_message = response.choices[0].message.content
    if memory:
        memory.add_message(role="assistant", content=ai_message)

    return ai_message


if __name__ == '__main__':
    # Carica le variabili d'ambiente e inizializza il client OpenAI
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Esempio 1: chat senza memoria
    user_message = "What have I asked before?"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer all user questions"},
            {"role": "user", "content": user_message},
        ],
        temperature=0.0,
    )
    print("Risposta senza memoria:", response.choices[0].message.content)

    # Esempio 2: chat con memoria manuale
    memory = [
        {"role": "system", "content": "Answer all user questions"},
        {"role": "user", "content": "What's an API?"},
    ]

    new_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=memory,
        temperature=0.0,
    )
    memory.append({"role": "assistant", "content": new_response.choices[0].message.content})
    memory.append({"role": "user", "content": "What have I asked?"})

    new_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=memory,
        temperature=0.0,
    )
    memory.append({"role": "assistant", "content": new_response.choices[0].message.content})
    print("Memoria manuale:", memory)

    # Esempio 3: uso della classe Memory
    memory_obj = Memory()
    memory_obj.add_message(role="system", content="You're a helpful assistant")

    print("Messaggi iniziali in memoria:", memory_obj.get_messages())

    print("\nChat senza memoria persistente:")
    print(chat(user_message="what's the capital of Brazil"))

    print("\nChat con memoria persistente:")
    print(chat(user_message="what's the capital of Brazil", memory=memory_obj))
    print(chat(user_message="what have I asked?", memory=memory_obj))

    print("\nStato finale della memoria:")
    print(memory_obj.get_messages())