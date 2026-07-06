import os
import time
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from groq import Groq

# Core architectural primitives imported from local agent module
from agent import HindsightMemoryEngine, CascadeFlowGateway

# =====================================================================
# 1. API CONFIGURATION & CORE INITIALIZATION
# =====================================================================
app = FastAPI(
    title="Enterprise Deal Intelligence Engine",
    description="Production-grade CRM memory and routing runtime API.",
    version="1.0.0"
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("CRITICAL: Environment variable GROQ_API_KEY is unconfigured.")

# Initialize the Groq SDK client
client = Groq(api_key=GROQ_API_KEY)

# Instantiate long-lived engines as global instances
memory_engine = HindsightMemoryEngine()
routing_gateway = CascadeFlowGateway()


# =====================================================================
# 2. SECURITY & AUTHENTICATION MIDDLEWARE
# =====================================================================
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def validate_auth_token(api_key: str = Security(api_key_header)) -> str:
    """
    Validates incoming API requests against a static enterprise token.
    
    Args:
        api_key (str): Extracted token from the request header.
        
    Raises:
        HTTPException: 403 Forbidden error if token is missing or invalid.
    """
    # Note: In production, swap this for an env variable or dynamic vault lookup
    if api_key != "secret_sales_token_2026":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Unauthorized: Invalid Enterprise Security Token."
        )
    return api_key


# =====================================================================
# 3. DATA PERSISTENCE LAYER (SCHEMAS)
# =====================================================================
class AnalysisRequest(BaseModel):
    """Payload schema for client inbound interaction analyses."""
    prospect_name: str
    incoming_interaction: str

    class Config:
        json_schema_extra = {
            "example": {
                "prospect_name": "Acme Corp",
                "incoming_interaction": "Can we review the pricing model for the enterprise subscription?"
            }
        }


class AnalysisResponse(BaseModel):
    """Standardized response schema returned to the client gateway."""
    prospect_name: str
    intent_detected: str
    model_allocated: str
    latency_seconds: float
    generated_output: str


# =====================================================================
# 4. TRANSACTION ENGINE ROUTER (ENDPOINTS)
# =====================================================================
@app.post(
    "/api/v1/deal-intelligence", 
    response_model=AnalysisResponse, 
    status_code=status.HTTP_200_OK,
    summary="Process customer intent with context-aware routing."
)
async def process_deal_transaction(
    payload: AnalysisRequest, 
    auth: str = Depends(validate_auth_token)
):
    """
    Processes client interactions by pulling conversation history,
    dynamically routing the request to an optimal LLM hardware path,
    and handling automated model failovers if network faults occur.
    """
    start_time = time.time()
    
    # Step A: Asynchronously fetch historical timeline context
    historical_memory = await memory_engine.recall_isolated_context(payload.prospect_name)
    
    # Step B: Compute intent tier and dynamically select LLM target route
    computed_intent = await routing_gateway.analyze_intent_complexity(payload.incoming_interaction)
    target_model = routing_gateway.select_hardware_route(computed_intent)
    
    # Step C: Compose instructions and isolate background data
    system_instructions = (
        "You are an Elite Enterprise Sales Agent Core Operations Unit.\n"
        "Analyze the historical context and draft an immediate response matrix address.\n"
        "Enforce strict validation constraints: Always explicitly mention historical timeline dates."
    )
    
    combined_user_payload = (
        f"Historical Scope Background Data:\n{historical_memory}\n\n"
        f"New Live Input Data:\n{payload.incoming_interaction}\n\n"
        f"Action Requirement: Compile a professional executive sales output."
    )
    
    try:
        # Step D: Primary API Call Loop Execution
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": combined_user_payload}
            ],
            model=target_model,
            temperature=0.2,
            stream=False
        )
        
        latency = time.time() - start_time
        generated_text = completion.choices[0].message.content or ""
        
        print(f"📊 [Telemetry Audit] Success | Route: {target_model} | Latency: {latency:.2f}s")
        
        return AnalysisResponse(
            prospect_name=payload.prospect_name,
            intent_detected=computed_intent,
            model_allocated=target_model,
            latency_seconds=round(latency, 3),
            generated_output=generated_text
        )
        
    except Exception as network_error:
        # Step E: Secondary Failover Intercept Routing Path
        print(f"❌ [API Failover System] Error over target cluster: {str(network_error)}")
        backup_model = "llama-3.1-8b-instant"
        print(f"🔄 [CascadeFlow Intercept] Redirecting current payload to backup array: {backup_model}")
        
        try:
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": combined_user_payload}],
                model=backup_model,
                stream=False
            )
            fallback_text = completion.choices[0].message.content or ""
        except Exception as critical_err:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Critical system blackout. LLM clusters unreachable: {str(critical_err)}"
            )

        return AnalysisResponse(
            prospect_name=payload.prospect_name,
            intent_detected="emergency_failover",
            model_allocated=backup_model,
            latency_seconds=round(time.time() - start_time, 3),
            generated_output=fallback_text
        )