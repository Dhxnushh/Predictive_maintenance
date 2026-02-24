# AI-Driven Predictive Maintenance System

A complete end-to-end predictive maintenance solution using machine learning to monitor industrial equipment and predict failures before they occur.

## 🚀 Features

- **Machine Learning Pipeline**: Automated training with Random Forest and XGBoost models
- **Automatic Model Selection**: Chooses best model based on F1-score and ROC-AUC
- **RESTful API**: FastAPI-based backend with prediction endpoints
- **Real-time Dashboard**: Live monitoring of multiple machines
- **Data Simulation**: Realistic sensor data generation for continuous monitoring
- **Health Status Indicators**: Clear visual indicators (Healthy, Risk, Maintenance Required)
- **Alert System**: Automatic alerts when failure probability exceeds threshold
- **Production-Ready**: Modular architecture with separate components

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for Python packages

## 🔧 Installation

1. **Clone the repository or navigate to the project directory:**
   ```bash
   cd e:\Projects\Predictive_maintenance
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Dataset

The system uses the **AI4I 2020 Predictive Maintenance Dataset** which should be located at:
```
predicrtiver_maintenance_dataset/ai4i2020.csv
```

### Dataset Features:
- Air temperature [K]
- Process temperature [K]
- Rotational speed [rpm]
- Torque [Nm]
- Tool wear [min]
- Machine type (L, M, H)
- Machine failure (target variable)

## 🎯 Usage

### Step 1: Train the Model

First, train and evaluate the machine learning models:

```bash
python train_model.py
```

This will:
- Load and preprocess the dataset
- Train Random Forest and XGBoost classifiers
- Evaluate both models using multiple metrics
- Automatically select the best-performing model
- Save the best model to the `models/` directory

**Expected Output:**
```
PREDICTIVE MAINTENANCE MODEL TRAINING PIPELINE
===============================================================
✓ Random Forest training completed
✓ XGBoost training completed
✓ Best model selected: [Model Name]
✓ Model saved successfully
```

### Step 2: Start the Backend Server

Launch the FastAPI backend server:

```bash
python app.py
```

The server will start at: `http://localhost:8000`

**Available Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `GET /model/info` - Model information
- `POST /predict` - Single machine prediction
- `POST /predict/batch` - Batch predictions
- `GET /simulate-and-predict` - Real-time simulation + prediction
- `GET /dashboard` - Live monitoring dashboard
- `GET /docs` - Interactive API documentation (Swagger UI)

### Step 3: Access the Dashboard

Open your web browser and navigate to:
```
http://localhost:8000/dashboard
```

The dashboard will:
- Display real-time sensor data for multiple machines
- Show failure probability for each machine
- Provide health status indicators
- Trigger alerts when maintenance is required
- Auto-refresh every 2 seconds (configurable)

## 🏗️ Project Structure

```
Predictive_maintenance/
│
├── config.py                   # Configuration settings
├── train_model.py              # Model training pipeline
├── model_inference.py          # Model inference module
├── data_simulator.py           # Real-time data generator
├── monitoring_service.py       # Integrated monitoring service
├── app.py                      # FastAPI backend application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── RUN_SYSTEM.ps1             # PowerShell script to run everything
│
├── predicrtiver_maintenance_dataset/
│   └── ai4i2020.csv           # Dataset (10,000 samples)
│
├── models/                     # Saved models (created after training)
│   ├── random_forest.pkl or xgboost.pkl
│   ├── label_encoder.pkl
│   └── model_metadata.json
│
└── static/                     # Frontend assets
    └── dashboard.html          # Real-time monitoring dashboard
```

## 🔍 How It Works

### 1. Data Preprocessing
- Removes irrelevant columns (UDI, Product ID)
- Handles missing values
- Encodes categorical features (Type: L, M, H)
- Engineers new features (temperature difference, power)
- Balances dataset using SMOTE

### 2. Model Training
- Trains Random Forest (200 trees, optimized parameters)
- Trains XGBoost (200 estimators, optimized parameters)
- Evaluates both using:
  - Accuracy
  - Precision
  - Recall
  - F1-Score
  - ROC-AUC
- Selects best model based on composite score

### 3. Real-time Monitoring
- **Data Simulator**: Generates realistic sensor data with:
  - Natural variations
  - Correlated parameters
  - Progressive tool wear
  - Occasional anomalies
  - Different operating modes

- **Prediction Engine**: 
  - Processes sensor data
  - Calculates failure probability
  - Determines health status
  - Triggers alerts

- **Dashboard**:
  - Displays 5 machines by default
  - Updates every 2 seconds
  - Shows color-coded health status
  - Displays all sensor parameters
  - Provides failure probability percentage

### 4. Health Status Thresholds
- **Healthy**: 0-30% failure probability (Green)
- **Risk**: 30-60% failure probability (Yellow)
- **Maintenance Required**: 60-100% failure probability (Red, flashing)

## 🎨 Dashboard Features

- **Live Statistics**: Total machines, healthy count, at-risk count, maintenance required
- **Machine Cards**: Individual cards for each machine showing:
  - Machine ID
  - Health status badge
  - Failure probability (large display + progress bar)
  - All sensor readings
  - Alert banner when maintenance needed
- **Controls**:
  - Pause/Resume monitoring
  - Manual refresh
  - Adjustable update interval (1s, 2s, 5s, 10s)
- **Visual Indicators**:
  - Color-coded progress bars
  - Animated alerts
  - Real-time clock
  - Last update timestamp

## 🔌 API Examples

### Single Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "machine_id": "M001",
    "Type": "M",
    "Air temperature [K]": 298.5,
    "Process temperature [K]": 308.7,
    "Rotational speed [rpm]": 1500,
    "Torque [Nm]": 45.0,
    "Tool wear [min]": 120
  }'
```

### Batch Prediction
```bash
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "machines": [
      {
        "machine_id": "M001",
        "Type": "M",
        "Air temperature [K]": 298.5,
        "Process temperature [K]": 308.7,
        "Rotational speed [rpm]": 1500,
        "Torque [Nm]": 45.0,
        "Tool wear [min]": 120
      }
    ]
  }'
```

### Real-time Simulation
```bash
curl "http://localhost:8000/simulate-and-predict"
```

## ⚙️ Configuration

Edit `config.py` to customize:

- `NUM_MACHINES`: Number of machines to simulate (default: 5)
- `SIMULATION_INTERVAL`: Update interval in seconds (default: 2)
- `FAILURE_THRESHOLD`: Probability threshold for alerts (default: 0.6)
- `API_PORT`: Backend server port (default: 8000)
- `SENSOR_RANGES`: Min/max values for each sensor

## 🧪 Testing Components

### Test Data Simulator
```bash
python data_simulator.py
```

### Test Model Inference
```bash
python model_inference.py
```

## 📈 Model Performance

After training, check `models/model_metadata.json` for:
- Model name (Random Forest or XGBoost)
- Training date
- Performance metrics:
  - Accuracy
  - Precision
  - Recall
  - F1-Score
  - ROC-AUC

Typical performance:
- Accuracy: 96-98%
- Precision: 85-95%
- Recall: 70-85%
- F1-Score: 75-88%
- ROC-AUC: 92-97%

## 🚦 System Status

The system is considered operational when:
1. ✅ Model is trained and saved in `models/` directory
2. ✅ Backend server is running on port 8000
3. ✅ Dashboard is accessible at `/dashboard`
4. ✅ Data simulator is generating realistic sensor data
5. ✅ Predictions are being made in real-time

## 🛠️ Troubleshooting

### "Model not loaded" error
- Run `python train_model.py` first to train and save the model

### Dashboard shows no data
- Ensure the backend server is running
- Check that the API is accessible at `http://localhost:8000`
- Verify the model is loaded (check `/model/info` endpoint)

### Port already in use
- Change `API_PORT` in `config.py`
- Or kill the process using port 8000

## 📝 Notes

- The system uses pseudo real-time simulation since actual industrial streaming data is unavailable
- Machine degradation and failures are simulated realistically
- Tool wear increases over time, affecting failure probability
- Some machines are randomly assigned higher degradation rates
- The dashboard uses client-side polling (not WebSocket) for simplicity

## 🎓 Learning Resources

This project demonstrates:
- End-to-end ML pipeline development
- Model comparison and selection
- REST API design with FastAPI
- Real-time data visualization
- Production-ready code structure
- Data simulation techniques
- Predictive maintenance concepts

## 📄 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

Feel free to enhance the system with:
- Additional ML models
- More sophisticated feature engineering
- WebSocket support for real-time updates
- Database integration for historical data
- Advanced alerting mechanisms
- Email/SMS notifications

---

**Built with:** Python, scikit-learn, XGBoost, FastAPI, HTML/CSS/JavaScript
