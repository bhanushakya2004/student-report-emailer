from fastapi import FastAPI
from pydantic import BaseModel
from app.gmail_service import send_email_via_gmail
from app.google_sheets import fetch_marks_from_sheet
from app.utils import analyze_marks_with_ai, generate_report_card

app = FastAPI()

class SheetRequest(BaseModel):
    sheet_id: str

@app.post("/upload_marks/")
async def upload_marks(request: SheetRequest):
    sheet_id = request.sheet_id  # Extract sheet_id from JSON request

    # Fetch marks data from Google Sheets
    marks_data = fetch_marks_from_sheet(sheet_id)
    
    for student in marks_data:
        student_name = student["Name"]
        email = student["Email"]

        # Convert student marks into a dictionary
        subjects_marks = {key: value for key, value in student.items() if key not in ["Name", "Email"]}
        
        # Analyze marks using AI
        analysis = analyze_marks_with_ai(student_name, subjects_marks)

        # Generate report card
        report_card = generate_report_card(student_name, subjects_marks, analysis)

        # Send email to the student
        send_email_via_gmail(email, "Your Report Card", report_card)
    
    return {"message": "Emails sent successfully!"}
