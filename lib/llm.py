from openai import OpenAI

from config import XAI_API_KEY
from lib.prompts import DESCRIPTION_PROMPT, CONTRIBUTION_PROMPT, COMMENT_PROMPT, ISSUE_PROMPT

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)


def create_description(card: "Card"):
    profile_disc = f"Number of contributions: {card.total_commits}\n Number of issues: {card.issues}\n Number of pull requests: {card.pull_requests}\n Number of comments: {card.comments}\n Primary languages: {card.get_primary_languages()}"
    completion = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {
                "role": "system",
                "content": DESCRIPTION_PROMPT,
            },
            {"role": "user", "content": profile_disc},
        ],
    )

    return completion.choices[0].message.content


def create_contribution_description(card: "Card"):
    completion = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {
                "role": "system",
                "content": CONTRIBUTION_PROMPT,
            },
            {
                "role": "user",
                "content": f"Number of contributions: {card.total_commits}",
            },
        ],
    )

    return completion.choices[0].message.content


def create_comment_description(card: "Card"):
    completion = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {
                "role": "system",
                "content": COMMENT_PROMPT,
            },
            {"role": "user", "content": f"Number of comments: {card.comments}"},
        ],
    )

    return completion.choices[0].message.content


def create_issue_description(card: "Card"):
    completion = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {
                "role": "system",
                "content": ISSUE_PROMPT,
            },
            {"role": "user", "content": f"Number of issues: {card.issues}"},
        ],
    )

    return completion.choices[0].message.content
