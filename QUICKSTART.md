# Quick Start Guide

This is a comprehensive AI-driven predictive maintenance system. Follow these steps to get started:

## Quick Start (3 Steps)

### Option A: Automated (Recommended)
```powershell
# Run this single command:
.\RUN_SYSTEM.ps1
```

This will automatically:
1. Train the model (if not already trained)
2. Start the backend server
3. Enable the real-time dashboard

### Option B: Manual
```powershell
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Train the model
python train_model.py

# Step 3: Start the server
python app.py
```

## Access the System

Once the server is running:

1. **Dashboard**: http://localhost:8000/dashboard
   - Real-time monitoring of 5 machines
   - Live failure probability updates
   - Health status indicators
   - Sensor parameter displays

2. **API Documentation**: http://localhost:8000/docs
   - Interactive Swagger UI
   - Test all endpoints
   - View request/response schemas

3. **API Health Check**: http://localhost:8000/health
   - Verify system status

## What to Expect

### Training Phase (First Run)
- Loads AI4I 2020 dataset (10,000 samples)
- Preprocesses data and engineers features
- Trains Random Forest and XGBoost models
- Evaluates both models
- Selects best model automatically
- Saves model to `models/` directory
- **Duration**: ~30-60 seconds

### Runtime Phase
- Backend server starts on port 8000
- Data simulator generates realistic sensor data
- Dashboard updates every 2 seconds
- Predictions made in real-time
- Alerts triggered when failure probability > 60%

## Dashboard Features

You'll see:
- 5 machine cards with live updates
- Statistics: Total machines, healthy, at risk, maintenance required
- Each machine shows:
  - Machine ID (M001 - M005)
  - Health status badge (color-coded)
  - Failure probability (percentage + progress bar)
  - All sensor readings (temperature, speed, torque, wear)
  - Alert banner if maintenance needed

## Controls

- **Pause/Resume**: Stop/start automatic updates
- **Refresh Now**: Manually trigger update
- **Update Interval**: Change refresh rate (1s, 2s, 5s, 10s)

## Testing

### Test Individual Components

```powershell
# Test data simulator
python data_simulator.py

# Test model inference
python model_inference.py
```

## Troubleshooting

### Common Issues

1. **"Model not found" error**
   - Solution: Run `python train_model.py`

2. **"Port 8000 already in use"**
   - Solution: Change `API_PORT` in `config.py`
   - Or: Kill process on port 8000

3. **Dashboard shows no data**
   - Check server is running
   - Verify http://localhost:8000/health shows "healthy"
   - Check browser console for errors

4. **ImportError or ModuleNotFoundError**
   - Solution: Run `pip install -r requirements.txt`

## System Requirements

- Python 3.8 or higher
- 4GB RAM minimum
- Windows/Linux/macOS
- Modern web browser (Chrome, Firefox, Edge)

## Next Steps

1. Watch the dashboard for a few minutes to see machines degrade
2. Try the API at http://localhost:8000/docs
3. Adjust settings in `config.py`:
   - Number of machines
   - Update interval
   - Failure threshold
   - Sensor ranges

## Architecture

```
User Request → FastAPI Backend → Monitoring Service
                                      ↓
                           ┌──────────┴──────────┐
                           ↓                     ↓
                    Data Simulator      Model Inference
                           ↓                     ↓
                    Sensor Data          Predictions
                           └──────────┬──────────┘
                                      ↓
                              Dashboard Display
```

## Support

For detailed information, see README.md

---

**Enjoy monitoring your machines!** 🔧
