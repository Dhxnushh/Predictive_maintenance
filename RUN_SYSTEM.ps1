# Predictive Maintenance System - Startup Script
# This script trains the model (if needed) and starts the monitoring system

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Predictive Maintenance System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if models directory exists and contains model
$modelsDir = "models"
$modelMetadata = Join-Path $modelsDir "model_metadata.json"

if (-not (Test-Path $modelMetadata)) {
    Write-Host "⚠ Model not found. Training model first..." -ForegroundColor Yellow
    Write-Host ""
    
    # Train the model
    python train_model.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ Model training failed!" -ForegroundColor Red
        Write-Host "Please check the error messages above." -ForegroundColor Red
        pause
        exit 1
    }
    
    Write-Host ""
    Write-Host "✅ Model training completed successfully!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "✅ Model already trained" -ForegroundColor Green
    Write-Host ""
}

# Display instructions
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Backend Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Dashboard will be available at:" -ForegroundColor Green
Write-Host "   http://localhost:8000/dashboard" -ForegroundColor White
Write-Host ""
Write-Host "📖 API Documentation available at:" -ForegroundColor Green
Write-Host "   http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "⚙️  API Endpoints:" -ForegroundColor Green
Write-Host "   http://localhost:8000/health" -ForegroundColor White
Write-Host "   http://localhost:8000/model/info" -ForegroundColor White
Write-Host "   http://localhost:8000/simulate-and-predict" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start the FastAPI server
python app.py
