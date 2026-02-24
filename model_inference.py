"""
Model Inference Module for Predictive Maintenance
"""
import joblib
import json
import os
import numpy as np
import pandas as pd
import config


class ModelInference:
    """
    Handle model loading and inference for predictive maintenance
    """
    
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.feature_columns = None
        self.metadata = None
        self.model_loaded = False
        
    def load_model(self, model_name=None):
        """
        Load the trained model and associated artifacts
        """
        try:
            # Load metadata to get model name and features
            metadata_path = os.path.join(config.MODEL_DIR, 'model_metadata.json')
            
            if not os.path.exists(metadata_path):
                raise FileNotFoundError(
                    "Model metadata not found. Please train the model first using train_model.py"
                )
            
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            
            # Use metadata model name if not specified
            if model_name is None:
                model_name = self.metadata['model_name']
            
            # Load model
            model_path = os.path.join(config.MODEL_DIR, f'{model_name}.pkl')
            self.model = joblib.load(model_path)
            
            # Load label encoder
            encoder_path = os.path.join(config.MODEL_DIR, 'label_encoder.pkl')
            self.label_encoder = joblib.load(encoder_path)
            
            # Load feature columns
            self.feature_columns = self.metadata['feature_columns']
            
            self.model_loaded = True
            
            print(f"✓ Model loaded successfully: {model_name}")
            print(f"  Training date: {self.metadata['training_date']}")
            print(f"  Metrics: {self.metadata['metrics']}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            self.model_loaded = False
            return False
    
    def preprocess_input(self, sensor_data):
        """
        Preprocess input sensor data for prediction
        
        Args:
            sensor_data (dict): Dictionary containing sensor values
                Required keys: 'Type', 'Air temperature [K]', 'Process temperature [K]',
                              'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]'
        
        Returns:
            np.array: Preprocessed features ready for prediction
        """
        # Encode Type
        type_encoded = self.label_encoder.transform([sensor_data['Type']])[0]
        
        # Extract sensor values (handle both formats)
        air_temp = sensor_data.get('Air temperature [K]') or sensor_data.get('Air_temperature_K')
        process_temp = sensor_data.get('Process temperature [K]') or sensor_data.get('Process_temperature_K')
        speed = sensor_data.get('Rotational speed [rpm]') or sensor_data.get('Rotational_speed_rpm')
        torque = sensor_data.get('Torque [Nm]') or sensor_data.get('Torque_Nm')
        tool_wear = sensor_data.get('Tool wear [min]') or sensor_data.get('Tool_wear_min')
        
        # Calculate engineered features
        temp_diff = process_temp - air_temp
        power = torque * speed / 1000
        
        # Create feature dictionary in correct order (using cleaned names)
        features = {
            'Air_temperature_K': air_temp,
            'Process_temperature_K': process_temp,
            'Rotational_speed_rpm': speed,
            'Torque_Nm': torque,
            'Tool_wear_min': tool_wear,
            'Type_encoded': type_encoded,
            'Temp_diff': temp_diff,
            'Power': power
        }
        
        # Create DataFrame with features in correct order
        df = pd.DataFrame([features])
        df = df[self.feature_columns]
        
        return df.values
    
    def predict(self, sensor_data):
        """
        Make prediction for given sensor data
        
        Args:
            sensor_data (dict or list): Sensor data for one or multiple machines
        
        Returns:
            dict: Prediction results including failure probability and health status
        """
        if not self.model_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Handle single prediction
        if isinstance(sensor_data, dict):
            sensor_data = [sensor_data]
        
        predictions = []
        
        for data in sensor_data:
            # Preprocess input
            features = self.preprocess_input(data)
            
            # Get prediction and probability
            prediction = self.model.predict(features)[0]
            probability = self.model.predict_proba(features)[0]
            
            # Determine health status
            failure_prob = float(probability[1])  # Convert numpy.float to Python float
            health_status = self._get_health_status(failure_prob)
            
            # Clean sensor_data to ensure all values are JSON-serializable
            clean_sensor_data = {}
            for key, value in data.items():
                if isinstance(value, (np.integer, np.floating)):
                    clean_sensor_data[key] = float(value)
                elif isinstance(value, np.ndarray):
                    clean_sensor_data[key] = value.tolist()
                elif isinstance(value, np.bool_):
                    clean_sensor_data[key] = bool(value)
                else:
                    clean_sensor_data[key] = value
            
            result = {
                'machine_id': data.get('machine_id', 'Unknown'),
                'prediction': int(prediction),  # Convert numpy.int to Python int
                'failure_probability': round(failure_prob, 4),
                'normal_probability': round(float(probability[0]), 4),  # Convert to float
                'health_status': health_status,
                'sensor_data': clean_sensor_data,
                'alert': bool(failure_prob >= config.FAILURE_THRESHOLD)  # Convert to bool
            }
            
            predictions.append(result)
        
        return predictions if len(predictions) > 1 else predictions[0]
    
    def _get_health_status(self, failure_probability):
        """
        Determine health status based on failure probability
        """
        for status, (min_prob, max_prob) in config.HEALTH_STATUS.items():
            if min_prob <= failure_probability < max_prob:
                return status.upper().replace('_', ' ')
        
        return "MAINTENANCE REQUIRED"
    
    def get_model_info(self):
        """
        Get information about the loaded model
        """
        if not self.model_loaded:
            return {"error": "Model not loaded"}
        
        return {
            "model_name": self.metadata['model_name'],
            "training_date": self.metadata['training_date'],
            "metrics": self.metadata['metrics'],
            "feature_columns": self.feature_columns,
            "status": "loaded"
        }


# Singleton instance
_model_inference = None

def get_model_inference():
    """
    Get or create ModelInference singleton instance
    """
    global _model_inference
    if _model_inference is None:
        _model_inference = ModelInference()
        _model_inference.load_model()
    return _model_inference


if __name__ == "__main__":
    # Test inference
    inference = ModelInference()
    inference.load_model()
    
    # Sample sensor data
    test_data = {
        'machine_id': 'M001',
        'Type': 'M',
        'Air temperature [K]': 298.1,
        'Process temperature [K]': 308.6,
        'Rotational speed [rpm]': 1551,
        'Torque [Nm]': 42.8,
        'Tool wear [min]': 150
    }
    
    result = inference.predict(test_data)
    print("\nTest Prediction:")
    print(json.dumps(result, indent=2))
