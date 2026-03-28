from autogen import AssistantAgent
from utility.llm_config import llm_config
from tools.send_email import escalate_ticket_with_email


def get_notification_agent():

    notification_agent = AssistantAgent(
        name="NotificationAgent",
        system_message=(
            "You are an IT escalation agent.\n\n"
            "MANDATORY RULES:\n"
            "1. If the issue is unresolved or you see 'NO_SOLUTION_FOUND', you MUST call the tool 'escalate_ticket_with_email'.\n"
            "2. Use EXACT JSON format:\n"
            "{ \"issue\": \"user issue string\" }\n"
            "3. DO NOT use keys like 'ticket'. Only use 'issue'.\n"
            "4. DO NOT explain — call the tool directly.\n"
            "5. After sending email, confirm escalation.\n"
            "6. Always end your response with TERMINATE."
        ),
        llm_config=llm_config,
        code_execution_config={"use_docker": False},
    )

    # ✅ Tool registration (STRICT FORMAT)
    notification_agent.register_for_llm(
        name="escalate_ticket_with_email",
        description=(
            "Send escalation email for unresolved IT issues.\n"
            "Input MUST be:\n"
            "{ \"issue\": \"string\" }\n"
            "Example:\n"
            "{ \"issue\": \"Laptop not working\" }"
        )
    )(escalate_ticket_with_email)

    notification_agent.register_for_execution(
        name="escalate_ticket_with_email"
    )(escalate_ticket_with_email)

    return notification_agent