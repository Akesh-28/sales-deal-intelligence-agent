import os
import json
import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SalesEngine")

# Configuration Constants
STRATEGIC_KEYWORDS = {
    "proposal", "pricing", "competitor", "contract", 
    "negotiate", "pitch", "legal", "compliance"
}


class HindsightMemoryEngine:
    """Manages isolated episodic cross-session memory banks."""

    def __init__(self, storage_path: str = "data/sales_interactions.json"):
        self.storage_path = Path(storage_path)

    async def _read_records_async(self) -> List[Dict[str, Any]]:
        """Helper to read JSON file in a thread pool to avoid blocking the event loop."""
        if not self.storage_path.exists():
            return []
            
        def _read_file():
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
                
        # Runs blocking I/O in a separate thread
        return await asyncio.to_thread(_read_file)

    async def recall_isolated_context(self, prospect_name: str) -> str:
        """Asynchronously reads data to simulate zero-blocking DB I/O loops."""
        logger.info(f"Querying isolated context for prospect: '{prospect_name}'")
        fallback_msg = "No prior conversational history tracked for this entity identity scope."
        
        try:
            # Emulating database read latency
            await asyncio.sleep(0.05) 
            
            records = await self._read_records_async()
            if not records:
                return fallback_msg
            
            extracted_facts = [
                f"- [{r['date']}]: {r['transcript']}" 
                for r in records 
                if r.get("prospect", "").lower() == prospect_name.lower()
            ]
            
            if extracted_facts:
                return "\n[HINDSIGHT CONTEXT ACTIVE]\n" + "\n".join(extracted_facts)
                
        except Exception as e:
            logger.error(f"Memory isolation read fallback triggered: {str(e)}")
            
        return fallback_msg


class CascadeFlowGateway:
    """Evaluates intent complexity and manages dynamic cloud infrastructure routing."""

    def __init__(self):
        self.cost_ceiling_usd = 10.00
        self.current_session_cost = 0.00

    async def analyze_intent_complexity(self, text: str) -> str:
        """Automatically checks text patterns to discover structural complexity metrics."""
        # Yield control briefly to simulate processing if needed in an async chain
        await asyncio.sleep(0) 
        
        input_words = set(text.lower().split())
        
        # Intersection check is faster and cleaner than list comprehensions
        if input_words.intersection(STRATEGIC_KEYWORDS):
            return "strategic_objection"
        return "administrative_summary"

    def select_hardware_route(self, intent_tier: str) -> str:
        """Maps computed transaction profiles to targeted LPU hardware segments."""
        if intent_tier == "strategic_objection":
            logger.info("High-stakes negotiation intent detected. Routing to 70B array.")
            return "llama-3.3-70b-versatile"
        
        logger.info("Basic utility intent detected. Routing to 8B baseline engine.")
        return "llama-3.1-8b-instant"


# Script test sandbox block
async def main():
    logger.info("Running local core intelligence engine sandbox test...")
    
    if not os.environ.get("GROQ_API_KEY"):
        logger.critical("GROQ_API_KEY environment variable is not configured.")
        sys.exit(1)
        
    engine = HindsightMemoryEngine()
    gateway = CascadeFlowGateway()
    
    # Execute pipelines
    intent = await gateway.analyze_intent_complexity("Let's talk about pricing structure.")
    model = gateway.select_hardware_route(intent)
    
    logger.info(f"Sandbox Verification Successful. Route computed: {model}")


if __name__ == "__main__":
    asyncio.run(main())