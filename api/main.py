from email.message import EmailMessage
import smtplib
import threading
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
import shutil
import os
import zipfile
from src.visual_insights_crew.crew import VisualInsightsCrewCrew

app = FastAPI()

# Endpoint to trigger CrewAI run
@app.post("/run")
async def run_crew(request: Request, background_tasks: BackgroundTasks):
    inputs = await request.json() if request.headers.get("content-type") == "application/json" else {}

    # Add a background task to handle the crew and email
    background_tasks.add_task(run_crew_in_thread, inputs)

    # Return immediately, while the background task runs in the background
    return {"result": "Request is being processed in the background."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, debug=True)

def run_crew_in_thread(inputs):
    try:
        thread = threading.Thread(target=run_crew_task, args=(inputs,))
        thread.start()
    except Exception as e:
        print(f"Failed to start thread: {str(e)}")

def run_crew_task(inputs):
    try:
        niche = inputs.get("niche")
        email = inputs.get("email")
        platform = inputs.get("platform")

        if not niche or not platform or not email:
            raise HTTPException(status_code=400, detail="Missing required parameters: 'niche', 'platform', or 'email'")

        crew = VisualInsightsCrewCrew(inputs={"niche": niche, "email": email, "platform": platform})
        crew.crew().kickoff(inputs={"niche": niche, "email": email, "platform": platform})

        results_directory = f"tmp/{email}_{niche}_{platform}"

        if not os.path.exists(results_directory):
            raise HTTPException(status_code=500, detail="Results directory not found")

        zip_file_path = f"tmp/{email}_{niche}_{platform}_insights.zip"
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for root, _, files in os.walk(results_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, results_directory))

        shutil.rmtree(results_directory)
        send_email_with_attachment(email, zip_file_path)

    except Exception as e:
        print(f"Error in run_crew_task: {str(e)}")

def send_email_with_attachment(email, attachment_path):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Your Viral Insights AI Report'
        msg['From'] = 'support@viralinsightsai.com'
        msg['To'] = email
        msg['Bcc'] = 'tpdoye87@gmail.com'
        msg.set_content('Please find attached the Viral Insights AI report you requested.')

        # Attach the file
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='zip', filename=file_name)

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('tpdoyle87@gmail.com', os.getenv('GMAIL_APP_PASSWORD'))
            smtp.send_message(msg)
        # shutil.rmtree(attachment_path)

    except Exception as e:
        print(f"Failed to send email: {str(e)}")