import torch
import torch.nn as nn
import pandas as pd
import numpy as np

# 1. Define the exact same Autoencoder architecture used in training
class FirewallAutoencoder(nn.Module):
    def __init__(self, input_dim):
        super(FirewallAutoencoder, self).__init__()
        # Updated encoder to match your training script dimensions (16 and 8)
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8)
        )
        # Updated decoder to match matching inverse dimensions (16 and input_dim)
        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim)
        )
        
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
def predict_anomalies():
    print("1. Loading trained model weights...")
    
    # Define features used during training
    feature_cols = ['packet_size', 'flow_duration', 'src_port', 'dst_port', 'packet_count']
    input_dim = len(feature_cols)
    
    # Initialize model and load saved state dictionary
    model = FirewallAutoencoder(input_dim)
    model.load_state_dict(torch.load('firewall_anomaly_model.pth'))
    model.eval() # Set model to evaluation mode
    
    print("2. Loading test network traffic data...")
    # Using your network logs dataset as a sample for inference
    df = pd.read_csv('../data/network_logs.csv')
    X = df[feature_cols].values
    
    # Normalize features using simple min-max or mean scaling (matching training prep)
    X_mean = X.mean(axis=0)
    X_std = X.std(axis=0)
    X_std[X_std == 0] = 1.0 # Prevent division by zero
    X_scaled = (X - X_mean) / X_std
    
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    
    print("3. Calculating anomaly scores (Reconstruction Error)...")
    with torch.no_grad():
        reconstructions = model(X_tensor)
        # Calculate Mean Squared Error per sample
        mse_loss = torch.mean((X_tensor - reconstructions) ** 2, dim=1).numpy()
        
    # Define an anomaly threshold (e.g., top highest errors or custom threshold)
    threshold = np.percentile(mse_loss, 85) # Flags top 15% highest error as anomalies
    
    df['reconstruction_error'] = mse_loss
    df['is_anomaly'] = df['reconstruction_error'] > threshold
    
    print("\n--- INFERENCE RESULTS ---")
    print(df[['packet_size', 'dst_port', 'reconstruction_error', 'is_anomaly']])

if __name__ == '__main__':
    predict_anomalies()