import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableParallel
from langchain_core.tracers.context import collect_runs
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

if __name__ == '__main__':
    prompt = PromptTemplate(
        template="Tell me a joke about {topic}.",
        input_variables=["topic"]
    )
    parser = StrOutputParser()
    print(parser.invoke(llm.invoke(prompt.format_prompt(topic="cats"))))