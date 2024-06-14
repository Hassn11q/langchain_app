from fastapi import FastAPI
from langserve import add_routes
import uvicorn
from chain import chain

# initiate the app
app = FastAPI(
    title="LangChain Server",
    version = "1.0" , 
    description="LangChain Server for FastAPI"
)
# add routes
add_routes(app , chain , path= "/chatbot")

# run the app
if __name__ == "__main__":
    uvicorn.run(app , host= "localhost", port= 8000)
