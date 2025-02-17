from typing import List, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from datetime import datetime

app = FastAPI()

class Route(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    region: str
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

class RouteUpdate(SQLModel):
    title: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None
    is_private: Optional[bool] = None

class RoutePointUpdate(SQLModel):
    latitude: float
    longitude: float
    
class RoutePhotoUpdate(SQLModel):
    url: Optional[str] = None

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
@app.get("/images/", response_model=List[RoutePhoto])
def read_images():
    with Session(engine) as session:
        images = session.exec(select(RoutePhoto)).all()
        return images

@app.get("/points/", response_model=List[RoutePoint])
def read_points():
    with Session(engine) as session:
        points = session.exec(select(RoutePoint)).all()
        return points
    
#создание маршрута

@app.post("/create_route/", response_model=Route)
def create_route(route: Route):
    with Session(engine) as session:
        session.add(route)
        session.commit()
        session.refresh(route)
    return route
#создание фото к маршруту
@app.post("/images/{route_id}", response_model=RoutePhoto)
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
@app.post("/points/{route_id}", response_model=RoutePoint)
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
#удаление маршрута
@app.delete("/routes/{route_id}", response_model=Route)
def delete_route(route_id: int):
    with Session(engine) as session:
        route = session.get(Route, route_id)
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        session.delete(route)
        session.commit()
        return route

#удаление точки маршрута
@app.delete("/route_points/{point_id}", response_model=RoutePoint)
def delete_route_point(point_id: int):
    with Session(engine) as session:
        point = session.get(RoutePoint, point_id)
        if not point:
            raise HTTPException(status_code=404, detail="RoutePoint not found")
        session.delete(point)
        session.commit()
        return point

#удаление фотографии маршрута
@app.delete("/route_photos/{photo_id}", response_model=RoutePhoto)
def delete_route_photo(photo_id: int):
    with Session(engine) as session:
        photo = session.get(RoutePhoto, photo_id)
        if not photo:
            raise HTTPException(status_code=404, detail="RoutePhoto not found")
        session.delete(photo)
        session.commit()
        return photo

@app.patch("/routes/{route_id}", response_model=Route)
def update_route(route_id: int, route: RouteUpdate):
    with Session(engine) as session:
        db_route = session.get(Route, route_id)
        if not db_route:
            raise HTTPException(status_code=404, detail="Route not found")
        route_data = route.dict(exclude_unset=True)
        for key, value in route_data.items():
            setattr(db_route, key, value)
        session.add(db_route)
        session.commit()
        session.refresh(db_route)
        return db_route




@app.patch("/route_photos/{photo_id}", response_model=RoutePhoto)
def update_photos(photo_id: int, route: RoutePhotoUpdate):
    with Session(engine) as session:
        db_photo = session.get(RoutePhoto, photo_id)
        if not db_photo:
            raise HTTPException(status_code=404, detail="Route not found")
        route_data = route.dict(exclude_unset=True)
        for key, value in route_data.items():
            setattr(db_photo, key, value)
        session.add(db_photo)
        session.commit()
        session.refresh(db_photo)
        return db_photo


@app.patch("/route_point/{point_id}", response_model=RoutePoint)
def update_point(point_id: int, route: RoutePointUpdate):
    with Session(engine) as session:
        db_point = session.get(RoutePoint, point_id)
        if not db_point:
            raise HTTPException(status_code=404, detail="Route not found")
        route_data = route.dict(exclude_unset=True)
        for key, value in route_data.items():
            setattr(db_point, key, value)
        session.add(db_point)
        session.commit()
        session.refresh(db_point)
        return db_point

# if (__name__ == "__main__"):
#     uvicorn.run("main:app", reload=True)
