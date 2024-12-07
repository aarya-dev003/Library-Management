from fastapi.middleware.cors import CORSMiddleware


#database using sqlalchemy no longer needed because of alembic
# models.Base.metadata.create_all(bind=engine)


def add_cors_middleware(app):

    #allowed cors origins
    origins = [
        "*"
    ]


            
    #CORS Headers
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )