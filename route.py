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
    is_private: bool
    points: List["RoutePoint"] = Relationship(back_populates="route")
    photos: List["RoutePhoto"] = Relationship(back_populates="route")

class RoutePoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    route_id: Optional[int] = Field(default=None, foreign_key="route.id")
    route: Optional[Route] = Relationship(back_populates="points")

class RoutePhoto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: Optional[str] = None
    route_id: Optional[int] = Field(default=None, foreign_key="route.id")
    route: Optional[Route] = Relationship(back_populates="photos")






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

#создание маршрута
@app.post("/create_route/", response_model=Route)
def create_route(route: Route):
    with Session(engine) as session:
        session.add(route)
        session.commit()
        session.refresh(route)
    return route

#создание фото к маршруту
@app.post("/routes/{route_id}/images/", response_model=RoutePhoto)
def create_route_image(route_id: int, route_photo: RoutePhoto):
    route_photo.route_id = route_id
    with Session(engine) as session:
        route = session.get(Route, route_id)
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        session.add(route_photo)
        session.commit()
        session.refresh(route_photo)
    return route_photo

#создание точек к маршруту
@app.post("/routes/{route_id}/points/", response_model=RoutePoint)
def create_route_point(route_id: int, route_point: RoutePoint):
    route_point.route_id = route_id
    with Session(engine) as session:
        route = session.get(Route, route_id)
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        session.add(route_point)
        session.commit()
        session.refresh(route_point)
    return route_point


# if (__name__ == "__main__"):
#     uvicorn.run("main:app", reload=True)




