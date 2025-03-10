import random

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from lib.github import GithubClient
from lib.llm import (
    create_comment_description,
    create_contribution_description,
    create_description,
    create_issue_description,
    CardType as LLMCardType,
)
from lib.storage import get_download_url, upload_image_to_bucket
from models.db import Base
from config import GITHUB_PAT

load_dotenv()


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="cards")
    s3_uri = Column(String)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "base_card",
    }

    def __init__(self, user: "User"):
        username = user.username
        self.user_stats = GithubClient(token=GITHUB_PAT).fetch_user_stats(username=username)
        self.name = self.user_stats["name"]
        self.pull_requests = self.user_stats["pullRequests"]["totalCount"]
        self.issues = self.user_stats["issues"]["totalCount"]
        self.total_commits = self.user_stats["contributionsCollection"]["contributionCalendar"][
            "totalContributions"
        ]
        self.comments = self.user_stats["contributionsCollection"][
            "totalPullRequestReviewContributions"
        ]
        self.email = self.user_stats["email"]
        self.stars = sum(
            [repo["stargazerCount"] for repo in self.user_stats["repositories"]["nodes"]]
        )
        self.user = user

    def to_dict(self):
        return {
            "id": self.id,
            "s3_uri": get_download_url(self.s3_uri),
            "created_at": self.created_at,
        }

    def get_primary_languages(self):
        languages = {}
        colors = {}
        for repo in self.user_stats["repositories"]["nodes"]:
            if repo["primaryLanguage"]:
                languages[repo["primaryLanguage"]["name"]] = (
                    languages.get(repo["primaryLanguage"]["name"], 0) + 1
                )

                colors[repo["primaryLanguage"]["name"]] = repo["primaryLanguage"]["color"]
        # Sort languages by frequency and return list
        sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)

        languages = [lang[0] for lang in sorted_languages]
        return languages

    def _add_heading(self, image: Image, text: str):
        blank_image = Image.new("RGBA", (630, 92), (0, 0, 0, 0))

        font_size = 48
        font = ImageFont.truetype("static/Roboto/Roboto-Medium.ttf", font_size)
        draw = ImageDraw.Draw(blank_image)

        draw.text((0, 0), text, font=font, fill="#fefefe")

        x_coord = (
            570
            if self.stars < 10
            else (
                550
                if self.stars < 100
                else (
                    520
                    if self.stars < 1000
                    else (500 if self.stars < 10000 else (480 if self.stars < 100_000 else 460))
                )
            )
        )
        github_logo = Image.open("static/star.png")
        github_logo = github_logo.resize((36, 36))
        blank_image.paste(github_logo, (x_coord - 48, 10))

        draw.text(
            (x_coord, 0),
            f"{self.stars}",
            font=font,
            fill="#fefefe",
            align="right",
        )
        blank_image = blank_image.convert("RGBA")

        image.alpha_composite(blank_image, (84, 61))

    def _add_github_username(self, image: Image, text: str):
        font_size = 32
        font = ImageFont.truetype("static/Roboto/Roboto-Medium.ttf", font_size)
        blank_image = Image.new("RGBA", (700, 40), (0, 0, 0, 0))
        github_logo = Image.open("static/github_logo.png")
        github_logo = github_logo.resize((33, 33))
        username = f"@{text}"
        draw_blank = ImageDraw.Draw(blank_image)
        draw_blank.text((0, 0), username, font=font, fill="#fefefe")
        github_logo_x = 18 * len(username)
        blank_image.paste(github_logo, (github_logo_x, 3))
        # Convert blank_image to RGBA if it isn't already
        blank_image = blank_image.convert("RGBA")

        # Instead of paste, use alpha_composite to overlay the images
        image.alpha_composite(blank_image, (88, 560))

    def _add_description(self, image: Image, text: str):
        font_size = 24
        font = ImageFont.truetype("static/Roboto/Roboto-Regular.ttf", font_size)
        draw = ImageDraw.Draw(image)

        # Calculate text wrapping
        max_width = 630  # Available width for text
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width = draw.textlength(word + " ", font=font)
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(" ".join(current_line))

        # Draw wrapped text
        y = 620
        line_height = font_size * 1.2  # Add some spacing between lines
        for line in lines:
            draw.text((90, y), line, font=font, fill="#fefefe")
            y += line_height

    def _add_issues(self, image: Image, text: str):
        blank_image = Image.new("RGBA", (630, 92), (0, 0, 0, 0))
        # Add PR icons
        issue_icon = Image.open("static/issue.png")
        issue_icon = issue_icon.resize((42, 42))
        if self.issues < 10:  # 1
            blank_image.paste(issue_icon, (30, 20))
        elif self.issues < 50:  # 2
            blank_image.paste(issue_icon, (0, 20))
            blank_image.paste(issue_icon, (56, 20))
        elif self.issues < 100:  # 3
            blank_image.paste(issue_icon, (0, 0))
            blank_image.paste(issue_icon, (56, 0))
            blank_image.paste(issue_icon, (30, 50))
        else:  # 4
            blank_image.paste(issue_icon, (0, 0))
            blank_image.paste(issue_icon, (56, 0))
            blank_image.paste(issue_icon, (0, 50))
            blank_image.paste(issue_icon, (56, 50))

        # Add PR text
        font_size = 24
        font = ImageFont.truetype("static/Roboto/Roboto-Bold.ttf", font_size)
        draw = ImageDraw.Draw(blank_image)
        draw.text((160, 10), "Issues", font=font, fill="#fefefe")

        font = ImageFont.truetype("static/Roboto/Roboto-Regular.ttf", font_size)
        draw.text((160, 48), text, font=font, fill="#fefefe")

        # Add PR count
        font_size = 48
        font = ImageFont.truetype("static/Roboto/Roboto-Medium.ttf", font_size)
        draw = ImageDraw.Draw(blank_image)

        x_coord = (
            590
            if self.issues < 10
            else (
                560
                if self.issues < 100
                else (530 if self.issues < 1000 else (510 if self.issues < 10000 else 490))
            )
        )
        draw.text((x_coord, 10), f"{self.issues}", font=font, fill="#fefefe", align="right")
        image.alpha_composite(blank_image, (90, 970))

    def _add_comments(self, image: Image, text: str):
        blank_image = Image.new("RGBA", (630, 92), (0, 0, 0, 0))
        # Add PR icons
        comment_icon = Image.open("static/comment.png")
        comment_icon = comment_icon.resize((42, 42))
        if self.comments < 10:  # 1
            blank_image.paste(comment_icon, (30, 20))
        elif self.comments < 50:  # 2
            blank_image.paste(comment_icon, (0, 20))
            blank_image.paste(comment_icon, (56, 20))
        elif self.comments < 100:  # 3
            blank_image.paste(comment_icon, (0, 0))
            blank_image.paste(comment_icon, (56, 0))
            blank_image.paste(comment_icon, (30, 50))
        else:  # 4
            blank_image.paste(comment_icon, (0, 0))
            blank_image.paste(comment_icon, (56, 0))
            blank_image.paste(comment_icon, (0, 50))
            blank_image.paste(comment_icon, (56, 50))

        # Add PR text
        font_size = 24
        font = ImageFont.truetype("static/Roboto/Roboto-Bold.ttf", font_size)
        draw = ImageDraw.Draw(blank_image)
        draw.text((160, 10), "Comments", font=font, fill="#fefefe")

        font = ImageFont.truetype("static/Roboto/Roboto-Regular.ttf", font_size)
        draw.text((160, 48), text, font=font, fill="#fefefe")

        # Add PR count
        font_size = 48
        font = ImageFont.truetype("static/Roboto/Roboto-Medium.ttf", font_size)
        draw = ImageDraw.Draw(blank_image)

        x_coord = (
            590
            if self.comments < 10
            else (
                560
                if self.comments < 100
                else (530 if self.comments < 1000 else (510 if self.comments < 10000 else 490))
            )
        )
        draw.text((x_coord, 10), f"{self.comments}", font=font, fill="#fefefe", align="right")
        image.alpha_composite(blank_image, (90, 850))

    def _add_contributions(self, image: Image, text: str):
        blank_image = Image.new("RGBA", (630, 92), (0, 0, 0, 0))
        # Add PR icons
        pr_icons = Image.open("static/pullrequest.png")
        pr_icons = pr_icons.resize((42, 42))
        if self.total_commits < 10:  # 1
            blank_image.paste(pr_icons, (30, 20))
        elif self.total_commits < 50:  # 2
            blank_image.paste(pr_icons, (0, 20))
            blank_image.paste(pr_icons, (56, 20))
        elif self.total_commits < 100:  # 3
            blank_image.paste(pr_icons, (0, 0))
            blank_image.paste(pr_icons, (56, 0))
            blank_image.paste(pr_icons, (30, 50))
        else:  # 4
            blank_image.paste(pr_icons, (0, 0))
            blank_image.paste(pr_icons, (56, 0))
            blank_image.paste(pr_icons, (0, 50))
            blank_image.paste(pr_icons, (56, 50))

        # Add PR text
        font_size = 24
        font = ImageFont.truetype("static/Roboto/Roboto-Bold.ttf", font_size)
        draw = ImageDraw.Draw(blank_image)
        draw.text((160, 10), "Contributions", font=font, fill="#fefefe")

        font = ImageFont.truetype("static/Roboto/Roboto-Regular.ttf", font_size)
        draw.text((160, 48), text, font=font, fill="#fefefe")

        # Add PR count
        font_size = 48
        font = ImageFont.truetype("static/Roboto/Roboto-Medium.ttf", font_size)
        draw = ImageDraw.Draw(blank_image)

        x_coord = (
            590
            if self.total_commits < 10
            else (
                560
                if self.total_commits < 100
                else (
                    530
                    if self.total_commits < 1000
                    else (510 if self.total_commits < 10000 else 490)
                )
            )
        )
        draw.text(
            (x_coord, 10),
            f"{self.total_commits}",
            font=font,
            fill="#fefefe",
            align="right",
        )
        image.alpha_composite(blank_image, (90, 730))

    def _add_avatar(self, image: Image, avatar_url: str):
        avatar = Image.open(avatar_url)
        # Get dimensions of avatar
        width, height = avatar.size

        # Calculate dimensions for center crop
        target_aspect_ratio = 610 / 344
        current_aspect_ratio = width / height

        if current_aspect_ratio > target_aspect_ratio:
            # Image is wider than needed
            new_width = int(height * target_aspect_ratio)
            left = (width - new_width) // 2
            right = left + new_width
            top = 0
            bottom = height
        else:
            # Image is taller than needed
            new_height = int(width / target_aspect_ratio)
            top = (height - new_height - 100) // 2
            bottom = top + new_height
            left = 0
            right = width

        # Crop to target aspect ratio from center
        avatar = avatar.crop((left, top, right, bottom))

        # Resize to exact dimensions
        avatar = avatar.resize((612, 348))
        # Convert avatar to RGBA mode to ensure compatibility
        avatar = avatar.convert("RGBA")
        image.alpha_composite(avatar, (94, 147))

    def _generate_card(
        self, base_card: str, avatar: str, card_type: LLMCardType = LLMCardType.NORMAL
    ):
        image = Image.open(base_card)
        image = image.resize((812, 1132))
        self._add_heading(image, self.name.split(" ")[0])
        self._add_avatar(image, avatar)
        self._add_github_username(image, self.user.username)
        self._add_description(image, create_description(self, card_type))
        self._add_contributions(image, create_contribution_description(self, card_type))
        self._add_comments(image, create_comment_description(self, card_type))
        self._add_issues(image, create_issue_description(self, card_type))
        self.s3_uri = upload_image_to_bucket(image)

        return image

    def _get_avatar(self):
        avatars = [
            "static/cat.png",
            "static/dog.png",
            "static/fluffy.png",
            "static/hamster.png",
            "static/shark.png",
        ]
        return random.choice(avatars)


class YellowCard(Card):
    __mapper_args__ = {
        "polymorphic_identity": "yellow_card",
    }

    def __init__(self, user: "User"):
        super().__init__(user)
        self._generate_card("static/yellow.png", self._get_avatar())
        return self


class BlueCard(Card):
    __mapper_args__ = {
        "polymorphic_identity": "blue_card",
    }

    def __init__(self, user: "User"):
        super().__init__(user)
        self._generate_card("static/blue.png", self._get_avatar())
        return self


class GreenCard(Card):
    __mapper_args__ = {
        "polymorphic_identity": "green_card",
    }

    def __init__(self, user: "User"):
        super().__init__(user)
        self._generate_card("static/green.png", self._get_avatar())
        return self


class OrangeCard(Card):
    __mapper_args__ = {
        "polymorphic_identity": "orange_card",
    }

    def __init__(self, user: "User"):
        super().__init__(user)
        self._generate_card("static/orange.png", self._get_avatar())
        return self


class PurpleCard(Card):
    __mapper_args__ = {
        "polymorphic_identity": "purple_card",
    }

    def __init__(self, user: "User"):
        super().__init__(user)
        self._generate_card("static/purple.png", self._get_avatar())
        return self


class RoastCard(Card):
    __mapper_args__ = {
        "polymorphic_identity": "roast_card",
    }

    def __init__(self, user: "User"):
        super().__init__(user)
        self._generate_card("static/roast.png", "static/catinfire.png", LLMCardType.ROAST)
        return self
