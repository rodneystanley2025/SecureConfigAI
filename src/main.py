from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Depends, Form
from fastapi.responses import FileResponse # Import FileResponse
from sqlalchemy.orm import Session
from uuid import uuid4
import os
import json # Import json for parsing selected_engines
import traceback # Import traceback
from typing import Dict, Any, List

from src.orchestrator.main import run_scan
from src.database.database import SessionLocal, engine, get_db
from src.database.models import Base, Scan # Import Base and Scan model

# Create database tables if they don't exist
# In a production environment, Alembic handles this. For quick dev, this is convenient.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Scanner",
    description="An AI-powered scanner for configuration files.",
    version="0.1.0",
)

# Create a temporary directory for uploads if it doesn't exist
UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_scan_task(scan_id: str, file_path: str, selected_engines: Dict[str, bool]):
    """Background task to run the scan and store results in the database."""
    db: Session = SessionLocal()
    try:
        scan_record = db.query(Scan).filter(Scan.scan_id == scan_id).first()
        if not scan_record:
            # Should not happen if created in upload_file_for_scan, but for safety
            print(f"Error: Scan record for {scan_id} not found in DB for processing.")
            return

        scan_record.status = "in_progress"
        db.add(scan_record)
        db.commit()
        db.refresh(scan_record)

        results_from_orchestrator = run_scan(file_path, selected_engines)
        scan_record.tool_findings = results_from_orchestrator.get("scan_results", {}).get("tool_findings")
        scan_record.ai_analysis = results_from_orchestrator.get("scan_results", {}).get("ai_analysis")
        scan_record.identified_type = results_from_orchestrator.get("identified_type", "unknown")
        scan_record.status = "completed"
        scan_record.error_message = None # Clear any previous error
    except ValueError as e: # Catch specific errors like missing GEMINI_API_KEY
        scan_record.status = "failed"
        scan_record.error_message = str(e)
        print(f"Scan {scan_id} failed with ValueError: {e}")
    except Exception as e:
        scan_record.status = "failed"
        scan_record.error_message = f"An unexpected error occurred during scan: {e}\n{traceback.format_exc()}"
        print(f"Scan {scan_id} failed with unexpected error: {e}\n{traceback.format_exc()}")
    finally:
        db.add(scan_record)
        db.commit()
        db.refresh(scan_record)
        db.close()
        # Clean up the temporary file after scanning
        if os.path.exists(file_path):
            os.remove(file_path)


@app.get("/", include_in_schema=False) # exclude from OpenAPI docs
async def get_index():
    return FileResponse("index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    # Assuming favicon.ico is in the project root
    favicon_path = "./favicon.ico"
    if not os.path.exists(favicon_path):
        raise HTTPException(status_code=404, detail="favicon.ico not found")
    return FileResponse(favicon_path, media_type="image/x-icon")

@app.post("/scan")
async def upload_file_for_scan(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...),
    selected_engines: str = Form(...), # Accept selected_engines as form data
    db: Session = Depends(get_db)
):
    scan_id = str(uuid4())
    file_location = os.path.join(UPLOAD_DIR, f"{scan_id}_{file.filename}")
    
    # Save the uploaded file
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    
    # Parse selected engines
    parsed_selected_engines = json.loads(selected_engines)

    # Create initial scan record in DB
    new_scan = Scan(
        scan_id=scan_id,
        filename=file.filename,
        identified_type="unknown", # Will be updated by orchestrator
        status="queued"
    )
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    # Add scan to background tasks, passing selected_engines
    background_tasks.add_task(process_scan_task, scan_id, file_location, parsed_selected_engines)
    
    return {"scan_id": scan_id, "message": f"File '{file.filename}' uploaded successfully. Scan queued."}

@app.get("/scan/{scan_id}")
async def get_scan_results(scan_id: str, db: Session = Depends(get_db)):
    scan_record = db.query(Scan).filter(Scan.scan_id == scan_id).first()
    
    if not scan_record:
        raise HTTPException(status_code=404, detail="Scan ID not found.")
    
    # Convert the SQLAlchemy model to a dict for API response
    result_dict = scan_record.to_dict()
    
    # For a completed scan, the 'results' key should contain the full scan data
    # For failed, it should contain the error message
    if scan_record.status == "completed":
        return {"scan_id": scan_id, "status": scan_record.status, "results": result_dict}
    elif scan_record.status == "failed":
        # The frontend expects 'error' key for failed scans
        return {"scan_id": scan_id, "status": scan_record.status, "error": scan_record.error_message}
    else:
        # For queued or in_progress, return status and a message
        return {"scan_id": scan_id, "status": scan_record.status, "message": "Scan in progress or queued."}

@app.get("/scans", response_model=List[Dict[str, Any]])
async def get_all_scans(db: Session = Depends(get_db)):
    """
    Retrieves a list of all scan records from the database, ordered by creation date.
    """
    scans = db.query(Scan).order_by(Scan.created_at.desc()).all()
    return [scan.to_dict() for scan in scans]

@app.delete("/scan/{scan_id}")
async def delete_scan(scan_id: str, db: Session = Depends(get_db)):
    """
    Deletes a scan record from the database.
    """
    scan_record = db.query(Scan).filter(Scan.scan_id == scan_id).first()
    
    if not scan_record:
        raise HTTPException(status_code=404, detail="Scan ID not found.")
    
    db.delete(scan_record)
    db.commit()
    
    return {"message": f"Scan with ID '{scan_id}' deleted successfully."}
