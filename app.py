from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional

# Create FastAPI app
app = FastAPI()

# Allow all origins to make requests to the server (for CORS support)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET"],  # Allows only GET requests
    allow_headers=["*"],
)

# Read the CSV data into a pandas DataFrame
df = pd.read_csv("students.csv")

# Convert DataFrame to a list of dictionaries (JSON-like format)
students_data = df.to_dict(orient="records")

@app.get("/api")
async def get_students(
    class_: Optional[List[str]] = Query(None, alias="class")
):
    """
    This endpoint serves the student data.

    - If `class` is provided in the query parameters, filter students by class.
    - Returns the list of students as a JSON response.
    """
    # Log the received class_ parameter to debug
    print(f"Received classes to filter: {class_}")
    
    if class_:
        # Filter students based on the provided classes
        filtered_students = [
            student for student in students_data if student["class"] in class_
        ]
    else:
        # Return all students if no `class_` parameter is provided
        filtered_students = students_data

    return {"students": filtered_students}
