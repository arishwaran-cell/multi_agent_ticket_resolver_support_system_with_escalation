import gradio as gr
import json

from group_chat import manager, user
from tools.send_email import escalate_ticket_with_email


# =============================
# 🧠 RUN AUTOGEN
# =============================

def run_autogen(user_input):
    try:
        result = user.initiate_chat(
            recipient=manager,
            message=user_input
        )

        chat_history = result.chat_history
        final_answer = ""

        for msg in reversed(chat_history):
            if msg.get("role") == "tool":
                content = msg.get("content", "")

                if "No matching solutions found." in content:
                    final_answer = "❌ No solution found. You can escalate this issue."
                else:
                    lines = content.split("\n")
                    solution_lines = [l for l in lines if l.startswith("Solution:")]

                    if solution_lines:
                        final_answer = solution_lines[0].replace("Solution:", "").strip()
                    else:
                        final_answer = content

                break

        return final_answer, gr.update(visible=True)

    except Exception as e:
        return f"❌ ERROR:\n{str(e)}", gr.update(visible=False)


# =============================
# 📧 ESCALATION
# =============================

def escalate_issue(issue):
    result = escalate_ticket_with_email(issue)
    return result["content"]


# =============================
# 🎨 UI
# =============================

with gr.Blocks() as demo:

    gr.Markdown("# 🤖 AI IT Support System")
    gr.Markdown("### ⚡ AutoGen + RAG + Email Escalation")

    user_input = gr.Textbox(
        label="Describe your IT issue",
        lines=5,
        placeholder="e.g., VPN not connecting"
    )

    resolve_btn = gr.Button("🚀 Resolve Issue")

    output = gr.Textbox(label="Solution", lines=8)

    with gr.Row(visible=False) as feedback_row:
        yes_btn = gr.Button("✅ Resolved")
        no_btn = gr.Button("❌ Not Resolved")

    status = gr.Textbox(label="Status")

    # =============================
    # 🔁 FLOW
    # =============================

    resolve_btn.click(
        fn=run_autogen,
        inputs=user_input,
        outputs=[output, feedback_row],
        show_progress=True
    )

    yes_btn.click(
        fn=lambda: "✅ Glad it worked!",
        outputs=status
    )

    no_btn.click(
        fn=escalate_issue,
        inputs=user_input,
        outputs=status
    )


# =============================
# ▶️ RUN
# =============================

if __name__ == "__main__":
    demo.launch()