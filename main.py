"""
FastAPI backend for Phishing Email Classifier.
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import EmailInput, AnalysisResponse, ThreatReport
from agent import agent
from samples import SAMPLES


# Create FastAPI app
app = FastAPI(
    title="Phishing Email Classifier API",
    description="AI-powered phishing detection using Pydantic AI + Groq",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Phishing Email Classifier API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze (POST)",
            "examples": "/examples"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model": "groq:llama-3.3-70b-versatile",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_email(email_input: EmailInput):
    """
    Analyze an email for phishing threats.
    
    Args:
        email_input: EmailInput containing raw_email, optional sender and subject
        
    Returns:
        AnalysisResponse with ThreatReport and metadata
    """
    try:
        # Run the Pydantic AI agent
        result = await agent.run(email_input.raw_email)
        report: ThreatReport = result.output
        
        return AnalysisResponse(
            report=report,
            analyzed_at=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/examples")
def get_examples():
    """Get 5 pre-loaded sample phishing emails for demo."""
    return {
        "samples": SAMPLES,
        "count": len(SAMPLES)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
