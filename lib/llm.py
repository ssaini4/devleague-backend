from openai import OpenAI

from config import XAI_API_KEY

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
                "content": "Create a fun, respectful, and concise description of the Github user's profile using the information provided. The description should be 1-2 sentences (150 characters max). The description should be in third person, direct, and promote the user's skills and contributions. DO NOT use the word 'user' or 'profile' in the description. DO NOT use the word 'Github' in the description. DO NOT mention user's pull requests, issues, or comments in the description. Be creative and write like a fiction book or a pokemon card. DO NOT use special characters like *, ', or #",
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
                "content": "Create a fun, respectful, and concise description of the github user using the number of contributions. It should be creative, and 2-3 words max. Some examples: Contributor General, Extraordinary Contributor, Contributor Extraordinaire, MVP Contributor. Be creative and write like a fiction book or a pokemon card. DO NOT use special characters like *, ', or #",
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
                "content": "Create a fun, respectful, and concise description of the github user using the number of comments. It should be creative, and 2-3 words max. Some examples: Comment Maniac, Super Commenter, Crazy Critic. Be creative and write like a fiction book or a pokemon card. DO NOT use special characters like *, ', or #",
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
                "content": "Create a fun, respectful, and concise description of the github user using the number of issues. It should be creative, and 2-3 words max. Some examples: Issue Digger, Super Issue Solver, Crazy Issue Creator. Be creative and write like a fiction book or a pokemon card. DO NOT use special characters like *, ', or #.",
            },
            {"role": "user", "content": f"Number of issues: {card.issues}"},
        ],
    )

    return completion.choices[0].message.content
