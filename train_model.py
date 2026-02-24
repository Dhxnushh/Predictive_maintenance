"""
Data Preprocessing and Model Training Pipeline
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, classification_report, 
                             confusion_matrix)
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
import joblib
import os
import json
from datetime import datetime
import config


class PredictiveMaintenanceModel:
    """
    Complete pipeline for training and evaluating predictive maintenance models
    """
    
    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.best_model = None
        self.best_model_name = None
        self.feature_columns = None
        self.metrics = {}
        
    def load_data(self):
        """Load the dataset"""
        print("Loading dataset...")
        df = pd.read_csv(config.DATASET_PATH)
        print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    
    def preprocess_data(self, df):
        """
        Preprocess the data:
        - Remove irrelevant columns
        - Handle missing values
        - Encode categorical features
        - Feature engineering
        """
        print("\nPreprocessing data...")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.any():
            print(f"Missing values found:\n{missing_values[missing_values > 0]}")
            df = df.fillna(df.mean(numeric_only=True))
        else:
            print("No missing values found")
        
        # Drop irrelevant columns
        df_processed = df.drop(columns=config.DROP_COLUMNS)
        
        # Rename columns to remove special characters (required for XGBoost)
        column_mapping = {
            'Air temperature [K]': 'Air_temperature_K',
            'Process temperature [K]': 'Process_temperature_K',
            'Rotational speed [rpm]': 'Rotational_speed_rpm',
            'Torque [Nm]': 'Torque_Nm',
            'Tool wear [min]': 'Tool_wear_min'
        }
        df_processed = df_processed.rename(columns=column_mapping)
        
        # Encode categorical 'Type' column
        df_processed['Type_encoded'] = self.label_encoder.fit_transform(df_processed['Type'])
        df_processed = df_processed.drop(columns=['Type'])
        
        # Additional feature engineering
        df_processed['Temp_diff'] = df_processed['Process_temperature_K'] - df_processed['Air_temperature_K']
        df_processed['Power'] = df_processed['Torque_Nm'] * df_processed['Rotational_speed_rpm'] / 1000
        
        print(f"Preprocessed data shape: {df_processed.shape}")
        print(f"Features: {df_processed.columns.tolist()}")
        
        return df_processed
    
    def prepare_features(self, df):
        """Separate features and target"""
        # Features: all columns except target and failure type columns
        failure_cols = ['Machine failure', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF']
        
        # Target
        y = df[config.TARGET_COLUMN]
        
        # Features (drop all failure-related columns)
        X = df.drop(columns=failure_cols)
        
        self.feature_columns = X.columns.tolist()
        
        print(f"\nFeature columns: {self.feature_columns}")
        print(f"Target distribution:\n{y.value_counts()}")
        print(f"Failure rate: {y.mean():.2%}")
        
        return X, y
    
    def balance_dataset(self, X_train, y_train):
        """Balance the dataset using SMOTE"""
        print("\nApplying SMOTE to balance the dataset...")
        print(f"Before SMOTE: {y_train.value_counts().to_dict()}")
        
        smote = SMOTE(random_state=config.RANDOM_STATE)
        X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
        
        print(f"After SMOTE: {pd.Series(y_resampled).value_counts().to_dict()}")
        
        return X_resampled, y_resampled
    
    def train_random_forest(self, X_train, y_train):
        """Train Random Forest classifier"""
        print("\n" + "="*60)
        print("Training Random Forest Classifier...")
        print("="*60)
        
        rf_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=config.RANDOM_STATE,
            n_jobs=-1,
            class_weight='balanced'
        )
        
        rf_model.fit(X_train, y_train)
        print("Random Forest training completed")
        
        return rf_model
    
    def train_xgboost(self, X_train, y_train):
        """Train XGBoost classifier"""
        print("\n" + "="*60)
        print("Training XGBoost Classifier...")
        print("="*60)
        
        # Calculate scale_pos_weight for imbalanced data
        scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
        
        xgb_model = XGBClassifier(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=scale_pos_weight,
            random_state=config.RANDOM_STATE,
            use_label_encoder=False,
            eval_metric='logloss'
        )
        
        xgb_model.fit(X_train, y_train)
        print("XGBoost training completed")
        
        return xgb_model
    
    def evaluate_model(self, model, model_name, X_test, y_test):
        """Evaluate model performance"""
        print(f"\n{'='*60}")
        print(f"Evaluating {model_name}")
        print(f"{'='*60}")
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc
        }
        
        print(f"\nAccuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-Score:  {f1:.4f}")
        print(f"ROC-AUC:   {roc_auc:.4f}")
        
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        print(f"\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return metrics
    
    def select_best_model(self, models_metrics):
        """
        Automatically select the best model based on F1-score and ROC-AUC
        """
        print("\n" + "="*60)
        print("MODEL SELECTION")
        print("="*60)
        
        # Create comparison DataFrame
        comparison = pd.DataFrame(models_metrics).T
        print("\nModel Comparison:")
        print(comparison)
        
        # Calculate composite score (weighted average of F1 and ROC-AUC)
        comparison['composite_score'] = (comparison['f1_score'] * 0.5 + 
                                         comparison['roc_auc'] * 0.5)
        
        best_model_name = comparison['composite_score'].idxmax()
        
        print(f"\n{'='*60}")
        print(f"BEST MODEL: {best_model_name}")
        print(f"{'='*60}")
        print(f"Composite Score: {comparison.loc[best_model_name, 'composite_score']:.4f}")
        
        return best_model_name, comparison
    
    def save_model(self, model, model_name, label_encoder, feature_columns, metrics):
        """Save the trained model and metadata"""
        # Create models directory if it doesn't exist
        os.makedirs(config.MODEL_DIR, exist_ok=True)
        
        # Save model
        model_path = os.path.join(config.MODEL_DIR, f'{model_name}.pkl')
        joblib.dump(model, model_path)
        print(f"\nModel saved to: {model_path}")
        
        # Save label encoder
        encoder_path = os.path.join(config.MODEL_DIR, 'label_encoder.pkl')
        joblib.dump(label_encoder, encoder_path)
        print(f"Label encoder saved to: {encoder_path}")
        
        # Save metadata
        metadata = {
            'model_name': model_name,
            'feature_columns': feature_columns,
            'metrics': metrics,
            'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'random_state': config.RANDOM_STATE
        }
        
        metadata_path = os.path.join(config.MODEL_DIR, 'model_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        print(f"Metadata saved to: {metadata_path}")
    
    def run_pipeline(self):
        """Execute the complete training pipeline"""
        print("\n" + "="*60)
        print("PREDICTIVE MAINTENANCE MODEL TRAINING PIPELINE")
        print("="*60)
        
        # Step 1: Load data
        df = self.load_data()
        
        # Step 2: Preprocess data
        df_processed = self.preprocess_data(df)
        
        # Step 3: Prepare features and target
        X, y = self.prepare_features(df_processed)
        
        # Step 4: Split data
        print("\nSplitting data into train and test sets...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=config.TEST_SIZE, 
            random_state=config.RANDOM_STATE,
            stratify=y
        )
        print(f"Training set: {X_train.shape[0]} samples")
        print(f"Test set: {X_test.shape[0]} samples")
        
        # Step 5: Balance training data
        X_train_balanced, y_train_balanced = self.balance_dataset(X_train, y_train)
        
        # Step 6: Train models
        rf_model = self.train_random_forest(X_train_balanced, y_train_balanced)
        xgb_model = self.train_xgboost(X_train_balanced, y_train_balanced)
        
        # Step 7: Evaluate models
        rf_metrics = self.evaluate_model(rf_model, "Random Forest", X_test, y_test)
        xgb_metrics = self.evaluate_model(xgb_model, "XGBoost", X_test, y_test)
        
        # Step 8: Select best model
        models_metrics = {
            'Random Forest': rf_metrics,
            'XGBoost': xgb_metrics
        }
        
        models = {
            'Random Forest': rf_model,
            'XGBoost': xgb_model
        }
        
        best_model_name, comparison = self.select_best_model(models_metrics)
        self.best_model = models[best_model_name]
        self.best_model_name = best_model_name
        
        # Step 9: Save best model
        self.save_model(
            self.best_model,
            best_model_name.lower().replace(' ', '_'),
            self.label_encoder,
            self.feature_columns,
            models_metrics[best_model_name]
        )
        
        print("\n" + "="*60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("="*60)
        
        return self.best_model, self.best_model_name, self.feature_columns


if __name__ == "__main__":
    # Run the training pipeline
    pipeline = PredictiveMaintenanceModel()
    model, model_name, features = pipeline.run_pipeline()
    
    print(f"\n✓ Best model ({model_name}) is ready for deployment!")
