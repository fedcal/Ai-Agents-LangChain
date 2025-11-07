"""
Welcome to your Chatbot Building Exercise! In this challenge, you’ll create a chatbot that remembers past interactions, follows a structured conversation flow, and provides more human-like responses using Few-Shot Prompting.

By leveraging memory, structured prompts, and few-shot examples, your chatbot will behave in a consistent and engaging manner.

Scenario
You're developing a virtual assistant for a company. Your chatbot needs to:

- Maintain conversation history.

- Respond consistently using predefined few-shot examples.

- Be customizable for different roles, such as:

    - A robotic assistant with a sci-fi tone.

    - A casual chatbot for fun interactions.

    - A professional AI assistant for business tasks.

At the end of this exercise, you’ll have a fully functional chatbot that can chat dynamically while following a predefined personality.

Challenge
Your chatbot must:

- Track conversation history.

- Use a structured Few-Shot Prompting approach.

- Allow customization of tone and personality.
"""

import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
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
                 name: str,
                 instructions: str,
                 examples: List[dict],
                 model:str="gpt-4o-mini",
                 temperature:float=0.0):
        self.name = name
        self.llm = ChatOpenAI(
            model_name=model,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )

        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",instructions),
                ("human","{input}"),
                ("ai","{output}"),
            ]
        )

        prompt_template = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=examples,
        )

        #Memory
        self.messages = prompt_template.invoke({}).to_messages()

    def invoke(self, user_user_message: str) -> AIMessage:
        self.messages.append(HumanMessage(user_user_message))
        ai_message = self.llm.invoke(self.messages)
        self.messages.append(ai_message)
        return ai_message

if __name__ == '__main__':
    instructions = (
        "You are a friendly and helpful virtual assistant. "
        "Respond to user queries in a polite and informative manner."
        "You are an expert in providing information about technology and programming."
    )

    examples = [
        {
            "input": "Hello! How are you today?",
            "output": "Hello there! I'm doing wonderful, thank you for asking! I'm here and ready to help you with any technology or programming questions you might have. How can I assist you today?"
        },
        {
            "input": "What is Python?",
            "output": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used for web development, data science, artificial intelligence, automation, and more. Python's syntax is clean and easy to learn, making it an excellent choice for beginners and experienced developers alike."
        },
        {
            "input": "Can you help me with JavaScript?",
            "output": "Absolutely! I'd be happy to help you with JavaScript. JavaScript is a versatile programming language primarily used for web development to create interactive and dynamic websites. Whether you need help with syntax, concepts, frameworks, or debugging, just let me know what specific aspect you'd like assistance with!"
        },
        {
            "input": "What's the difference between HTML and CSS?",
            "output": "Great question! HTML (HyperText Markup Language) is the structure and content of a webpage - it defines what elements appear on the page like headings, paragraphs, and images. CSS (Cascading Style Sheets) is responsible for the visual presentation - it controls how those HTML elements look, including colors, fonts, layouts, and spacing. Think of HTML as the skeleton and CSS as the styling that makes it look beautiful!"
        },
        {
            "input": "I'm feeling frustrated with coding",
            "output": "I completely understand that feeling! Coding can be challenging, and frustration is a natural part of the learning process. Remember that every experienced programmer has been where you are now. Take a short break, try breaking the problem into smaller steps, and don't hesitate to ask for help. You're making progress even when it doesn't feel like it. What specific issue are you working on? I'm here to help you through it!"
        },
        {
            "input": "Thank you for your help!",
            "output": "You're absolutely welcome! I'm so glad I could help you today. Remember, I'm always here whenever you need assistance with technology, programming, or any other questions. Don't hesitate to reach out anytime. Have a fantastic day and happy coding!"
        }
    ]

    chatbot = ChatBot(
        name="TechHelper",
        instructions=instructions,
        examples=examples,
        model="gpt-4o-mini",
        temperature=0.0
    )

    print(chatbot.invoke("Hi there! Can you tell me a fun fact about programming?").content)
    print("\n" + "="*50 + "\n")
    print(chatbot.messages)

