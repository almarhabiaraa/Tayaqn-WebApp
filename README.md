# Tayaqn: An AI-Driven Diabetes Prediction System Using Federated Learning Architecture

## 🚀 Project Overview
**Tayaqn** is a privacy-preserving diabetes prediction system developed as part of a senior project. Leveraging **Federated Learning (FL)**, it enables AI model training across distributed client devices without sharing raw medical data. This ensures user privacy while maintaining high model performance.

The system integrates advanced AI techniques with secure and scalable software architecture, including both frontend and backend components, to deliver an end-to-end predictive solution.

---

## 🔑 Features
- ✅ **Federated Learning-based AI Model** for secure, decentralized training  
- 🧠 **Deep Learning with PyTorch** for high-performance prediction  
- 🌐 **Interactive Web Frontend** for user-friendly data input and prediction results  
- 🖥️ **FastAPI-powered Local & Global Servers** for scalable deployment  
- 🔐 **Data Privacy** maintained by keeping user data on local devices

---

## 📁 Repository Structure

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
---

## 📊 Model Performance
The model was evaluated using the **Diabetes Health Indicators** dataset on metrics including:

- **Accuracy**
- **Precision**
- **Recall**
- **F1-Score**

Federated learning results were comparable to centralized training, proving effective in preserving data privacy without sacrificing performance.

> *Detailed performance charts or evaluation tables can be added here.*

---

## 🔭 Future Work
- 🔄 Implement **differential privacy** for stronger data protection  
- 📱 Build **mobile clients** for real-time, on-the-go data collection  
- 📈 Support for **larger and diverse datasets** to enhance model generalization  
- 🧩 Integration with **Electronic Health Record (EHR)** systems  
- 🧠 Include **explainability techniques** like SHAP or LIME for model transparency

---

## 📄 License
This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for more information.

---

## 🙏 Acknowledgments
- Project supervisors and faculty at [Your University Name]
- The authors of the **Diabetes Health Indicators** dataset
- Open-source contributors to **PyTorch**, **FastAPI**, **Angular**, and **Federated Learning frameworks**

---

> Developed by the Tayaqn Team | 2025

