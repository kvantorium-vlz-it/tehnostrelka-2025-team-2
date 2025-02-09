from typing import *
import uvicorn
from fastapi import *
from sqlmodel import *
from typing import *
from datetime import *

app = FastAPI()


class Route(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    creator: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    created_at: str
    is_private: bool
    points: List["RoutePoint"] = Relationship(back_populates="route")


class RouteImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    photo_url: Optional[str] = None
    photo_id: Optional[int] = Field(default=None, foreign_key="photo.id")




class RoutePoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    route_id: Optional[int] = Field(default=None, foreign_key="route.id")
    route: Optional[Route] = Relationship(back_populates="points")






engine = create_engine("sqlite:///database.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#вывожу все route

@app.get("/routes/", response_model=List[Route])
def read_routes():
    with Session(engine) as session:
        routes = session.exec(select(Route)).all()
        return routes



# if (__name__ == "__main__"):
#     uvicorn.run("main:app", reload=True)




