from sqlmodel import *
from typing import *
import datetime


class Route(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    creator: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now(), nullable=False)
    is_private: bool
    photo_url: Optional[str] = None
    points: List["RoutePoint"] = Relationship(back_populates="route")


class RoutePoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    route_id: Optional[int] = Field(default=None, foreign_key="route.id")
    route: Optional[Route] = Relationship(back_populates="points")



engine = create_engine("sqlite:///database.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

create_db_and_tables() 

#
def add_sample_data():
    with Session(engine) as session:
        route1 = Route(
            title="Mountain Hike",
            description="A beautiful hike through the mountains.",
            creator="Alice",
            # created_at=1622505600, 
            is_private=False,
            photo_url="http://example.com/photo1.jpg"
        )
        
        route2 = Route(
            title="City Tour",
            description="An entertaining tour of the city's highlights.",
            creator="Bob",
            # created_at=1622505601,
            is_private=False,
            photo_url="http://example.com/photo2.jpg"
        )

        session.add(route1)
        session.add(route2)

        session.commit()

        point1 = RoutePoint(latitude=40.7128, longitude=-74.0060, route_id=route1.id)
        point2 = RoutePoint(latitude=40.7306, longitude=-73.9352, route_id=route1.id)
        
        point3 = RoutePoint(latitude=34.0522, longitude=-118.2437, route_id=route2.id)
        point4 = RoutePoint(latitude=34.0522, longitude=-118.2439, route_id=route2.id)

        session.add(point1)
        session.add(point2)
        session.add(point3)
        session.add(point4)

        session.commit()

def print_database_contents():
    with Session(engine) as session:
        routes = session.exec(select(Route)).all()
        for route in routes:
            print(f"Route ID: {route.id}, Title: {route.title}, Description: {route.description}, Creator: {route.creator}, Created At: {route.created_at}, Private: {route.is_private}, Photo URL: {route.photo_url}")
            for point in route.points:
                print(f"   RoutePoint ID: {point.id}, Latitude: {point.latitude}, Longitude: {point.longitude}")
        for route in routes:
            print(f"Route ID: {route.id}, Title: {route.title}, Description: {route.description}, Creator: {route.creator}, Created At: {route.created_at}, Private: {route.is_private}, Photo URL: {route.photo_url}")

            print(f"   RoutePoint ID: {point.id}, Latitude: {point.latitude}, Longitude: {point.longitude}")

add_sample_data()
print_database_contents()

print()