# Multi-Model Emotion Detection System

### INTRODUCTION
In the period of human-computer interaction and full of feeling computing, understanding human feelings plays an urgent part in upgrading client involvement and engagement. To address this, our venture points to creating a modern multimodal feeling discovery framework leveraging facial expressions, voice sounds, and literary settings. By joining these different modalities, we look for a comprehensive arrangement capable of precisely recognizing and deciphering human feelings in real time. The system's backbone integrates the LLAMA (or LLAVA) model, a state-of-the-art deep learning architecture designed for multimodal learning tasks. Streamlit, a user-friendly web application framework, is used for the system's front end, providing an intuitive interface for users. MongoDB or Firebase are used for data storage and management, ensuring seamless integration with the emotion detection system. Flask is used for communication between the frontend and backend components, facilitating robust endpoints for data exchange. The project pushes the boundaries of emotion detection technology by leveraging synergies between facial, voice, and textual modalities. By integrating cutting-edge deep learning models, intuitive frontend interfaces, and robust backend infrastructure, the project aims to deliver a powerful multimodal emotion detection system capable of enriching human-computer interactions across various domains, including virtual assistants, social robotics, and affective computing applications.

### [Project Initiation Powerpoint slide] (https://github.com/Oversoul73/DS-Capstone-Spring-2024/blob/main/Presentation.pdf)

### [Project Initiation Document] (https://github.com/Oversoul73/DS-Capstone-Spring-2024/blob/main/Project_Inititation.docx)

## Prerequisites:

1. ### Python 3.11 or later version installed on the manchine.

2. ### MongoDB Atlas/compass account created, and credetnials kept ready.

3. ### VS Code Editor (recommended).

## Installation commnads in VScode Terminal:

1.  ### Install MongoDB Driver:
           python -m pip install "pymongo[srv]"

2. ###  FastAPI installation :
           pip install fastapi

3. ###  Uvicorn installation:
           pip install uvicorn


## Run commnads in VScode Terminal:

1.  ### Run FastAPI:
           uvicorn main:app --reload

2. ###  Run Streamlit:
           streamlit run main.py    
