import os
import time
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from groq import Groq

# Import core architectural primitives directly from agent.py
from agent import HindsightMemoryEngine, CascadeFlowGateway

# 1. API Routing Configuration Setup
app = FastAPI(
    title="Enterprise Deal Intelligence Engine",
    description="Production-grade CRM memory and routing runtime API.",
    version="1.0.0"
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("CRITICAL: Environment variable GROQ_API_KEY is unconfigured.")

client = Groq(api_key=GROQ_API_KEY)

# 2. Enterprise Security Token Infrastructure
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def validate_auth_token(api_key: str = Security(api_key_header)):
    if api_key != "secret_sales_token_2026":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Unauthorized: Invalid Enterprise Security Token."
        )
    return api_key

# 3. Data Presentation Layer Models (Schemas)
class AnalysisRequest(BaseModel):
    prospect_name: str
    incoming_interaction: str

class AnalysisResponse(BaseModel):
    prospect_name: str
    intent_detected: str
    model_allocated: str
    latency_seconds: float
    generated_output: str

# 4. Global Middleware Initializations
memory_engine = HindsightMemoryEngine()
routing_gateway = CascadeFlowGateway()

# 5. Production Transaction Router Endpoint
@app.post("/api/v1/deal-intelligence", response_model=AnalysisResponse, status_code=200)
async def process_deal_transaction(
    payload: AnalysisRequest, 
    auth: str = Depends(validate_auth_token)
):
    start_time = time.time()
    
    # Step A: Asynchronous isolated context tracking execution (Hindsight)
    historical_memory = await memory_engine.recall_isolated_context(payload.prospect_name)
    
    # Step B: Automated semantic evaluation execution (cascadeflow)
    computed_intent = await routing_gateway.analyze_intent_complexity(payload.incoming_interaction)
    target_model = routing_gateway.select_hardware_route(computed_intent)
    
    # Step C: Composing production isolation execution boundaries
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
        # Step D: Execute Network Inference Loop over cloud framework clusters
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
        
        print(f"📊 [Telemetry System Audit] Complete. Target: {target_model} | Runtime: {latency:.2f}s")
        
        return AnalysisResponse(
            prospect_name=payload.prospect_name,
            intent_detected=computed_intent,
            model_allocated=target_model,
            latency_seconds=round(latency, 3),
            generated_output=generated_text
        )
        
    except Exception as network_error:
        print(f"❌ [API Failover System] Error detected over target array: {str(network_error)}")
        
        # Step E: Immediate automatic failover fallback path execution
        backup_model = "llama-3.1-8b-instant"
        print(f"🔄 [cascadeflow Intercept] Redirecting current thread payload to safe-mode core: {backup_model}")
        
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": combined_user_payload}],
            model=backup_model,
            stream=False
        )

        fallback_text = completion.choices[0].message.content or ""
        
        return AnalysisResponse(
            prospect_name=payload.prospect_name,
            intent_detected="emergency_failover",
            model_allocated=backup_model,
            latency_seconds=round(time.time() - start_time, 3),
            generated_output=fallback_text
        )