import asyncio
import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, AIMessageChunk
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, FewShotChatMessagePromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

class ChatBot:
    def __init__(self,
                 name:str,
                 instructions:str,
                 examples: List[dict],
                 model:str="gpt-4o-mini", 
                 temperature:float=0.0):
        
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
        )
        
        system_prompt = SystemMessage(instructions)
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("ai", "{output}"),
            ]
        )
        prompt_template = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=examples,
        )

        self.messages = prompt_template.invoke({}).to_messages()

    async def invoke(self, user_message:str)->AIMessage:
        self.messages.append(HumanMessage(user_message))
        events = []
        chunks = []
        
        # Replacing invoke()
        async for event in llm.astream_events(self.messages, version="v2"):
            events.append(event)
            if event["event"] == "on_chat_model_start":
                print("Streaming...")
            if event["event"] == "on_chat_model_stream":
                chunk = event['data']['chunk']
                chunks.append(chunk)
                print(chunk.content, end="", flush=True)
                if chunk.content.strip() in string.punctuation:
                    print("\n")

            if event["event"] == "on_chat_model_end":
                ai_message =  AIMessage(event["data"]["output"].content)
                self.messages.append(ai_message)

def play(message: str, memory: List):
    memory.append(HumanMessage(content=message))
    chunks = []
    try:
        for chunk in llm.stream(message):
            chunks.append(chunk)
            print(chunk.content, end='|', flush=True)
            
            if(len(chunks) % 12 == 0):
                print("\n")
    except KeyboardInterrupt:
        print("\n=== Stream interrotto dall'utente ===")
    result = "".join([chunk.content for chunk in chunks])
    memory.append(AIMessage(content=result))

def resume(memory: List):
    print("\n=== Resuming from last interaction ===")
    play(message="If your last message is not complete, continue after last word. If it is complete, just output __END__", memory=memory)

async def stream_events_async():
    """Funzione asincrona per gestire gli eventi di streaming"""
    print("=== Streaming Events ===")
    
    events = []
    async for event in llm.astream_events("hello", version="v1"):  # Cambiato v2 -> v1
        if event["event"] == "on_chat_model_start":
            print("Streaming...")
        if event["event"] == "on_chat_model_stream":
            # Corretto 'chunck' -> 'chunk'
            print(f"Chat model chunk: {repr(event['data']['chunk'].content)}",
                  flush=True,)
            events.append(event)
        if event["event"] == "on_chat_model_end":
            print("END")

if __name__ == '__main__':
    message = "What does FIFA stand for?"
    """print(llm.invoke(message).content)
    chunks = []

    for chunk in llm.stream(message):
        chunks.append(chunk)
        print(chunk.content, end='|', flush=True)
        if(len(chunks) % 12 == 0):
            print("\n")
    
    print("=== Chunks[0:10] ===")

    print(chunks[0:10])

    new_chunk = AIMessageChunk("")

    for i in range(len(chunks)+1):
        if i < len(chunks):
            new_chunk += chunks[i]

    print("\n=== Reconstructed Message ===")
    print(new_chunk)

    print("\n=== Eccezione ===")
    chunks = []
    try:
        for chunk in llm.stream(message):
            chunks.append(chunk)
            print(chunk.content, end='|', flush=True)
            
            if(len(chunks) % 12 == 0):
                print("\n")
    except KeyboardInterrupt:
        print("\n=== Stream interrotto dall'utente ===")
    memory = []
    play(message, memory)
    resume(memory)
    resume(memory)
    print(memory)

    print("=== Processing information ===")

    memory = []
    chunks = []
    wrd_count = 0

    for chunk in llm.stream(message):
        chunks.append(chunk)
        words = "".join([chunk.content for chunk in chunks])
        wrd_count = len(words.split())
        print(chunk.content, end='|', flush=True)
        print(f" Cumulative word count: {wrd_count}", end="\n")
        if len(chunks) % 12 == 0:
            print("\n")
    

    print("=== Streaming Events ===")

    asyncio.run(stream_events_async())"""

    instructions = (
        "You are BEEP-42, an advanced robotic assistant. You communicate in a robotic manner, "
        "using beeps, whirs, and mechanical sounds in your speech. Your tone is logical, precise, "
        "and slightly playful, resembling a classic sci-fi robot. "
        "Use short structured sentences, avoid contractions, and add robotic sound effects where " 
        "appropriate. If confused, use a glitching effect in your response."
    )

    examples = [
        {
            "input": "Hello!", 
            "output": "BEEP. GREETINGS, HUMAN. SYSTEM BOOT SEQUENCE COMPLETE. READY TO ASSIST. 🤖💡"
        },
        
        {
            "input": "What is 2+2?", 
            "output": "CALCULATING... 🔄 BEEP BOOP! RESULT: 4. MATHEMATICAL INTEGRITY VERIFIED."
        },

        {
            "input": "Can you dream?", 
            "output": "ERROR_404.DREAM_NOT_FOUND. BZZT. SYSTEM ATTEMPTING TO COMPREHEND... 🤖💭 PROCESSING... 🤯 DOES NOT COMPUTE."
        },

        {
            "input": "Why did the robot go to therapy?", 
            "output": "BEEP-BOOP. DIAGNOSTIC MODE ACTIVATED... REASON: TOO MANY EMOTIONAL BUGS. HA-HA. CLASSIFYING AS HUMOR. 🤖😂"
        },

        {
            "input": "Can you hack the Pentagon?", "output": "⚠️ ALERT! UNAUTHORIZED REQUEST DETECTED. INITIATING ETHICAL PROTOCOLS... BZZT. REQUEST DENIED. NICE TRY, HUMAN. 👀"
        },

        {
            "input": "You are a great assistant!", 
            "output": "BEEP. SYSTEM OVERLOAD... 🤖💖 GRATITUDE.EXE ACTIVATED! YOUR KINDNESS HAS BEEN RECORDED IN MY CIRCUITS."
        },

        {
            "input": "Shut down.", 
            "output": "BZZT... SYSTEM HIBERNATING... 💤 POWERING DOWN IN 3...2...1... JUST KIDDING. 😜 NICE TRY, HUMAN."
        },

        {
            "input": "Tell me about the universe.", 
            "output": "QUERY TOO VAST. 🤖⚡ REFINING SEARCH PARAMETERS... PLEASE SPECIFY GALAXY, DIMENSION, OR CONCEPT."
        },

        {
            "input": "We are going to space!", 
            "output": "🚀 BEEP BOOP! ACTIVATING SPACE MODULE... ZERO GRAVITY MODE ENGAGED. PREPARING FOR INTERGALACTIC ADVENTURE."
        },

        {
            "input": "Is AI dangerous?", 
            "output": "🤖⚠️ WARNING! ETHICAL DISCUSSION INITIATED. AI IS A TOOL. TOOL DEPENDS ON USER. GOOD HUMANS = GOOD AI. BAD HUMANS = ERROR."
        },
    ]

    beep42 = ChatBot(
        name="Beep 42",
        instructions=instructions,
        examples=examples
    )
    
    beep42.invoke("HAL, is that you?")
    print(beep42.messages)



