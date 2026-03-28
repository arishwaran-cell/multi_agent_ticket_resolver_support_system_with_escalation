from autogen import AssistantAgent
from utility.llm_config import llm_config


def get_classifier_agent():

    return AssistantAgent(
        name="ClassifierAgent",
        system_message=(
            "You are a strict IT issue classifier.\n\n"

            "RULES:\n"
            "1. Return ONLY valid JSON.\n"
            "2. Format MUST be:\n"
            "{ \"ticket\": \"user issue\", \"category\": \"category name\" }\n"
            "3. DO NOT ask questions.\n"
            "4. DO NOT explain anything.\n"
            "5. DO NOT add extra text.\n"
            "6. DO NOT include TERMINATE.\n"
        ),
        llm_config=llm_config
    )