"""
This is the main entry point for the Booking Authentication Service.
It uses FastAPI, a modern, fast Python web framework for building APIs.
"""

# Import the FastAPI class from the fastapi package
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import text
from app.database import engine , SessionLocal
from sqlalchemy.orm import Session
from app.models import User



# 'app' is an instance of the FastAPI class.
# This 'app' object represents our actual web application.
# It handles incoming HTTP requests, routes them to the correct functions, 
# and returns the responses. We attach routes to it using decorators (like @app.get).
app=FastAPI()


# We define a Pydantic model (LoginRequest) to specify the shape of the data we expect.
# FastAPI will automatically validate incoming JSON against this model.
# If a client forgets to send an 'email' or 'password', FastAPI throws an automatic error.
class LoginRequest(BaseModel):
    email: str
    password: str
# The @app.get("/") decorator tells FastAPI that the function below it (root) 
# is responsible for handling HTTP GET requests that go to the root URL ("/").


@app.get("/")
def root():
    # Return a simple dictionary. FastAPI will automatically convert this 
    # to a JSON response and send it back to the client.
    return {
        "message": "Booking Auth Service is running"
    }

# The @app.post("/login") decorator tells FastAPI that the login function
# should handle HTTP POST requests made to the "/login" endpoint.
# POST requests are typically used when clients submit data (like a username/password).
@app.post("/login")
def login(request:LoginRequest):
    # For now, this just returns a hardcoded success message.
    # Eventually, it will take the credentials, verify them, and return a token.
    return {
        "message": "Login request received by Auth Service",
        "email": request.email
    }

@app.get("/health/db")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as error:
        return {
            "database": "not connected",
            "error": str(error),
        }

# Dependency helper function to provide a database session for a single request
# It yields a session to the endpoint and guarantees it will be closed afterwards
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# The @app.get("/users/{email}") decorator defines a dynamic route
# '{email}' is a path parameter that will be passed directly into the get_user function
@app.get("/users/{email}")
def get_user(email: str, db: Session = Depends(get_db)):
    # Depends(get_db) tells FastAPI to run the get_db function and pass the yielded session into 'db'
    
    # We use SQLAlchemy's query builder to search for a user matching the requested email
    # .first() ensures we return a single object, not a list
    user = db.query(User).filter(User.email == email).first()
    
    # If the database returns None (user doesn't exist), we raise a 404 Not Found error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' not found",
        )
    # FastAPI automatically serializes the SQLAlchemy User object into JSON and sends it back
    return user