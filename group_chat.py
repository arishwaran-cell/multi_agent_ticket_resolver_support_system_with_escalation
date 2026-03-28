from autogen import GroupChat, GroupChatManager, UserProxyAgent
from agents.classifier_agent import get_classifier_agent
from agents.knowledge_base_agent import get_knowledge_base_agent
from agents.notification_agent import get_notification_agent
from utility.llm_config import llm_config


def is_termination_msg(message):
    return (
        isinstance(message, dict)
        and message.get("content", "").strip().endswith("TERMINATE")
    )

classifier = get_classifier_agent()
kb_agent = get_knowledge_base_agent()
notification_agent = get_notification_agent()


user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=is_termination_msg,
    max_consecutive_auto_reply=10,  # 🔥 important
)


groupchat = GroupChat(
    agents=[user, classifier, kb_agent, notification_agent],
    messages=[],
    speaker_selection_method="round_robin",  # 🔥 KEY FIX
    allow_repeat_speaker=True,
    max_round=10
)


manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
    is_termination_msg=is_termination_msg,
    max_consecutive_auto_reply=10   # 🔥 ADD THIS
)