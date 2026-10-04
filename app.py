import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from question_bank import QUESTION_BANK, Question


class InterviewAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Interview Preparation Assistant")
        self.root.geometry("1000x700")
        self.root.minsize(860, 620)

        self.category_var = tk.StringVar()
        self.current_questions = []
        self.current_index = 0
        self.answers = []
        self.results = []

        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.show_start_screen()

    def clear_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear_widgets()

        title = ttk.Label(
            self.main_frame,
            text="AI Interview Preparation Assistant",
            font=("Segoe UI", 22, "bold"),
        )
        title.pack(pady=(10, 20))

        subtitle = ttk.Label(
            self.main_frame,
            text="Practice technical and behavioral interview questions with instant feedback.",
            font=("Segoe UI", 11),
            wraplength=700,
        )
        subtitle.pack(pady=(0, 20))

        card = ttk.Frame(self.main_frame, padding=20)
        card.pack(fill=tk.X, padx=80)

        ttk.Label(card, text="Choose interview category:", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        categories = list(QUESTION_BANK.keys())
        self.category_var.set(categories[0])
        category_menu = ttk.Combobox(card, textvariable=self.category_var, values=categories, state="readonly", width=40)
        category_menu.pack(anchor="w", pady=(8, 18))

        actions = ttk.Frame(card)
        actions.pack(anchor="w")
        ttk.Button(actions, text="Start Interview", command=self.start_interview, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions, text="Exit", command=self.root.destroy, width=15).pack(side=tk.LEFT)

        info = ttk.Label(
            self.main_frame,
            text="Features included: answer evaluation, score generation, answer feedback, summary report.",
            font=("Segoe UI", 10),
            foreground="#555555",
            wraplength=720,
        )
        info.pack(pady=(25, 0))

    def start_interview(self):
        selected = self.category_var.get()
        if not selected:
            messagebox.showwarning("Selection required", "Please choose a category before continuing.")
            return

        self.current_questions = QUESTION_BANK[selected][:]
        self.current_index = 0
        self.answers = []
        self.results = []
        self.show_question_screen()

    def show_question_screen(self):
        self.clear_widgets()

        question = self.current_questions[self.current_index]

        header = ttk.Label(
            self.main_frame,
            text=f"Question {self.current_index + 1} of {len(self.current_questions)}",
            font=("Segoe UI", 12, "bold"),
        )
        header.pack(anchor="w", pady=(0, 12))

        prompt = ttk.Label(
            self.main_frame,
            text=question.prompt,
            font=("Segoe UI", 14),
            wraplength=800,
            justify=tk.LEFT,
        )
        prompt.pack(anchor="w", pady=(0, 20))

        answer_box = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=110, height=16, font=("Segoe UI", 11))
        answer_box.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        buttons = ttk.Frame(self.main_frame)
        buttons.pack(fill=tk.X)

        ttk.Button(buttons, text="Submit Answer", command=lambda: self.submit_answer(answer_box, question), width=18).pack(side=tk.LEFT)
        ttk.Button(buttons, text="Back to Home", command=self.show_start_screen, width=18).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(buttons, text="Exit", command=self.root.destroy, width=15).pack(side=tk.RIGHT)

    def submit_answer(self, answer_box, question):
        answer_text = answer_box.get("1.0", tk.END).strip()
        if not answer_text:
            messagebox.showwarning("Missing answer", "Please provide an answer before submitting.")
            return

        score, feedback = self.evaluate_answer(answer_text, question)
        self.results.append({
            "question": question.prompt,
            "score": score,
            "feedback": feedback,
            "answer": answer_text,
        })

        self.current_index += 1
        if self.current_index < len(self.current_questions):
            self.show_question_screen()
        else:
            self.show_summary_screen()

    @staticmethod
    def evaluate_answer(answer, question: Question):
        if not answer or len(answer.strip()) < 20:
            return 0, "Your answer is too short. Add more detail and explain your reasoning clearly."

        lowered = answer.lower()
        keyword_hits = sum(1 for kw in question.keywords if kw.lower() in lowered)

        length_score = min(10, len(answer.split()) // 16)
        relevance_score = min(10, 3 + keyword_hits * 2)
        clarity_score = 6 if len(answer.split()) > 30 else 4

        score = round((relevance_score + length_score + clarity_score) / 3)
        score = max(0, min(100, score * 10))

        if score >= 85:
            feedback = "Excellent answer. It is relevant, well-structured, and demonstrates clear understanding."
        elif score >= 70:
            feedback = "Good response. You have the main idea; improve by adding examples and stronger reasoning."
        elif score >= 50:
            feedback = "Fair attempt. Make your explanation more specific and tie it back to the key concepts."
        else:
            feedback = "Your answer needs more depth. Include technical details, examples, and clearer structure."

        return score, feedback

    def show_summary_screen(self):
        self.clear_widgets()

        average_score = 0
        if self.results:
            average_score = round(sum(item["score"] for item in self.results) / len(self.results))

        title = ttk.Label(
            self.main_frame,
            text="Interview Summary",
            font=("Segoe UI", 22, "bold"),
        )
        title.pack(pady=(10, 15))

        ttk.Label(
            self.main_frame,
            text=f"Average score: {average_score}/100",
            font=("Segoe UI", 16),
        ).pack(pady=(0, 15))

        summary_frame = ttk.Frame(self.main_frame)
        summary_frame.pack(fill=tk.BOTH, expand=True)

        for idx, item in enumerate(self.results, start=1):
            result_card = ttk.LabelFrame(summary_frame, text=f"Q{idx}", padding=(12, 10))
            result_card.pack(fill=tk.X, pady=8)
            ttk.Label(result_card, text=f"Score: {item['score']}/100", font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Label(result_card, text=f"Feedback: {item['feedback']}", wraplength=740, justify=tk.LEFT).pack(anchor="w", pady=(4, 0))

        buttons = ttk.Frame(self.main_frame)
        buttons.pack(pady=(20, 0))
        ttk.Button(buttons, text="Try Again", command=self.show_start_screen, width=16).pack(side=tk.LEFT, padx=(0, 12))
        ttk.Button(buttons, text="Exit", command=self.root.destroy, width=12).pack(side=tk.LEFT)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterviewAssistantApp(root)
    root.mainloop()
