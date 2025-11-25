from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

from .query_generator import QueryGenerator
from .mitre_attack import MitreAttackIntegration
from .validators import QueryValidator

app = FastAPI(
    title="Threat Hunting Query Generator",
    description="AI-powered system that converts natural language to threat-hunting queries",
    version="1.0.0"
)

# Initialize components
query_generator = QueryGenerator()
mitre_attack = MitreAttackIntegration()
query_validator = QueryValidator()

class QueryRequest(BaseModel):
    """Request model for query generation"""
    description: str
    query_type: str  # spl, kql, dsl
    include_mitre: Optional[bool] = False

class QueryResponse(BaseModel):
    """Response model for generated queries"""
    query: str
    explanation: str
    mitre_technique: Optional[str] = None
    validation_result: Optional[dict] = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Threat Hunting Query Generator API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/generate-query", response_model=QueryResponse)
async def generate_query(request: QueryRequest):
    """Generate threat hunting query from natural language description"""
    try:
        # Generate query using LLM
        query_result = query_generator.generate(request.description, request.query_type)
        
        # Get MITRE ATT&CK mapping if requested
        mitre_technique = None
        if request.include_mitre:
            mitre_technique = mitre_attack.map_to_technique(request.description)
        
        # Validate query
        validation_result = query_validator.validate(query_result["query"], request.query_type)
        
        return QueryResponse(
            query=query_result["query"],
            explanation=query_result["explanation"],
            mitre_technique=mitre_technique,
            validation_result=validation_result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating query: {str(e)}")

@app.get("/mitre-techniques")
async def get_mitre_techniques():
    """Get all MITRE ATT&CK techniques"""
    try:
        techniques = mitre_attack.get_all_techniques()
        return {"techniques": techniques}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching MITRE techniques: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)