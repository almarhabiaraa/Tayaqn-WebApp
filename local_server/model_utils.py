import torch
import torch.nn as nn
import numpy as np
from typing import Dict, Any
from config import settings

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

class LocalModelManager:
    def __init__(self, model: nn.Module, scaler: Any):
        self.model = model
        self.scaler = scaler
    
    def predict(self, features: np.ndarray) -> int:
        """Make prediction for single sample."""
        self.model.eval()
        with torch.no_grad():
            features_scaled = self.scaler.transform(features.reshape(1, -1))
            features_tensor = torch.tensor(features_scaled, dtype=torch.float32, device=self.device)
            outputs = self.model(features_tensor)
            prediction = outputs.argmax(dim=1).item()
        return prediction
    
    def train_local(self, features: np.ndarray, labels: np.ndarray, epochs: int = 5) -> Dict:
        """Train model on local data."""
        self.model.train()
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Convert to tensors
        X = torch.tensor(features_scaled, dtype=torch.float32, device=self.device)
        y = torch.tensor(labels, dtype=torch.long, device=self.device)
        
        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        losses = []
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self.model(X)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
        
        return {
            "final_loss": losses[-1],
            "avg_loss": sum(losses) / len(losses),
            "epochs": epochs
        }