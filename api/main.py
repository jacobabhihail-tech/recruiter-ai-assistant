from io import BytesIO

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    MatchRequest,
    ChatRequest,
    UploadResponse
)

from src.resume_parser import extract_text_from_pdf
from src.llm import extract_candidate_profile
from src.matching_engine import find_matching_jobs
from src.rag_engine import generate_rag_response

from src.candidate_schema import CandidateProfile
from src.intake_schema import CandidatePreferences
from src.job_schema import Job


# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI(
    title="AI Recruitment Assistant API",
    description="Backend API for the AI Recruitment Assistant",
    version="1.0.0"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():

    return {
        "message": "AI Recruitment Assistant API",
        "status": "running"
    }


# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ==================================================
# 1. RESUME UPLOAD
# ==================================================

@app.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_resume(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )


    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported"
        )


    try:

        # --------------------------------------------------
        # READ UPLOADED FILE
        # --------------------------------------------------

        file_bytes = await file.read()


        # --------------------------------------------------
        # CREATE NORMAL FILE-LIKE OBJECT
        # --------------------------------------------------

        pdf_file = BytesIO(
            file_bytes
        )


        # --------------------------------------------------
        # EXTRACT RESUME TEXT
        # --------------------------------------------------

        resume_text = extract_text_from_pdf(
            pdf_file
        )


        # --------------------------------------------------
        # EXTRACT CANDIDATE PROFILE
        # --------------------------------------------------

        candidate_profile = (
            extract_candidate_profile(
                resume_text
            )
        )


        # --------------------------------------------------
        # RETURN RESPONSE
        # --------------------------------------------------

        return UploadResponse(

            filename=file.filename,

            resume_text=resume_text,

            candidate_profile=(
                candidate_profile.model_dump()
            )
        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==================================================
# 2. JOB MATCHING
# ==================================================

@app.post("/match")
def match_jobs(
    request: MatchRequest
):

    try:

        # --------------------------------------------------
        # CONVERT CANDIDATE PROFILE
        # --------------------------------------------------

        candidate_profile = (
            CandidateProfile.model_validate(
                request.candidate_profile
            )
        )


        # --------------------------------------------------
        # CONVERT CANDIDATE PREFERENCES
        # --------------------------------------------------

        candidate_preferences = (
            CandidatePreferences.model_validate(
                request.candidate_preferences
            )
        )


        # --------------------------------------------------
        # FIND MATCHING JOBS
        # --------------------------------------------------

        matched_jobs = find_matching_jobs(

            candidate_profile,

            candidate_preferences,

            "data/jobs.json",

            top_k=request.top_k
        )


        # --------------------------------------------------
        # PREPARE JSON RESPONSE
        # --------------------------------------------------

        results = []


        for match in matched_jobs:

            job = match["job"]


            results.append({

                "job": job.model_dump(),

                "distance": match["distance"]

            })


        return {

            "count": len(results),

            "matches": results

        }


    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# ==================================================
# 3. RECRUITER CHAT
# ==================================================

@app.post("/chat")
async def recruiter_chat(
    request: ChatRequest
):

    try:

        # --------------------------------------------------
        # CONVERT CANDIDATE PROFILE
        # --------------------------------------------------

        candidate_profile = (
            CandidateProfile.model_validate(
                request.candidate_profile
            )
        )


        # --------------------------------------------------
        # CONVERT CANDIDATE PREFERENCES
        # --------------------------------------------------

        candidate_preferences = (
            CandidatePreferences.model_validate(
                request.candidate_preferences
            )
        )


        # --------------------------------------------------
        # CONVERT MATCHED JOBS
        # --------------------------------------------------

        matched_jobs = []


        for match in request.matched_jobs:

            job_data = match["job"]


            job = Job(
                id=job_data["id"],
                title=job_data["title"],
                skills=job_data["skills"],
                location=job_data["location"],
                experience=job_data["experience"]
            )


            matched_jobs.append(
                {
                    "job": job,
                    "distance": match["distance"]
                }
            )


        # --------------------------------------------------
        # GENERATE RAG RESPONSE
        # --------------------------------------------------

        response = generate_rag_response(

            candidate_profile,

            candidate_preferences,

            matched_jobs,

            request.query

        )


        # --------------------------------------------------
        # RETURN RESPONSE
        # --------------------------------------------------

        return {

            "query": request.query,

            "response": response

        }


    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )