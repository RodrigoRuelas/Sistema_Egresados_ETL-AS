import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno desde el archivo .env
load_dotenv()

DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "BD_SeguimientoEgresados")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION", "yes")

# Construcción de la cadena de conexión con pyodbc
if DB_TRUSTED_CONNECTION.lower() == "yes":
    # Autenticación de Windows
    DATABASE_URL = f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}?driver={DB_DRIVER.replace(' ', '+')}&trusted_connection=yes"
else:
    # Autenticación por Usuario/Contraseña de SQL Server
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver={DB_DRIVER.replace(' ', '+')}"

# Creación del engine de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Fabrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generador de sesiones para la base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()