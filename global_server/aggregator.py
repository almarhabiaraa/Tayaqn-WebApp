from typing import List, Dict
import torch
import torch.nn as nn
from model_utils import DiabetesBinaryNet
import numpy as np
from typing import List, Dict, Any

from logging_config import get_logger

logger = get_logger()

class FederatedAggregator:
    def __init__(self, model: nn.Module):
        self.global_model = model

    def _convert_to_tensor(self, value: Any) -> torch.Tensor:
        """Helper method to convert various types to tensor."""
        if isinstance(value, torch.Tensor):
            return value
        elif isinstance(value, (list, np.ndarray)):
            return torch.tensor(value, dtype=torch.float32)
        elif isinstance(value, (int, float)):
            return torch.tensor([float(value)], dtype=torch.float32)
        else:
            raise ValueError(f"Unsupported type for conversion: {type(value)}")

    def aggregate_weights(self, client_weights_list: List[Dict[str, Any]]) -> None:
        """Aggregate weights from multiple clients using FedAvg algorithm."""
        if not client_weights_list:
            return
            
        logger.info("AGGREGATING WEIGHTS")
        new_state = self.global_model.state_dict()
        
        for key in new_state.keys():
            try:
                client_tensors = []
                for weights in client_weights_list:
                    tensor_value = self._convert_to_tensor(weights[key])
                    client_tensors.append(tensor_value.float())
                
                # Stack tensors and compute mean
                stacked_tensors = torch.stack(client_tensors, dim=0)
                new_state[key] = torch.mean(stacked_tensors, dim=0)
                
            except Exception as e:
                logger.error(f"Error processing key {key}: {str(e)}")
                raise
        
        logger.info("WEIGHTS AGGREGATED SUCCESSFULLY")
        self.global_model.load_state_dict(new_state)
    
    def get_global_weights(self) -> Dict[str, torch.Tensor]:
        """Get current global model weights."""
        return self.global_model.state_dict()