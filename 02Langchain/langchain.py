from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

if __name__ == '__main__':
    """
    # Esempio 1: Invocazione semplice con una stringa
    # Il modello riceve direttamente il testo come input
    print("=== Esempio 1: Invocazione semplice ===")
    print(llm.invoke("Hello, world!").content)
    
    print("\n" + "="*50 + "\n")
    
    # Esempio 2: Invocazione con messaggi strutturati
    # Questo approccio permette di definire ruoli specifici nella conversazione
    messages = [
        SystemMessage("You are a helpful assistant."),  # Messaggio di sistema: definisce il ruolo dell'AI
        HumanMessage("Hello, world!")  # Messaggio umano: la richiesta dell'utente
    ]

    print("=== Esempio 2: Invocazione con messaggi strutturati ===")
    print(llm.invoke(messages).content)

    print("\n" + "="*50 + "\n")

    messages = [
        SystemMessage("You are a helpful assistant."),
        HumanMessage("Hello, world!"),
        AIMessage("Hello! How can I assist you today?"), # Messaggio AI: risposta generata
        HumanMessage("Can you tell me a joke?"),
    ]

    print("=== Esempio 3: Invocazione con messaggi strutturati e AI ===")
    print(llm.invoke(messages).content)

    print("\n" + "="*50 + "\n")

    topic = "Python programming"
    prompt = f"tell me an interesting fact about {topic}."
    print("=== Esempio 4: Invocazione con prompt dinamico ===")
    print(llm.invoke(prompt).content)

    print("\n" + "="*50 + "\n")

    prompt = "tell me an interesting fact about {topic}."
    print("=== Esempio 5: Invocazione con prompt dinamico ===")
    print(llm.invoke(prompt.format(topic="Java")).content)

    # Prompt template
    prompt_template = PromptTemplate(
        template="Tell me a fun fact about {topic}."
    )

    print("=== Esempio 6: Invocazione con PromptTemplate ===")
    print("PROMPT VARIABLE", prompt_template)
    prompt_template.format(topic="Space Exploration")
    print("PROMPT INVOKE",prompt_template.invoke({"topic": "Space Exploration"}))
    print(llm.invoke(prompt_template.invoke({"topic": "Space Exploration"})).content)"""

    example_prompt = PromptTemplate(
        template="Question: {input}\nThought: {thought}\nRespoonse:{output}"
    )

    examples = [
        {"input": "What is the capital of France?", "thought": "I need to recall the capital city of France.", "output": "The capital of France is Paris."},
        {"input": "Who wrote '1984'?", "thought": "I need to remember the author of the book '1984'.", "output": "George Orwell wrote '1984'."}
    ]

    print("=== Esempio 7: Invocazione con FewShotPromptTemplate ===")
    print(example_prompt.invoke(examples[0]).to_string())

    prompt_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="Here are some examples of questions and answers:",
        suffix="Now, answer the following question:\nQuestion: {input}\nThought:",
        input_variables=["input"]
    )
    response = llm.invoke(prompt_template.invoke({"input": "What is the largest planet in our solar system?"}))
    print(response.content)

