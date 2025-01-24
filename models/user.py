import random

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.card import BlueCard, GreenCard, OrangeCard, PurpleCard, YellowCard
from models.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # One-to-one relationship with GitHubAuth
    github_auth = relationship("GitHubAuth", back_populates="user", uselist=False)
    cards = relationship("Card", back_populates="user")

    def generate_card(self):

        card_types = {1: YellowCard, 2: BlueCard, 3: OrangeCard, 4: PurpleCard, 5: GreenCard}

        choice = random.randint(1, len(card_types))
        card_class = card_types[choice]

        # Check if user already has this type of card
        existing_card = next((card for card in self.cards if isinstance(card, card_class)), None)
        if existing_card:
            return existing_card

        # Create new card if none exists
        return card_class(self)
