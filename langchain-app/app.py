from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
import uvicorn
from chain import chain

# initiate the app
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="LangChain Server for FastAPI"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add routes
add_routes(app, chain, path="/chatbot")

# run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
