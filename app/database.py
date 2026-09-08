import os  # Imports the os module for environment variable access
from dotenv import load_dotenv  # Imports the load_dotenv function to read a .env file
from sqlalchemy import create_engine  # Imports create_engine to establish a connection to the database
from sqlalchemy.orm import declarative_base, sessionmaker  # Imports ORM tools for mapping classes to tables and managing sessions

# Load environment variables from .env file
load_dotenv()  # Actually loads the variables from the .env file into the system environment

# Database credentials
DB_HOST = os.getenv("DB_HOST")  # Retrieves the database host address
DB_PORT = os.getenv("DB_PORT", "3306")  # Retrieves the database port, defaulting to 3306
DB_NAME = os.getenv("DB_NAME")  # Retrieves the database name
DB_USER = os.getenv("DB_USER")  # Retrieves the database user name
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Retrieves the database password

# SQLAlchemy connection string
DATABASE_URL = (  # Starts the definition of the connection URL
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # Formats the credentials into a connection string for pymysql
)

# Engine setup
engine = create_engine(  # Creates the database engine, the core interface to the database
    DATABASE_URL,  # Passes the connection string to the engine
    pool_pre_ping=True,  # Recommended: checks connection validity before executing queries (prevents stale connection errors)
)

# Session factory
SessionLocal = sessionmaker(  # Creates a configured class for generating new Session objects
    autocommit=False,  # Disables automatic commits, requiring manual db.commit()
    autoflush=False,  # Disables automatic flushing of pending changes to the database before queries
    bind=engine,  # Associates these sessions with our created engine
)
#SessionLocal is a factory that creates new, temporary connections (sessions) to your database whenever you need to interact with it.
#Each session is like a conversation with the database. It keeps track of the changes you make, 
#tracks which rows you’ve loaded, and manages transactions (groups of operations that should either all succeed or all fail).

# Declarative base for ORM models
Base = declarative_base()  # Creates a base class that our database models will inherit from


# Dependency helper (useful for FastAPI / Flask routes)
def get_db():  # Defines a generator function to provide a database session
    db = SessionLocal()  # Creates a new database session instance
    try:  # Uses a try block to ensure the session is always closed
        yield db  # Yields the session to the calling function (e.g. a web request)
    finally:  # Ensures the following code runs no matter what happens in the try block
        db.close()  # Closes the session and returns the connection to the pool


# SQL Alchemy (ORM)

# Instead of writing raw SQL like SELECT * FROM users WHERE id = 1, SQLAlchemy lets you interact with your database using Python classes and objects
# If you start building your application using MySQL, but later decide you need to switch to PostgreSQL or SQLite (e.g., for local testing), you would normally have to rewrite many of your raw SQL queries because different databases have slightly different syntax.

# You write your code once using SQLAlchemy, and it works with MySQL, PostgreSQL, SQLite, MSSQL, Oracle, and many other databases without you having to rewrite your queries.

# Prevents SQL injection Attack
# Connection Pooling - opening a new connection to a database every time a user makes a request is slow and expensive. SQLAlchemy’s engine automatically manages a "pool" of active database connections.