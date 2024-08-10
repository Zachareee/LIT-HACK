import ollama
from typing import Callable
import re

YES, NO = "Yes", "No"
OPTIONS = [YES, NO]
questionNum = 0
END = "DONE"
MODEL = "llama3.1"
ollama.pull(MODEL)


class Question:
    def __init__(self, question: str, layman: str, next: Callable[[str], int] = lambda x: None, warn: Callable[[str], str] = lambda x: None) -> None:
        self.question = question
        self.layman = layman
        self.next = next
        self.warn = warn


def constructChoices() -> list[str]:
    arr = []
    for idx in range(questionsLength):
        for key, value in list(hardcode.items()):
            if idx > key:
                arr.append(value)
                del hardcode[key]
        answer = answers[idx]
        if answer is not None:
            arr.append(f"{questions[idx].question}: {answer}")
    return arr


def eval_question(message: str) -> None:
    global questionNum
    while True:
        question = questions[questionNum]

        response = chat(message, question)
        print(f"Ollama run done, response: {response}")

        if re.search("yes", response, re.I):
            response = YES
        if re.search("no", response, re.I):
            response = NO

        if response not in OPTIONS:
            raise Exception(question)

        answers[questionNum] = response
        warning = question.warn(response)
        if warning:
            accumulatedWarnings.append(warning)

        next = question.next(response)
        if next == END:
            return
        elif next is None:
            questionNum += 1
        else:
            questionNum = next


def chat(message: str, question: Question) -> str:
    print("Running Ollama")
    return ollama.chat(
        model=MODEL,
        messages=[{
            'role': 'user',
            'content': f"A user replies \"{message}\" to the question \"{question.question}\". The user is answering a critical question, hence there should be no mistake in trying to determine what he is trying to convey. What is the user implying? Reply with only yes or no, or maybe if you are unsure"
        }]
    )['message']['content']


def genWarning(actual: str, expected: str, warningNum: int):
    if (actual == expected):
        return warnings[warningNum]
    return None


def jump(actual: str, expected: str, jumpIdx: int):
    if (actual == expected):
        return jumpIdx
    return None


questions = [
    Question(  # 0
        "Are you a bankrupt?",
        "Are you a bankrupt?"
    ), Question(  # 1
        "Do you have permission from Official Assignee to commence court proceedings?",
        "Did you get permission from Official Assignee to go to court?",
        warn=lambda x: genWarning(x, NO, 0)
    ), Question(  # 2
        "Are you claiming against the correct party with whom you have a contractual obligation?",
        "Are you bringing the right person or people to court which you signed a contract with?",
        warn=lambda x: genWarning(x, NO, 1)
    ), Question(  # 3
        "Is the other party an individual?",
        "Is the scammer working alone?",
        next=lambda x: jump(x, YES, 7)
    ), Question(  # 4
        "We note that you are claiming against a corporate entity. Is the other party in liquidation or winding-up?",
        "Is the organisation of the scammer closing down or declaring bankruptcy?",
        warn=lambda x: genWarning(x, YES, 2)
    ), Question(  # 5
        "Do you have the recent (within the last 1 month) ACRA record showing the address and status of the party?",
        "Do you have any ACRA record (within the last month) mentioning the address and status of the scammer?",
        warn=lambda x: genWarning(x, NO, 3)
    ), Question(  # 6
        "In the recent ACRA record, is the corporate entity's (party) status reflected as \"Live\"",
        "Is the scammers' status \"Live\" in the ACRA record?",
        warn=lambda x: genWarning(x, NO, 4),
    ), Question(  # 7
        "Is there a mediation/arbitration clause in your agreement?",
        "Did you sign a contract with the other party to settle disagreements outside of court?"
    ), Question(  # 8
        "Do all parties agree to dispense with the mediation/arbitration clause and have the matter dealt with at SCT?",
        "Do both parties agree to go to court instead of settling?",
        warn=lambda x: genWarning(x, NO, 5)
    ), Question(  # 9
        "Does your claim relate to a contract for goods sold/bought?",
        "Is this claim related to something you bought or sold?",
        warn=lambda x: genWarning(x, NO, 6)
    ), Question(  # 10
        "Did the cause of action arise on or before 31 Oct 2018?",
        "Did this happen before 31 Oct 2018?",
        warn=lambda x: genWarning(x, YES, 7)
    ), Question(  # 11
        "Is your claim evidenced in writing?",
        "Is there written evidence?",
        warn=lambda x: genWarning(x, NO, 8)
    ), Question(  # 12
        "Are you splitting or dividing your invoice/contract to bring it within SCT's jurisdiction?",
        "Are you splitting the bill or contract so that it may be brought to Small Claims Tribunal?",
        warn=lambda x: genWarning(x, YES, 9)
    ), Question(  # 13
        "Does your claim relate to or arise out of consignment of goods?",
        "Was there a middleman involved in the transaction?",
        warn=lambda x: genWarning(x, NO, 10)
    ), Question(  # 14
        "Has the credit term or delivery date lapsed?",
        "Has the deadline for the transaction passed?",
        warn=lambda x: genWarning(x, NO, 11)
    ), Question(  # 15
        "Were the goods delivered?",
        "Were the goods delivered?",
        warn=lambda x: genWarning(x, NO, 12),
        next=lambda x: jump(x, NO, 19)
    ), Question(  # 16
        "Were there damages or defects to the goods?",
        "Were the goods damaged?",
        warn=lambda x: genWarning(x, NO, 13),
        next=lambda x: jump(x, NO, 19)
    ), Question(  # 17
        "Did you inform the other party of the defects?",
        "Did you tell the other party about the damages?",
        warn=lambda x: genWarning(x, NO, 14)
    ), Question(  # 18
        "Did the damage or defects occur within 6 months from the Sale of the goods?",
        "Did the damage happen within 6 months of buying the goods?",
        warn=lambda x: genWarning(x, NO, 15)
    ), Question(  # 19
        "Are you seeking a Money Order, Work Order and/or an Order for delivering vacant possession?",
        "Are you seeking a Money Order, Work Order and/or an Order for delivering vacant possession?",
        warn=lambda x: genWarning(x, NO, 16)
    ), Question(  # 20
        "Is the party/company whom you are filing against residing/located in Singapore or have a registered address in Singapore?",
        "Is the other party in Singapore or do they have an address?",
        warn=lambda x: genWarning(x, NO, 17)
    ), Question(  # 21
        "Are you able to locate and personally serve/bring the claim to the attention of the other party in Singapore?",
        "Is it possible for you to notify the other party in Singapore?",
        warn=lambda x: genWarning(x, NO, 18),
        next=lambda x: END
    )
]

warnings = [
    # 0
    "A bankrupt cannot sue or commence legal actions against another party without the permission from the Official Assignee.",
    # 1
    "You need to ensure that the claim is brought against a party or parties whom you have a contractual obligation with. SCT cannot deal with a matter where the party (or parties) whom you are filing against have no contractual obligation with you.",
    # 2
    "You cannot bring a claim against a corporate entity in liquidation or winding up, unless you have the permission of the High Court.",
    # 3
    "You need to obtain the latest ACRA record to determine the registered office address and status of the corporate entity. You can purchase a copy of the ACRA record at www.acra.gov.sg.",
    # 4
    "SCT cannot hear the matter against a corporate entity which is no longer Live.",
    # 5
    "SCT cannot hear the matter as the agreement requires any dispute to be resolved by way of arbitration, unless both parties agree in writing to dispense with the arbitration clause and have the matter dealt with at SCT.",
    # 6
    "Your claim may not relate to a contract for Sale of Goods. Please re-consider whether you have selected the correct nature of dispute.",
    # 7
    "SCT does not have jurisdiction to hear this claim. Please seek your own legal advice.",
    # 8
    "You must show evidence or supporting documents to enforce the duties and obligations of the parties under the contract.",
    # 9
    "No claim shall be split or divided and pursued in separate proceedings at SCT for the sole purpose of bringing the amount claimed in each of such proceedings within the jurisdiction of SCT.",
    # 10
    "SCT does not have jurisdiction to deal with consignment of goods. You may consider filing your claim in another appropriate forum.",
    # 11
    "You should wait till the contracted service performance date is due before filing your claim.",
    # 12
    "You may wish to consider contacting the other party to understand the reason for the non-delivery and explore mutual settlement before filing your claim.",
    # 13
    "Please consider how you are going to support your case at SCT, by showing evidence or supporting documents. You may also wish to confirm whether you are claiming under 'Sale of Goods' or 'Damage to Property'.",
    # 14
    "You should inform the other party of the defects and explore mutual settlement with the other party before filing your claim at SCT.",
    # 15
    "Generally, under the Lemon Law, if the defect is detected within 6 months of purchase, it is presumed the defect existed at the time of the delivery or purchase, unless the seller can prove otherwise. Please consider how you are going to support your case at SCT, by showing evidence or supporting documents. If it is a used car, you should also take into account the age of the car , depreciation and fair wear and tear.",
    # 16
    "SCT is unable to issue any other types of orders.",
    # 17
    "You cannot bring a claim against a person or entity who is out of jurisdiction (outside Singapore).",
    # 18
    "SCT cannot hear the matter if service has not been performed, ie. you have not brought the claim to the attention of the other party personally."
]

questionsLength = len(questions)
answers = [None] * questionsLength
accumulatedWarnings = []
hardcode = {12: "Is your claim related to profit or commission sharing?"}


def resetAI():
    global answers, accumulatedWarnings, hardcode
    answers = [None] * questionsLength
    accumulatedWarnings = []
    hardcode = {-1: "Are you claiming as an individual?: Yes", 12: "Is your claim related to profit or commission sharing?: No"}
