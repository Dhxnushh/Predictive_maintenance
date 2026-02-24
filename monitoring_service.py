"""
Integrated monitoring system that combines data simulation and prediction
"""
import asyncio
from fastapi import APIRouter
from typing import List, Dict
from data_simulator import get_simulator
from model_inference import get_model_inference
import config

router = APIRouter()


class MonitoringService:
    """
    Service that coordinates data simulation and real-time predictions
    """
    
    def __init__(self):
        self.simulator = get_simulator()
        self.model_inference = get_model_inference()
        
    def get_real_time_predictions(self) -> List[Dict]:
        """
        Generate sensor data and make predictions for all machines
        """
        # Generate sensor data for all machines
        sensor_data = self.simulator.generate_data()
        
        # Make predictions
        predictions = self.model_inference.predict(sensor_data)
        
        return predictions
    
    def get_machine_prediction(self, machine_id: str) -> Dict:
        """
        Generate sensor data and prediction for a specific machine
        """
        # Generate sensor data for specific machine
        sensor_data = self.simulator.generate_data(machine_id=machine_id)
        
        # Make prediction
        prediction = self.model_inference.predict(sensor_data)
        
        return prediction
    
    def perform_maintenance(self, machine_id: str) -> bool:
        """
        Reset machine tool wear (simulate maintenance)
        """
        return self.simulator.perform_maintenance(machine_id)
    
    def get_machines_status(self) -> List[Dict]:
        """
        Get status of all machines
        """
        return self.simulator.get_machines_info()


# Create global monitoring service instance
_monitoring_service = None

def get_monitoring_service():
    """Get or create monitoring service singleton"""
    global _monitoring_service
    if _monitoring_service is None:
        _monitoring_service = MonitoringService()
    return _monitoring_service


# API endpoints
@router.get("/simulate-and-predict")
async def simulate_and_predict():
    """
    Generate sensor data and predictions for all machines
    This is the main endpoint used by the dashboard
    """
    service = get_monitoring_service()
    predictions = service.get_real_time_predictions()
    return predictions


@router.get("/machines/status")
async def get_machines_status():
    """
    Get status information for all machines
    """
    service = get_monitoring_service()
    status = service.get_machines_status()
    return status


@router.post("/machines/{machine_id}/maintenance")
async def perform_maintenance(machine_id: str):
    """
    Perform maintenance on a specific machine (reset tool wear)
    """
    service = get_monitoring_service()
    success = service.perform_maintenance(machine_id)
    
    if success:
        return {
            "success": True,
            "message": f"Maintenance performed on {machine_id}",
            "machine_id": machine_id
        }
    else:
        return {
            "success": False,
            "message": f"Machine {machine_id} not found"
        }


@router.get("/machines/{machine_id}/predict")
async def predict_machine(machine_id: str):
    """
    Get prediction for a specific machine
    """
    service = get_monitoring_service()
    prediction = service.get_machine_prediction(machine_id)
    return prediction
