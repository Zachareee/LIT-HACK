import ollama
from typing import Callable

class Question:
    def __init__(self, question: str, layman: str, options: list[str] | None = ["Yes", "No", "Maybe"], hide_if: list[Callable[[int, str], bool]] = [], warn: Callable = lambda x: None) -> None:
        self.question = question
        self.layman = layman
        self.options = options
        self.hide_if = hide_if
        self.warn = warn


def chat(message: str, question: Question) -> str:
    response = ollama.chat(
        model="llama3.1",
        messages=[{
            'role': 'user',
            'content': f"{message}. Does this answer '{question}'? Reply with only {question.options} or maybe"
        }]
    )['message']['content']
    if question.options == None: return response
    if response in question.options: return response
    raise Exception("Response not in options")


questions = [
    Question(
        "Contract for sale of goods",
        "How did you purchase the goods?",
        options=["Defective Goods", "Non-Delivery", "Goods Not As Contracted", "Non-Payment", "Cancellation/Opt Out",
                 "Refund (motor vehicle deposit)", "Unfair Practice in relation to Hire Purchase Agreements", "Others"],
    ), Question(
        "Contract for Provision of Services",
        "",
        options=["Unsatisfactory Services", "Incomplete Services",
                 "Renovation Services", "No Services Rendered", "Non-Payment", "Others"]
    ), Question(
        "Damage to Property",
        "",
        options=["Owner of Property",
                 "Damage not arising from motor vehicle accident", "Others"]
    ), Question(
        "Lease Not Exceeding 2 Years (Residential Premises)",
        "",
        options=["Breach of Tenant's Obligation ", "Breach of Landlord's Obligation ",
                 "Refund of Rental Deposit ", "Rental Arrears ", "Others "]
    ), Question(
        "Hi",
        "Bye",
        options=None
    )
]

answers = []