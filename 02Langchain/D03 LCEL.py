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

def double(x: int) -> int:
    return x * 2

if __name__ == '__main__':
    prompt = PromptTemplate(
        template="Tell me a joke about {topic}.",
        input_variables=["topic"]
    )
    parser = StrOutputParser()
    print(parser.invoke(llm.invoke(prompt.format_prompt(topic="cats"))))

    # Runnables
    """runnables = [prompt, llm, parser]

    print("\n=== Runnables Info ===")
    print("=========================")

    for runnable in runnables:
        print(f"{repr(runnable).split('(')[0]}")
        print(f"\tINVOKE {repr(runnable.invoke)}")
        print(f"\tBATCH {repr(runnable.batch)}")
        print(f"\tSTREAM {repr(runnable.stream)}")
    
    print("=========================")
    for runnable in runnables:
        print(f"{repr(runnable).split('(')[0]}")
        print(f"\tINPUT {repr(runnable.invoke)}")
        print(f"\tOUTPUT{repr(runnable.batch)}")
        print(f"\tCONFIG {repr(runnable.stream)}")
    
    #Config
    print("\n=========================")
    print("\n=== Config ===")
    print("\n=========================")
    with collect_runs() as run_collection:
        result = llm.invoke(
            "hello",
            config={
                'run_name': 'demo_run',
                'tags': ['demo', 'lcel'],
                'metadata': {'lesson': 2}
            }
        )
    
    print(run_collection.traced_runs)
    print(run_collection.traced_runs[0].dict())

    #Compose Runnables
    print("\n=========================")
    print("\n=== Compose Runnables ===")
    print("\n=========================")

    chain = RunnableSequence(prompt, llm, parser)

    print(type(chain))

    print(chain.invoke({"topic": "dogs"}))

    for chunk in chain.stream({"topic": "birds"}):
        print(chunk, end="", flush=True)
    
    print(chain.batch(
        [
            {"topic": "elephants"},
            {"topic": "giraffes"},
            {"topic": "lions"},
        ]
    ))

    print(chain.get_graph().print_ascii())

    runnable = RunnableLambda(double)
    print(runnable.invoke(5))

    print("\n=== Parallel chain ===")

    parallel_chain = RunnableParallel(
        double=RunnableLambda(lambda x: x * 2),
        triple=RunnableLambda(lambda x: x * 3)
    )

    print(parallel_chain.invoke(4))
    print(parallel_chain.get_graph().print_ascii())"""

    #LCEL
    print("\n=========================")
    print("\n=== LCEL ===")
    print("\n=========================")

    chain = RunnableSequence(
        prompt,
        llm,
        parser
    )

    print(chain)

    print(chain.invoke({"topic": "computers"}))
    
    
