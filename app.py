"""
FastAPI Backend for Predictive Maintenance System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
from datetime import datetime
import os
import config
from model_inference import get_model_inference
from monitoring_service import router as monitoring_router, get_monitoring_service


# Pydantic models for request/response validation
class SensorData(BaseModel):
    machine_id: str = Field(..., description="Unique machine identifier")
    Type: str = Field(..., description="Machine type (L, M, or H)", pattern="^[LMH]$")
    air_temperature: float = Field(..., alias="Air temperature [K]", ge=290, le=310)
    process_temperature: float = Field(..., alias="Process temperature [K]", ge=300, le=320)
    rotational_speed: int = Field(..., alias="Rotational speed [rpm]", ge=1000, le=3000)
    torque: float = Field(..., alias="Torque [Nm]", ge=0, le=100)
    tool_wear: int = Field(..., alias="Tool wear [min]", ge=0, le=300)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "machine_id": "M001",
                "Type": "M",
                "Air temperature [K]": 298.5,
                "Process temperature [K]": 308.7,
                "Rotational speed [rpm]": 1500,
                "Torque [Nm]": 45.0,
                "Tool wear [min]": 120
            }
        }


class PredictionResponse(BaseModel):
    machine_id: str
    prediction: int
    failure_probability: float
    normal_probability: float
    health_status: str
    alert: bool
    timestamp: str


class BatchSensorData(BaseModel):
    machines: List[SensorData]


class ModelInfo(BaseModel):
    model_name: str
    training_date: str
    metrics: dict
    feature_columns: List[str]
    status: str


# Initialize FastAPI app
app = FastAPI(
    title="Predictive Maintenance API",
    description="AI-driven predictive maintenance system for industrial equipment monitoring",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include monitoring service router
app.include_router(monitoring_router)

# Global model inference instance
model_inference = None
monitoring_service = None


@app.on_event("startup")
async def startup_event():
    """Initialize model and monitoring service on startup"""
    global model_inference, monitoring_service
    model_inference = get_model_inference()
    monitoring_service = get_monitoring_service()  # This initializes the simulator
    print("✓ Predictive Maintenance API started successfully")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Predictive Maintenance API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #27ae60; font-weight: bold; }
            code { background: #34495e; color: #ecf0f1; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🔧 Predictive Maintenance API</h1>
        <p>AI-driven predictive maintenance system for industrial equipment monitoring</p>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/health</code><br>
            Check API health status
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/model/info</code><br>
            Get information about the loaded model
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/predict</code><br>
            Make prediction for a single machine
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/predict/batch</code><br>
            Make predictions for multiple machines
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/docs</code><br>
            Interactive API documentation (Swagger UI)
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/dashboard</code><br>
            Real-time monitoring dashboard
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model_inference.model_loaded if model_inference else False
    }


@app.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get information about the loaded model"""
    if not model_inference or not model_inference.model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return model_inference.get_model_info()


@app.post("/predict", response_model=PredictionResponse)
async def predict_single(sensor_data: SensorData):
    """
    Make prediction for a single machine
    
    Returns failure probability and health status based on sensor readings
    """
    if not model_inference or not model_inference.model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert Pydantic model to dict
        data_dict = sensor_data.model_dump(by_alias=True)
        
        # Make prediction
        result = model_inference.predict(data_dict)
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/batch")
async def predict_batch(batch_data: BatchSensorData):
    """
    Make predictions for multiple machines
    
    Returns failure probabilities and health statuses for all machines
    """
    if not model_inference or not model_inference.model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert Pydantic models to dicts
        machines_data = [machine.model_dump(by_alias=True) for machine in batch_data.machines]
        
        # Make predictions
        results = model_inference.predict(machines_data)
        
        # Add timestamps
        timestamp = datetime.now().isoformat()
        for result in results:
            result['timestamp'] = timestamp
        
        return {
            "predictions": results,
            "total_machines": len(results),
            "timestamp": timestamp
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard"""
    dashboard_path = os.path.join(os.path.dirname(__file__), "static", "dashboard.html")
    
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    else:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard Not Found</title>
        </head>
        <body>
            <h1>Dashboard not found</h1>
            <p>Please ensure the dashboard.html file exists in the static directory.</p>
        </body>
        </html>
        """, status_code=404)


if __name__ == "__main__":
    print("Starting Predictive Maintenance API server...")
    print(f"API will be available at http://{config.API_HOST}:{config.API_PORT}")
    print(f"Interactive docs at http://{config.API_HOST}:{config.API_PORT}/docs")
    
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level="info"
    )
