# backend/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import components from the current package (backend) directly.
# This works because you are running uvicorn from the 'backend' directory.
from backend.database import Base, engine, get_db
from backend import models # Imports the models module
from backend.routes import auth, wallet # Imports the auth and wallet routers from the routes subpackage

# Create the FastAPI app instance
app = FastAPI(title="Crypto Arbitrage Backend")

# Enable CORS (Cross-Origin Resource Sharing)
# This is CRUCIAL for your frontend (running on port 5500) to communicate with your backend (on port 8000).
origins = [
    "http://127.0.0.1:5500",  # Allow your frontend's specific origin
    "http://localhost:5500",  # Allow localhost if used
    "null" # Often needed if you're opening the HTML file directly from disk (file://)
]

app.add_middleware(
    CORSMiddleware,
    # For development, allow all origins is simpler: allow_origins=["*"]
    # For production, strictly define your frontend origins as in the `origins` list above.
    allow_origins=["*"], # Allowing all for initial testing, change for production!
    allow_credentials=True, # Allow cookies, authorization headers, etc.
    allow_methods=["*"],    # Allow all HTTP methods (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],    # Allow all headers (like Content-Type, Authorization)
)

# Create all database tables defined in models.py
# This will create 'db.sqlite3' if it doesn't exist and define the tables.
Base.metadata.create_all(bind=engine)

# Include API routers
# The `prefix` adds a common path segment to all routes in the router.
# The `tags` are used for grouping endpoints in the OpenAPI (Swagger UI) documentation.
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(wallet.router, prefix="/wallets", tags=["Wallets"])

# Root test endpoint to check if the backend is running
@app.get("/")
def root():
    return {"message": "Crypto Arbitrage Backend is running"}

# Development-only endpoint to list all users (useful for debugging)
@app.get("/debug/users")
def get_users(db: Session = Depends(get_db)):
    # Access User model via `models.User` because we did `import models`
    return db.query(models.User).all()

# Main entry point for running the application with Uvicorn
if __name__ == "__main__":
    import uvicorn
    # This runs the FastAPI application using Uvicorn.
    # --host 127.0.0.1 binds to your local machine.
    # --port 8000 sets the port.
    # --reload enables auto-reloading on code changes (great for development).
    uvicorn.run(app, host="127.0.0.1", port=8000)