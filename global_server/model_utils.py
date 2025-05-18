import os
import torch
import torch.nn as nn
import joblib
import json
from logging_config import get_logger
from typing import Dict, Any


logger = get_logger()

class DiabetesBinaryNet(nn.Module):
    def __init__(self, input_size: int):
        super().__init__()
        self.bn1 = nn.BatchNorm1d(input_size)
        self.fc1 = nn.Linear(input_size, 256)
        self.bn2 = nn.BatchNorm1d(256)
        self.fc2 = nn.Linear(256, 128)
        self.bn3 = nn.BatchNorm1d(128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 2)
        self.dropout = nn.Dropout(0.4)
        
    def forward(self, x):
        x = self.bn1(x)
        x = torch.relu(self.fc1(x))
        x = self.bn2(x)
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.bn3(x)
        x = self.dropout(x)
        x = torch.relu(self.fc3(x))
        return self.fc4(x)

def load_model_resources(settings) -> Dict[str, Any]:
    """Load all model resources."""
    with open(settings.FEATURES_PATH) as f:
        features = json.load(f)
    
    model = DiabetesBinaryNet(len(features)).to(settings.DEVICE)
    if os.path.exists(settings.MODEL_PATH):
        logger.info("LOADING GLOBAL MODEL FROM STORAGE")
        model.load_state_dict(torch.load(settings.MODEL_PATH, map_location=settings.DEVICE))
        model.eval()

    else:
        logger.info("MODEL NOT FOUND, CREATING NEW MODEL")
    
    scaler = joblib.load(settings.SCALER_PATH)
    
    return {
        "model": model,
        "scaler": scaler,
        "features": features
    }