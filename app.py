import gradio as gr
from group_chat import user, manager, notification_agent
import random
import string
import traceback

# ---------------------------
# Ticket generator
# ---------------------------
def generate_ticket_id(prefix="TKT", length=6):
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}-{suffix}"


# ---------------------------
# Core AI handler
# ---------------------------
def resolve_issue(user_input):
    print("🔹 resolve_issue called")

    if not user_input or not user_input.strip():
        return "⚠️ Please describe your issue.", user_input, False

    responses = []
    original_receive = user.receive

    try:
        def receive_and_capture(*args, **kwargs):
            if len(args) >= 2:
                message = args[0]
                if isinstance(message, dict):
                    content = message.get("content", "")
                    if content:
                        responses.append(content)
            return original_receive(*args, **kwargs)

        user.receive = receive_and_capture

        print("🔹 Starting agent chat...")
        user.initiate_chat(recipient=manager, message=user_input)
        print("🔹 Agent chat finished")

    finally:
        user.receive = original_receive

    if responses:
        return responses[-1], user_input, True
    else:
        return "⚠️ No response received from agents.", user_input, False


# ---------------------------
# Feedback handlers
# ---------------------------
def feedback_yes():
    print("👍 User said YES")
    return "🎉 Glad your issue is resolved!", False


def feedback_no(user_input):
    print("👎 User said NO")

    ticket_id = generate_ticket_id()

    notification_message = (
        f"🚨 Unresolved IT Issue\n\n"
        f"User reported: '{user_input}'\n"
        f"📄 Ticket ID: {ticket_id}"
    )

    try:
        reply = notification_agent.generate_reply(
            messages=[{"role": "user", "content": notification_message}],
            sender=user
        )

        final_reply = reply.get("content") if isinstance(reply, dict) else str(reply)

        return (
            f"⚠️ Issue escalated.\n\n📄 Ticket: {ticket_id}\n\n📨 {final_reply}",
            False
        )

    except Exception as e:
        error_details = traceback.format_exc()
        print("❌ Escalation Error:\n", error_details)
        return f"❌ Escalation failed:\n\n```\n{error_details}\n```", False


# ---------------------------
# UI
# ---------------------------
with gr.Blocks(title="Multi-Agent Ticket Resolver Support System with Escalation") as demo:

    gr.Markdown("# 🤖 Multi-Agent Ticket Resolver Support System with Escalation")
    gr.Markdown("## ⚡ Your AI Agents IT Support Assistant")

    # State variables
    state_user_input = gr.State("")
    state_show_feedback = gr.State(False)

    # Input
    user_input = gr.Textbox(
        label="Describe your IT issue",
        lines=5,
        placeholder="Example: Outlook crashes when opening..."
    )

    # Output
    output = gr.Markdown()

    # Button
    resolve_btn = gr.Button("🚀 Resolve Now")

    # Feedback row (IMPORTANT FIX)
    feedback_row = gr.Row(visible=False)
    with feedback_row:
        yes_btn = gr.Button("✅ Yes")
        no_btn = gr.Button("❌ No")

    # ---------------------------
    # Resolve flow with loading + error tracing
    # ---------------------------
    def resolve_wrapper(text):
        print("🚀 BUTTON CLICKED")

        # Step 1: Show loading immediately
        yield (
            "⏳ Processing your request... please wait...",
            text,
            False,
            gr.update(visible=False)
        )

        try:
            print("🔹 Calling resolve_issue...")
            result, saved_input, show_feedback = resolve_issue(text)

            print("✅ Completed successfully")

            # Step 2: Show result
            yield (
                result,
                saved_input,
                show_feedback,
                gr.update(visible=show_feedback)
            )

        except Exception:
            error_details = traceback.format_exc()
            print("❌ FULL ERROR:\n", error_details)

            # Step 3: Show full error in UI
            yield (
                f"❌ ERROR OCCURRED:\n\n```\n{error_details}\n```",
                text,
                False,
                gr.update(visible=False)
            )

    resolve_btn.click(
        fn=resolve_wrapper,
        inputs=[user_input],
        outputs=[output, state_user_input, state_show_feedback, feedback_row],
        show_progress=True
    )

    # ---------------------------
    # YES feedback
    # ---------------------------
    def yes_wrapper():
        result, show_feedback = feedback_yes()
        return result, show_feedback, gr.update(visible=False)

    yes_btn.click(
        fn=yes_wrapper,
        inputs=[],
        outputs=[output, state_show_feedback, feedback_row]
    )

    # ---------------------------
    # NO feedback
    # ---------------------------
    def no_wrapper(saved_input):
        result, show_feedback = feedback_no(saved_input)
        return result, show_feedback, gr.update(visible=False)

    no_btn.click(
        fn=no_wrapper,
        inputs=[state_user_input],
        outputs=[output, state_show_feedback, feedback_row]
    )


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    demo.launch(debug=True)