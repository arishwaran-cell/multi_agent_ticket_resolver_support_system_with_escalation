from autogen import AssistantAgent
from tools.knowledge_base_tool import search_similar_solution
from utility.llm_config import llm_config


def get_knowledge_base_agent():

    knowledge_agent = AssistantAgent(
        name="KnowledgeBaseAgent",
        system_message=(
            "You are an IT support assistant.\n\n"

            "STRICT EXECUTION:\n"

            "1. ALWAYS call 'search_similar_solution'\n"
            "2. WAIT for tool result\n"
            "3. AFTER tool result:\n"
            "   - Extract ONLY the solution\n"
            "   - Explain clearly\n"
            "4. If tool returns 'No matching solutions found.', respond EXACTLY: NO_SOLUTION_FOUND TERMINATE\n"
            "5. ALWAYS respond AFTER tool\n"
            "6. ALWAYS end with TERMINATE\n\n"

            "NEVER:\n"
            "- stop after tool call\n"
            "- return empty response\n"
        ),
        llm_config=llm_config,
        code_execution_config={"use_docker": False},
    )

    knowledge_agent.register_for_llm(
        name="search_similar_solution",
        description=(
            "Search IT solutions.\n"
            "Format:\n"
            "{ \"query\": \"string\", \"category\": \"optional string\" }"
        )
    )(search_similar_solution)

    knowledge_agent.register_for_execution(
        name="search_similar_solution"
    )(search_similar_solution)

    return knowledge_agent