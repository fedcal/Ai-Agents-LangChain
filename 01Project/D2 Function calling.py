"""
This demo explores how to use function calling with OpenAI's chat models while maintaining a memory layer. The system
identifies when to use a tool (function), extracts arguments, executes the tool, and feeds the result back into the
conversation, enabling a full loop of reasoning and tool use.
"""

from typing import List, Dict, Literal
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

class Memory:
    """Memorizza i messaggi scambiati con l'assistente."""

    def __init__(self):
        self._messages: List[Dict[str, str]] = []

    def add_message(self,
                    role: Literal['user', 'system', 'assistant', 'tool'],
                    content: str,
                    tool_calls: list = None,
                    tool_call_id=None) -> None:
        """Aggiunge un messaggio alla memoria."""
        message = {
            "role": role,
            "content": content,
        }
        
        # Aggiungi tool_calls solo se non è None e non è vuoto
        if tool_calls:
            message["tool_calls"] = tool_calls

        if role == "tool":
            message = {
                "role": role,
                "content": content,
                "tool_call_id": tool_call_id,
            }

        self._messages.append(message)

    def get_messages(self) -> List[Dict[str, str]]:
        """Restituisce tutti i messaggi."""
        return self._messages

    def last_message(self) -> Dict:
        """Restituisce l'ultimo messaggio."""
        if self._messages:
            return self._messages[-1]
        return {}

    def reset(self) -> None:
        """Svuota la memoria."""
        self._messages = []


"""
    chat_with_tools è stata creata per:
        - Accettare l'input dell'utente e gli strumenti disponibili.
        - Passare gli strumenti e la memoria al modello.
        - Gestire gli output delle chiamate degli strumenti.
"""
def chat_with_tools(user_question: str = None,
                    memory: Memory = None,
                    model: str = "gpt-4o-mini",
                    temperature: float = 0.0,
                    tools=None):
    """Invia un messaggio all'assistente e gestisce eventuali tool."""
    messages = []
    if memory:
        if user_question:
            memory.add_message(role="user", content=user_question)
        messages = memory.get_messages()
    else:
        messages = [{"role": "user", "content": user_question}]

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message
    
    # Converti tool_calls in formato corretto se presente
    tool_calls_list = None
    if hasattr(message, 'tool_calls') and message.tool_calls:
        tool_calls_list = []
        for call in message.tool_calls:
            tool_calls_list.append({
                "id": call.id,
                "type": call.type,
                "function": {
                    "name": call.function.name,
                    "arguments": call.function.arguments
                }
            })
    
    if memory:
        memory.add_message(role="assistant",
                           content=message.content or "",
                           tool_calls=tool_calls_list)
    return message

def chat_with_tools_loop(user_question: str, memory: Memory, tools: list, model="gpt-4o-mini"):
    # Step 1: manda il messaggio
    message = chat_with_tools(user_question, memory, tools=tools, model=model)

    # Step 2: controlla se il modello vuole usare un tool
    while hasattr(message, 'tool_calls') and message.tool_calls:
        for call in message.tool_calls:
            # Accedi agli attributi dell'oggetto, non come dizionario
            tool_name = call.function.name
            tool_args = json.loads(call.function.arguments)

            print(f"Calling tool: {tool_name} with args: {tool_args}")

            # Esegui il tool
            result = run_tool(tool_name, tool_args)

            print(f"Tool result: {result}")

            # Inserisci il risultato nella memoria come messaggio "tool"
            memory.add_message(
                role="tool",
                content=str(result),
                tool_call_id=call.id
            )

        # Chiedi al modello di generare la risposta finale
        message = chat_with_tools(None, memory, tools=tools, model=model)

    return message



def get_current_weather(location: str) -> str:
    """Restituisce un meteo fittizio per la città richiesta."""
    weather_data = {
        "Rome": "25°C, sunny",
        "London": "15°C, cloudy",
        "New York": "20°C, rainy",
    }
    return weather_data.get(location, "Weather data not found")

# La prima riga rappresenta un'informazione che noi passsiamo al modello per indicare
# cosa fa la funzione
def power(base: float, exponent: float) -> float:
    """Restituisce la base elevata all'esponente."""
    return base ** exponent

""""
    Questa funzione è racchiusa in una descrizione dello strumento schema JSON in modo che il modello possa apprendere 
    informazioni sulla sua esistenza e sui suoi parametri.
"""
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The name of the city"}
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "power",
            "description": "Restituisce la base elevata all'esponente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base": {"type": "number", "description": "The base value"},
                    "exponent": {"type": "number", "description": "The exponent value"}
                },
                "required": ["base", "exponent"],
            },
        },
    }
]



def run_tool(tool_name, tool_args):
    """Esegue il tool richiesto."""
    if tool_name == "get_current_weather":
        return get_current_weather(**tool_args)
    elif tool_name == "power":
        return power(**tool_args)
    else:
        return "Tool not found"

if __name__ == "__main__":
    memory = Memory()
    memory.add_message(
        role="system",
        content="You're a helpful assistant"
    )

    print("=== Test Function Calling ===")
    ai_message = chat_with_tools_loop(
        "What's 2 to the power of -5?",
        memory=memory,
        tools=tools,
        model="gpt-4o-mini"
    )
    
    print(f"\nFinal response: {ai_message.content}")
    
    # Debug: mostra l'ultimo messaggio
    last_msg = memory.last_message()
    if last_msg:
        print(f"\nLast message role: {last_msg.get('role')}")
        print(f"Last message content: {last_msg.get('content')}")

