# Tayaqn: An AI-Driven Diabetes Prediction System Using Federated Learning Architecture

## Project Overview
**Tayaqn** is a privacy-preserving diabetes prediction system developed as part of a senior project. Leveraging **Federated Learning (FL)**, it enables AI model training across distributed client devices without sharing raw medical data. This ensures user privacy while maintaining high model performance.

The system integrates advanced AI techniques with secure and scalable software architecture, including both frontend and backend components, to deliver an end-to-end predictive solution.



## Features
- **Federated Learning-based AI Model** for secure, decentralized training  
- **Deep Learning with PyTorch** for high-performance prediction  
- **Interactive Web Frontend** for user-friendly data input and prediction results  
- **FastAPI-powered Local & Global Servers** for scalable deployment  
- **Data Privacy** maintained by keeping user data on local devices



## Project Structure

```bash

Tayaqn/
├── Dataset/
│   └── diabetes_health_indicators.csv         # Source dataset
│
├── AI_Model/
│   └── diabetes.ipynb                         # Jupyter notebook for model training and evaluation
│
├── frontend/
│   ├── src/
│   └── angular_app_files...                   # Angular-based UI for input and prediction
│
├── local_server/
│   ├── main.py                                # FastAPI server for local training
│   └── utils.py                               # Data preprocessing, training logic
│
├── global_server/
│   ├── aggregator.py                          # Model aggregation logic
│   └── main.py                                # FastAPI server for coordinating federated learning
│
└── README.md

```


## Performance

The federated learning approach achieves comparable accuracy (0.8519) to the central model (0.86), demonstrating that privacy preservation comes with minimal performance loss.




## Future Work
1. **Mobile Accessibility**: Expand the system to a mobile app, making it more accessible to users on the go.
2. **Arabic Language Support**: Support Arabic language to reach a broader and more diverse user base.
3. **Explainable AI**: Incorporate Explainable AI techniques to provide transparent and understandable predictions.



> Developed by the Tayaqn Team | 2025

