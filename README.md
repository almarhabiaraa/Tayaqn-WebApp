# 🩺 Tayaqn: Smart & Secure Diabetes Prediction System 

**Senior Project:** AI-Driven Diabetes Prediction Using Federated Learning Architecture  

**Tools:** Python · Angular · PyTorch · FastAPI · SQLite · Node.js  



## Project Overview

**Tayaqn** is a privacy-focused, AI-powered diabetes prediction system that uses **Federated Learning (FL)** to train models across distributed clients without transferring raw medical data. This approach ensures data privacy while achieving high predictive accuracy.

The project combines advanced deep learning with secure software architecture, providing a complete end-to-end solution with both frontend and backend components.



## Features

- **Federated Learning** – Enables distributed training while preserving user data privacy  
- **Deep Learning with PyTorch** – Builds robust models for diabetes prediction  
- **Responsive Web Interface** – Built with Angular for a smooth user experience  
- **FastAPI Servers** – Handles local training and global model aggregation  
- **Secure Architecture** – Keeps sensitive health data on local devices  



## Project Structure

```bash
Tayaqn/
├── Dataset/
│   └── diabetes_health_indicators.csv         # Source dataset
│
├── AI_Model/
│   └── diabetes.ipynb                         # Jupyter notebook for training & evaluation
│
├── frontend/
│   ├── src/
│   └── angular_app_files...                   # Angular-based UI
│
├── local_server/
│   ├── main.py                                # FastAPI local server
│   └── utils.py                               # Data preprocessing & training logic
│
├── global_server/
│   ├── main.py                                # FastAPI aggregator server
│   └── aggregator.py                          # Model aggregation logic
│
├── Database/                                  # SQLite database files
│
├── Tayaqn_Demo.mov                            # Demo video
└── README.md

```
## Model Performance
| Model Type         | Accuracy |
|--------------------|----------|
| Centralized Model  | 0.8600   |
| Federated Learning | 0.8519   |

> ✅ The federated learning model achieves nearly the same performance as the centralized model, demonstrating effective privacy-preserving training.

## Web Application Overview

**Tayaqn** offers a responsive, user-friendly interface built for both **patients** and **healthcare professionals** to assess diabetes risk in real time while maintaining user data privacy.


### Core Pages & Workflow

- **Registration Page**  
  New users can sign up by providing a username, email, and password.

- **Login Page**  
  Registered users log in securely using their credentials.

- **Dashboard (History Page)**  
  Displays past assessment results. If no tests have been taken, an informative message is shown.

- **Take Test Page**  
  Users begin the diabetes risk assessment by clicking the **Start Now** button.



### Diabetes Risk Assessment Workflow

Each test consists of several structured steps to collect and evaluate relevant health data:

1. **Basic Information**  
   - Gender  
   - Age  
   - Body Mass Index (BMI)

2. **Health Indicators**  
   - Blood Pressure  
   - Cholesterol Levels

3. **Lifestyle Factors**  
   - Smoking  
   - Alcohol Consumption  
   - Diet (e.g., fruit/vegetable intake)

4. **Medical History**  
   - Stroke  
   - Heart Disease  
   - Physical Limitations (e.g., difficulty walking)

5. **🏃‍♂️ Health Status**  
   - Physical Activity  
   - Mental Health  
   - General Health (past 30 days)



### Prediction Results

- Results are displayed in the **Dashboard**:
  - ✅ **Negative** — Low risk of diabetes.
  - ⚠️ **Positive** — High risk, with a prompt suggesting medical advice.



### Contact Us Page

Users can reach out with questions or feedback by submitting:
- Subject  
- Message  

Responses help improve the system and user experience.

 ## Future Work
1. 📱 Mobile App Development – Build a mobile version for broader accessibility
2. 🌍 Arabic Language Support – Support multilingual users with Arabic interface
3. 🤖 Explainable AI (XAI) – Make predictions interpretable for medical users


 ## Demo
[▶️ Watch Tayaqn Demo](https://youtu.be/HanVSwcSN4w)

## Developed By
**Tayaqn Team – 2025**

