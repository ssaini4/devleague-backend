from openai import OpenAI
from enum import Enum

from config import XAI_API_KEY
from lib.prompts import (
    DESCRIPTION_PROMPT,
    CONTRIBUTION_PROMPT,
    COMMENT_PROMPT,
    ISSUE_PROMPT,
    ROAST_DESCRIPTION_PROMPT,
    ROAST_CONTRIBUTION_PROMPT,
    ROAST_COMMENT_PROMPT,
    ROAST_ISSUE_PROMPT,
)

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)


class CardType(str, Enum):
    NORMAL = "NORMAL"
    ROAST = "ROAST"


def create_description(card: "Card", card_type: CardType = CardType.NORMAL):
    profile_disc = f"Number of contributions: {card.total_commits}\n Number of issues: {card.issues}\n Number of pull requests: {card.pull_requests}\n Number of comments: {card.comments}\n Primary languages: {card.get_primary_languages()}"

    prompt = DESCRIPTION_PROMPT if card_type == CardType.NORMAL else ROAST_DESCRIPTION_PROMPT

    completion = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": profile_disc},
        ],
    )

    return completion.choices[0].message.content


def create_contribution_description(card: "Card", card_type: CardType = CardType.NORMAL):
    prompt = CONTRIBUTION_PROMPT if card_type == CardType.NORMAL else ROAST_CONTRIBUTION_PROMPT

    completion = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": f"Number of contributions: {card.total_commits}",
            },
        ],
    )

    return completion.choices[0].message.content


def create_comment_description(card: "Card", card_type: CardType = CardType.NORMAL):
    prompt = COMMENT_PROMPT if card_type == CardType.NORMAL else ROAST_COMMENT_PROMPT

    completion = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": f"Number of comments: {card.comments}"},
        ],
    )

    return completion.choices[0].message.content


def create_issue_description(card: "Card", card_type: CardType = CardType.NORMAL):
    prompt = ISSUE_PROMPT if card_type == CardType.NORMAL else ROAST_ISSUE_PROMPT

    completion = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": f"Number of issues: {card.issues}"},
        ],
    )

    return completion.choices[0].message.content
