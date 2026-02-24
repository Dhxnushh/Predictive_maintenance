# Predictive Maintenance System - Deployment Guide

## 🚀 Quick Deploy

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

1. **Fork this repository**
2. **Create a new Web Service** on Render
3. **Connect your repository**
4. Render will automatically detect `render.yaml` and deploy

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
heroku open
```

### Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select this repository
4. Railway will auto-deploy

---

## 📦 **What's Included**

- ✅ **Trained ML Model**: XGBoost classifier (97.5% accuracy)
- ✅ **FastAPI Backend**: RESTful API with auto-docs
- ✅ **Real-time Dashboard**: Minimal black & white UI
- ✅ **Data Simulator**: Generates realistic sensor data
- ✅ **Production Ready**: Environment variable support

---

## 🔧 Local Development

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python app.py
```

The application will be available at `http://localhost:8000`

### 3. Access Dashboard

Open: `http://localhost:8000/dashboard`

### 4. API Documentation

Open: `http://localhost:8000/docs`

---

## 🌍 Environment Variables

Configure these on your deployment platform:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Server port |
| `HOST` | `0.0.0.0` | Server host |
| `ENV` | `development` | Environment (`development` or `production`) |

---

## 📊 **System Features**

### Live Monitoring
- **5 Machines** monitored in real-time
- **Auto-updating** every 2 seconds
- **Health Status**: Healthy, At Risk, Maintenance Required
- **Failure Prediction**: AI-powered probability scores

### Machine Learning
- **Model**: XGBoost Classifier
- **Accuracy**: 97.50%
- **F1-Score**: 0.6875
- **ROC-AUC**: 0.9755

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/dashboard` | GET | Live monitoring dashboard |
| `/health` | GET | Health check |
| `/simulate-and-predict` | GET | Get predictions for all machines |
| `/predict` | POST | Predict for specific sensor data |
| `/model/info` | GET | Model information |
| `/docs` | GET | Interactive API documentation |

---

## 🎨 **Dashboard Preview**

Minimal black & white theme with:
- Real-time machine status cards
- Failure probability visualization
- Sensor data monitoring
- Model performance metrics
- Alert system for high-risk machines

---

## 📁 **Project Structure**

```
Predictive_maintenance/
├── app.py                          # FastAPI application
├── config.py                       # Configuration
├── train_model.py                  # Model training script
├── model_inference.py              # Inference engine
├── data_simulator.py               # Real-time data simulator
├── monitoring_service.py           # Monitoring service
├── requirements.txt                # Python dependencies
├── Procfile                        # Deployment config
├── render.yaml                     # Render deployment
├── runtime.txt                     # Python version
├── models/                         # Trained models
│   ├── xgboost.pkl
│   ├── label_encoder.pkl
│   └── model_metadata.json
├── static/                         # Frontend
│   └── dashboard.html
└── predicrtiver_maintenance_dataset/
    └── ai4i2020.csv               # Training dataset
```

---

## 🛠️ **Technology Stack**

- **Backend**: FastAPI, Python 3.11
- **ML**: XGBoost, Scikit-learn, Pandas, NumPy
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Deployment**: Uvicorn ASGI server

---

## 📝 **License**

MIT License - Feel free to use in your projects!

---

## 🤝 **Support**

For issues or questions, please create an issue in the repository.

---

**Built with ❤️ for Industrial IoT**
