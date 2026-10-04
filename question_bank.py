from dataclasses import dataclass, field
from typing import List


@dataclass
class Question:
    category: str
    prompt: str
    keywords: List[str] = field(default_factory=list)


QUESTION_BANK = {
    "Software Engineering": [
        Question(
            category="Software Engineering",
            prompt="Explain the difference between abstraction and encapsulation in object-oriented programming.",
            keywords=["abstraction", "encapsulation", "class", "hide", "details", "interface"],
        ),
        Question(
            category="Software Engineering",
            prompt="Describe how you would design a scalable REST API for a student portal.",
            keywords=["api", "rest", "endpoints", "authentication", "database", "scalable", "server"],
        ),
        Question(
            category="Software Engineering",
            prompt="What is the importance of version control in a software project?",
            keywords=["git", "commit", "branch", "history", "collaboration", "version control"],
        ),
    ],
    "General Behavioral": [
        Question(
            category="General Behavioral",
            prompt="Tell us about a time you handled pressure or a tight deadline.",
            keywords=["deadline", "pressure", "priority", "plan", "communication", "team"],
        ),
        Question(
            category="General Behavioral",
            prompt="Why do you want to work in this role or field?",
            keywords=["motivation", "interest", "growth", "learn", "goal", "career"],
        ),
        Question(
            category="General Behavioral",
            prompt="Describe a situation where you solved a problem creatively.",
            keywords=["problem", "creative", "solution", "analysis", "decision", "result"],
        ),
    ],
    "Data Structures": [
        Question(
            category="Data Structures",
            prompt="What is the difference between a stack and a queue?",
            keywords=["stack", "queue", "lifo", "fifo", "push", "pop", "enqueue", "dequeue"],
        ),
        Question(
            category="Data Structures",
            prompt="When would you choose a hash map instead of a list?",
            keywords=["hash map", "dictionary", "lookup", "search", "time complexity", "key value"],
        ),
    ],
}
