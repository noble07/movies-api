from fastapi import APIRouter
from fastapi import Path, Query, Response, Depends
from fastapi.responses import JSONResponse
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares import JWTBearer
from services.movie import MovieService
from schemas import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> list[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return jsonable_encoder(result)

@movie_router.get('/movies/{id}', tags=['movies'], status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)):
    db = Session()
    result = MovieService(db).get_movies(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies/', tags=['movies'], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    MovieService(db).create_movie(movie)

    return {"message": "Se ha registrado la pelicula"}

@movie_router.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie, response: Response):
    db = Session()
    result = MovieService(db).get_movies(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    MovieService(db).update_movie(id, movie)

    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

@movie_router.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Eliminado"})
