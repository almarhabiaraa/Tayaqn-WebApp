Tayaqn: AI-Driven Diabetes Prediction System Using Federated Learning
Project Overview
Tayaqn is an AI-powered diabetes prediction system designed using federated learning architecture. It aims to preserve user data privacy by training models locally on multiple clients and aggregating them globally without sharing raw data.

Project Structure
frontend/
Angular-based web application for user interaction and data visualization.

local_server/
Backend server handling local model training and data processing using FastAPI.

global_server/
Central server responsible for federated model aggregation and coordination.

diabetes.ipynb
Jupyter notebook for AI model development, experimentation, and evaluation.

Features
Privacy-preserving diabetes prediction using federated learning.

Interactive web frontend for data input and prediction results.

Scalable backend with local and global servers.

AI model development using PyTorch.

Getting Started
Prerequisites
Python 3.8+

Node.js and npm

Angular CLI

Git

Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/almarhabiaraa/Tayaqn-app.git
cd Tayaqn-app
Install backend dependencies:

bash
Copy
Edit
cd local_server
pip install -r requirements.txt
Install frontend dependencies:

bash
Copy
Edit
cd ../frontend
npm install
Running the Application Locally
Backend (Local Server)
cd ~/Desktop/Tayaqn-app/local_server
python3 main.py


Backend (Global Server)
cd ~/Desktop/Tayaqn-app/global_server
python3 main.py

Frontend (Angular UI)
cd ~/Desktop/Tayaqn-app/frontend
ng serve


Deployment
Backend services can be deployed on platforms like Render or Heroku.

Frontend can be deployed using Vercel, Netlify, or similar platforms.

License
MIT License

Contact
For questions or support, contact: [Your Email or GitHub Profile]
