from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from config import STAGE
from models import User, get_db, Card
from lib.llm import CardType

load_dotenv()


app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        ["https://devleague.io"] if STAGE == "production" else ["http://localhost:5174"]
    ),
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# app.include_router(auth_router)


@app.get("/healthcheck")
async def read_root():
    return {"Hello": "World"}


@app.get("/static/{image_name}")
async def get_image(image_name: str):
    file_path = f"static/{image_name}"
    return FileResponse(file_path)


@app.get("/api/count")
async def get_count():
    with get_db() as db:
        return {"count": db.query(Card).count()}


@app.post("/api/generate_card/{username}")
async def generate_card(request: Request, username: str):
    body = await request.json()
    card_type = CardType(body.get("type", CardType.NORMAL))
    with get_db() as db:
        try:
            user = db.query(User).filter(User.username == username.lower()).first()
            if user is None:
                user = User(username=username.lower())
                db.add(user)
            card = user.generate_card(card_type=card_type)
            db.add(card)
            db.commit()
            return card.to_dict()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
