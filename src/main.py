#from fastapi import FastAPI

#app = FastAPI()


#@app.get("/")
#async def root():
#    return {"message": "Hello World",
#            "group": "4"
#           }

# main.py

# main.py

from fastapi import FastAPI
from routes.route import router

app = FastAPI()

app.include_router(router)
