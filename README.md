# AI Agents with LangChain and LangGraph

This repository contains my coursework and projects for the **AI Agents with LangChain and LangGraph** course from Udacity. This comprehensive course teaches how to build intelligent AI agents using modern frameworks and tools for real-world applications.

## 🎯 Course Overview

The AI Agents with LangChain and LangGraph course is designed to take students from basic AI concepts to building sophisticated, production-ready AI agents. The course emphasizes practical implementation and real-world problem-solving using cutting-edge frameworks.

### 🧠 What You'll Learn

**Core Concepts:**
- **Agent Architecture & Design Patterns**: Understanding the fundamental building blocks of AI agents, including reasoning engines, memory systems, and action execution
- **LangChain Ecosystem**: Deep dive into the LangChain framework for building language model applications with components like chains, prompts, and output parsers
- **LangGraph State Management**: Creating complex, stateful agent workflows with graph-based architectures for multi-step reasoning
- **Memory & Persistence**: Implementing various memory mechanisms including short-term, long-term, and semantic memory for context retention
- **Tool Integration & Function Calling**: Connecting agents with external APIs, databases, and services for expanded capabilities
- **Self-Reflection & Improvement**: Building agents capable of critiquing, analyzing, and iteratively improving their own responses
- **Multi-Agent Coordination**: Orchestrating multiple specialized agents to work together on complex, distributed tasks

**Advanced Topics:**
- **Agent Communication Protocols**: Designing effective inter-agent communication patterns
- **Error Handling & Recovery**: Building robust agents that can handle failures gracefully
- **Performance Optimization**: Techniques for scaling and optimizing agent performance
- **Ethical AI & Safety**: Implementing guardrails and safety mechanisms in autonomous agents

## 📁 Repository Structure

```
AiAgentsWithLangChainAndLangGraph/
├── 01Project/                    # Core AI Agent Implementation
│   ├── D1 Memory.py             # Memory layer with conversation tracking
│   ├── D2 Function calling.py   # External function integration
│   ├── E1 Simple Call.py        # Basic agent invocation patterns
│   ├── E2 Agent Creation.py     # Agent instantiation and configuration
│   ├── E3 Self reflection.py    # Self-reflective agent with improvement loops
│   └── .env                     # Environment configuration
│
├── 02Langchain/                 # LangChain Framework Deep Dive
│   ├── langchain.py             # Comprehensive LangChain examples
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment configuration
│
├── 03LangGraph/                 # LangGraph Advanced Workflows (Coming Soon)
│   ├── state_machines.py       # State-based agent workflows
│   ├── graph_agents.py          # Graph-based reasoning agents
│   └── multi_agent_systems.py  # Coordinated multi-agent implementations
│
└── README.md                    # This file
```

## 🚀 Projects and Implementations

### Project 1: Foundational AI Agent Development
**Location**: `01Project/`

This section focuses on building the core components of intelligent AI agents:

#### **D1 Memory.py** - Advanced Memory Systems
- **Conversation Tracking**: Maintains full conversation history with context awareness
- **Memory Types**: Implements episodic (conversation-specific) and semantic (knowledge-based) memory
- **Context Management**: Intelligent context window management for optimal performance
- **Memory Retrieval**: Efficient algorithms for relevant memory retrieval based on current context

#### **D2 Function calling.py** - External Tool Integration
- **API Integration**: Seamless connection with external APIs and services
- **Function Registry**: Dynamic function registration and discovery system
- **Parameter Validation**: Automatic validation and type checking for function calls
- **Error Handling**: Robust error handling and fallback mechanisms

#### **E1 Simple Call.py** - Basic Agent Operations
- **Simple Invocation**: Direct model invocation with various input types
- **Response Handling**: Processing and formatting model responses
- **Basic Configurations**: Temperature, model selection, and parameter tuning

#### **E2 Agent Creation.py** - Agent Architecture
- **Agent Instantiation**: Creating and configuring AI agents with specific capabilities
- **Role Definition**: Defining agent roles, personalities, and specialized functions
- **Capability Management**: Adding and managing agent capabilities dynamically

#### **E3 Self reflection.py** - Autonomous Improvement
```python
# Key Features:
- Self-Critique System: Agents analyze their own responses for quality and accuracy
- Iterative Refinement: Configurable improvement cycles (1-3 iterations)
- Quality Metrics: Automatic evaluation of response quality and relevance
- Learning Integration: Incorporation of feedback into future responses
```

### Project 2: LangChain Framework Mastery
**Location**: `02Langchain/`

#### **langchain.py** - Comprehensive LangChain Implementation
- **Prompt Engineering**: Advanced prompt template creation and management
- **Message Handling**: Sophisticated message type management (System, Human, AI)
- **Chain Building**: Creating complex chains for multi-step reasoning
- **Few-Shot Learning**: Implementation of few-shot prompting techniques

**Key Examples Implemented:**
```python
# 1. Simple String Invocation
llm.invoke("Hello, world!")

# 2. Structured Message Conversation
messages = [
    SystemMessage("You are a helpful assistant."),
    HumanMessage("Hello, world!"),
    AIMessage("Hello! How can I assist you today?"),
    HumanMessage("Can you tell me a joke?")
]

# 3. Dynamic Prompt Templates
prompt_template = PromptTemplate(
    template="Tell me a fun fact about {topic}."
)

# 4. Few-Shot Learning Examples
examples = [
    {"input": "What is the capital of France?", 
     "thought": "I need to recall the capital city of France.", 
     "output": "The capital of France is Paris."}
]
```

### Project 3: LangGraph Advanced Workflows (In Development)
**Location**: `03LangGraph/` (Coming Soon)

This section will cover advanced agent orchestration using LangGraph:

- **State Machines**: Complex state-based agent workflows
- **Graph Reasoning**: Multi-step reasoning with graph-based architectures
- **Conditional Logic**: Dynamic decision-making based on context and conditions
- **Parallel Processing**: Concurrent agent operations for improved performance

## 🛠 Technical Implementation Details

### Memory Architecture
The memory system implements a multi-layered approach:

```python
class Memory:
    def __init__(self):
        self.conversations = []  # Episodic memory
        self.knowledge_base = {} # Semantic memory
        self.context_window = 4096  # Token management
    
    def add_conversation(self, role, content):
        # Add to conversation history with metadata
        
    def retrieve_context(self, query):
        # Intelligent context retrieval
```

### Self-Reflection Mechanism
The self-reflection system uses a multi-stage approach:

1. **Initial Response Generation**: Agent provides initial answer
2. **Self-Critique**: Agent analyzes its own response for quality
3. **Improvement Identification**: Identifies specific areas for enhancement
4. **Iterative Refinement**: Generates improved responses (1-3 cycles)
5. **Final Output**: Delivers the best refined response

### LangChain Integration Patterns
- **Template-Based Prompting**: Reusable prompt templates with variable substitution
- **Chain Composition**: Building complex workflows through chain composition
- **Output Parsing**: Structured output parsing and validation
- **Memory Integration**: Seamless integration with conversation memory

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API Key
- Basic understanding of Python and AI concepts

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AiAgentsWithLangChainAndLangGraph.git
   cd AiAgentsWithLangChainAndLangGraph
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   cd 02Langchain
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env files in project directories
   echo "OPENAI_API_KEY=your_api_key_here" > 01Project/.env
   echo "OPENAI_API_KEY=your_api_key_here" > 02Langchain/.env
   ```

### Running the Examples

#### Basic Agent Operations
```bash
# Test memory functionality
python "01Project/D1 Memory.py"

# Test function calling
python "01Project/D2 Function calling.py"

# Test self-reflection system
python "01Project/E3 Self reflection.py"
```

#### LangChain Examples
```bash
cd 02Langchain
python langchain.py
```

## 📚 Course Information

**Provider**: Udacity  
**Course**: AI Agents with LangChain and LangGraph  
**Duration**: 4 weeks (estimated)  
**Level**: Intermediate to Advanced  
**Prerequisites**: Python programming, basic ML/AI knowledge

**Key Learning Outcomes:**
- Build production-ready AI agents from scratch
- Master LangChain and LangGraph frameworks
- Implement advanced memory and reasoning systems
- Create self-improving and self-reflective agents
- Design multi-agent coordination systems
- Apply best practices for AI safety and ethics

## 🔧 Technologies & Dependencies

### Core Technologies
- **Python 3.8+**: Primary programming language
- **OpenAI GPT-4**: Large language model for agent intelligence
- **LangChain**: Framework for LLM application development
- **LangGraph**: Advanced workflow orchestration
- **dotenv**: Environment variable management

### Key Dependencies
```txt
langchain-openai>=0.1.0
langchain-core>=0.2.0
python-dotenv>=1.0.0
openai>=1.0.0
```

## 📈 Learning Progress Tracker

### ✅ Completed Modules
- [x] **Module 1**: Agent Fundamentals and Architecture
- [x] **Module 2**: Memory Systems Implementation
- [x] **Module 3**: Function Calling and Tool Integration
- [x] **Module 4**: Self-Reflection and Improvement Mechanisms
- [x] **Module 5**: LangChain Framework Deep Dive
- [x] **Module 6**: Prompt Engineering and Template Management

### 🔄 In Progress
- [ ] **Module 7**: LangGraph State Machines
- [ ] **Module 8**: Advanced Multi-Agent Coordination
- [ ] **Module 9**: Production Deployment Strategies

### 📅 Upcoming
- [ ] **Module 10**: Performance Optimization and Scaling
- [ ] **Module 11**: AI Safety and Ethical Considerations
- [ ] **Module 12**: Final Capstone Project

## 🎯 Real-World Applications

The techniques learned in this course can be applied to:

- **Customer Service Automation**: Intelligent chatbots with memory and context
- **Content Generation**: Automated content creation with quality control
- **Data Analysis**: AI agents that can analyze and report on complex datasets
- **Process Automation**: Intelligent workflow automation with decision-making
- **Educational Tools**: Personalized tutoring systems with adaptive learning
- **Research Assistance**: AI-powered research and knowledge discovery tools

## 🤝 Contributing

This repository is primarily for educational purposes, but contributions and improvements are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request with detailed explanations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Additional Resources

- [Udacity Course Page](https://www.udacity.com/course/ai-agents-langchain-langgraph)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

*This repository represents a comprehensive learning journey in AI agent development, showcasing the evolution from basic concepts to advanced, production-ready intelligent systems. Each implementation builds upon previous learning while introducing new frameworks and methodologies for creating sophisticated AI agents.*

**Last Updated**: November 2025  
**Status**: Active Learning Project  
**Next Milestone**: LangGraph Implementation & Multi-Agent Coordination