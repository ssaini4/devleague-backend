import random

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.card import BlueCard, GreenCard, OrangeCard, PurpleCard, YellowCard, RoastCard
from models.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # One-to-one relationship with GitHubAuth
    cards = relationship("Card", back_populates="user")

    def generate_card(self, card_type=None):
        if card_type == "ROAST":
            return RoastCard(self)

        # Existing random card logic for NORMAL type
        card_classes = [YellowCard, BlueCard, GreenCard, OrangeCard, PurpleCard]
        card_class = random.choice(card_classes)
        return card_class(self)
