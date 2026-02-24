"""
Configuration file for Predictive Maintenance System
Supports both local development and production deployment
"""
import os

# Environment
ENV = os.getenv('ENV', 'development')  # development or production
DEBUG = ENV == 'development'

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "predicrtiver_maintenance_dataset")
MODEL_DIR = os.path.join(BASE_DIR, "models")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Dataset
DATASET_PATH = os.path.join(DATA_DIR, "ai4i2020.csv")

# Model parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# Features to drop
DROP_COLUMNS = ['UDI', 'Product ID']

# Target column
TARGET_COLUMN = 'Machine failure'

# API Configuration - Use environment variables for production
API_HOST = os.getenv('HOST', '0.0.0.0')
API_PORT = int(os.getenv('PORT', 8000))

# Real-time simulation
SIMULATION_INTERVAL = 2  # seconds
NUM_MACHINES = 5
FAILURE_THRESHOLD = 0.6  # Probability threshold for maintenance alert

# Health status thresholds
HEALTH_STATUS = {
    'healthy': (0, 0.3),
    'risk': (0.3, 0.6),
    'maintenance_required': (0.6, 1.0)
}

# Sensor value ranges (for simulation)
SENSOR_RANGES = {
    'Air temperature [K]': (295, 304),
    'Process temperature [K]': (305, 313),
    'Rotational speed [rpm]': (1200, 2500),
    'Torque [Nm]': (15, 70),
    'Tool wear [min]': (0, 250),
    'Type': ['L', 'M', 'H']
}
