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
from fastapi.middleware.cors import CORSMiddleware
import streamlit as st
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Define FastAPI server URL
FASTAPI_URL = "http://localhost:8000"

def main():
    st.title("FastAPI and MongoDB with Streamlit")

    st.sidebar.header("Menu")
    menu = st.sidebar.radio("Navigate", ["Home", "View Items", "Add Item"])

    if menu == "Home":
        st.write("Welcome to the FastAPI and MongoDB with Streamlit App!")

    elif menu == "View Items":
        st.subheader("View Items")
        response = requests.get(f"{FASTAPI_URL}/")
        if response.status_code == 200:
            items = response.json()
            i=0
            for item in items:
                i += 1
                st.write(f"Database record - {i}, Name: {item['name']}, Description: {item['description']}")
        else:
            st.error("Failed to fetch items!")

    elif menu == "Add Item":
        st.subheader("Add Item")
        name = st.text_input("Name")
        description = st.text_input("Description")
        if st.button("Add"):
            new_item = {"name": name, "description": description}
            response = requests.post(f"{FASTAPI_URL}/", json=new_item)
            if response.status_code == 200:
                st.success("Item added successfully!")
            else:
                st.error("Failed to add item!")

if __name__ == "__main__":
    main()
