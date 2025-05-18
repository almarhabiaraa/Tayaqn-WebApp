from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from typing import List, Dict, Any

from config import get_settings
from model_utils import load_model_resources
from aggregator import FederatedAggregator
from colorlog import ColoredFormatter
from logging_config import get_logger



app = FastAPI(title="Diabetes Detection Global Server")
api_key_header = APIKeyHeader(name="X-API-Key")
logger = get_logger()
async def get_api_key(
    api_key_header: str = Security(api_key_header),
    settings = Depends(get_settings)
):
    if api_key_header != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key_header

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClientWeights(BaseModel):
    weights: Dict[str, Any]

# Load resources
settings = get_settings()
resources = load_model_resources(settings)
aggregator = FederatedAggregator(resources["model"])


@app.get("/model/global", dependencies=[Depends(get_api_key)])
async def get_global_model():
    """Get current global model weights."""
    global_weights = aggregator.get_global_weights()
    
    # Serialize tensors to lists
    serialized_weights = {
        k: v.tolist() if isinstance(v, torch.Tensor) else v
        for k, v in global_weights.items()
    }
    
    return {
        "weights": serialized_weights,
        "features": resources["features"]
    }

@app.post("/model/update", dependencies=[Depends(get_api_key)])
async def update_global_model(client_weights: List[ClientWeights]):
    """Update global model with client weights."""
    if not client_weights:    
        raise HTTPException(status_code=400, detail="No client weights provided")
    
    logger.info(f"WEIGHTS RECEIVED:")
    try:
        # Convert all client weights to state dictionaries
        state_dicts = []
        for cw in client_weights:
            state_dict = {}
            for key, value in cw.weights.items():
                try:
                    state_dict[key] = value
                except Exception as e:
                    logger.error(f"Error processing weight {key}: {str(e)}")
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Invalid weight format for key {key}: {str(e)}"
                    )
            state_dicts.append(state_dict)
        
        # Aggregate the weights
        aggregator.aggregate_weights(state_dicts)

        # Save the updated model
        torch.save(aggregator.global_model.state_dict(), settings.MODEL_PATH)
        global_weights = aggregator.get_global_weights()

        # Serialize tensors to lists
        serialized_weights = {
            k: v.tolist() if isinstance(v, torch.Tensor) else v
            for k, v in global_weights.items()
        }

        return {
            "message": "Global model updated successfully",
            "weights": serialized_weights
        }
    
    except Exception as e:
        logger.error(f"Error updating model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)