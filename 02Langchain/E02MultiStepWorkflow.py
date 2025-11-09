"""
Welcome to your next challenge in mastering LangChain’s Language Chain Expression Language (LCEL)! 🎯

In this exercise, you’ll build a multi-step workflow using LCEL to solve a more complex task than simply generating a joke. 
We’ll walk through the entire process, from planning a task, to using multiple prompts and chaining steps together.

By the end of this exercise, you’ll have built a workflow that generates a business idea, analyzes it, and presents 
the results in a structured, easy-to-understand format.

Scenario
You’ve been hired by a startup incubator to build an AI-powered assistant that helps aspiring entrepreneurs brainstorm 
business ideas, evaluate their potential, and summarize key insights.

Challenge
Create an AI Business Advisor that:
    - Accepts an industry as input.
    - Generates a business idea.
    - Analyzes the strengths and weaknesses.
    - Formats the results as a final report.

Use LangChain LCEL to chain prompts, LLMs, and output parsers.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

if __name__ == '__main__':
    logs = []
    parser = StrOutputParser()

    parse_and_log_output_chain = RunnableParallel(
        output=parser,
        log=RunnableLambda(lambda x: logs.append(x))
    )

    # Creazione della chain per creare l'idea di business
    idea_prompt = PromptTemplate.from_template(
        template="You are  a creative innovative business idea in the industry: "
        "{industry}. "
        "Provide a concise business idea." 
    )

    idea_chain = (
        idea_prompt
        | llm
        | parse_and_log_output_chain
    )

    idea_result = idea_chain.invoke({"industry": "agro"}) 
    print(idea_result)

    print("\n=== Log ===")
    for message in logs:
        print(f"\n[LOG] {message}")
    
    # Chain per analizzare l'idea di business
    analysis_prompt = PromptTemplate.from_template(
        template=("Analyze the following business idea: '{idea}'. Identify 3 key strengths amd 3 potential weaknesses.")
    )

    analysis_chain = (
        analysis_prompt
        | llm
        | parse_and_log_output_chain
    )

    idea_analysis = analysis_chain.invoke({"idea": idea_result["output"]})
    print("\n=== Idea Analysis ===")
    print(idea_analysis["output"])

    print("\n=== Log ===")
    for message in logs:
        print(f"\n[LOG] {message}")
    
    # Chain per report generation



