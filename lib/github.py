import json
from typing import Dict

import requests


class GithubClient:
    def __init__(self, token: str):
        self.token = token
        self.url = "https://api.github.com/graphql"

    def fetch_user_stats(self, username: str) -> Dict:
        query = """
        query($username: String!) {
            user(login: $username) {
                name
                email
                avatarUrl
                repositories(first: 100) {
                    totalCount
                    nodes{
                        name
                        stargazerCount
                        primaryLanguage {
                            name
                            color
                        }
                    }
                }
                pullRequests {
                    totalCount
                }
                issues {
                    totalCount
                }
                contributionsCollection {
                    contributionCalendar {
                        totalContributions
                    }
                    totalCommitContributions
                    totalIssueContributions
                    totalPullRequestContributions
                    totalPullRequestReviewContributions
                }
            }
        }
        """

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v4+json",
        }

        response = requests.post(
            self.url,
            data=json.dumps({"query": query, "variables": {"username": username}}),
            headers=headers,
        )

        if response.status_code != 200:
            raise Exception(f"GitHub API request failed: {response.text}")

        data = response.json()
        return data["data"]["user"]
