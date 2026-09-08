import traceback

try:
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset

    print("1. Loading dataset...")
    # Absolute path directly to your network logs CSV
    df = pd.read_csv(r'C:\Users\Abhishek Shakya\Desktop\SIH\AdaptiIQ\ai\data\network_logs.csv')

    print("2. Processing features...")
    feature_cols = ['packet_size', 'flow_duration', 'src_port', 'dst_port', 'packet_count']
    X = df[feature_cols].values
    y = df['is_attack'].values if 'is_attack' in df.columns else None

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    if y is not None:
        X_train, X_temp, y_train, y_temp = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    else:
        X_train, X_temp = train_test_split(X_scaled, test_size=0.3, random_state=42)
        X_val, X_test = train_test_split(X_temp, test_size=0.5, random_state=42)

    print("3. Setting up tensors and model...")
    train_tensor = torch.tensor(X_train, dtype=torch.float32)
    val_tensor = torch.tensor(X_val, dtype=torch.float32)

    train_dataset = TensorDataset(train_tensor, train_tensor)
    val_dataset = TensorDataset(val_tensor, val_tensor)

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)

    class NetworkAnomalyAutoencoder(nn.Module):
        def __init__(self, input_dim):
            super(NetworkAnomalyAutoencoder, self).__init__()
            self.encoder = nn.Sequential(
                nn.Linear(input_dim, 16),
                nn.ReLU(),
                nn.Linear(16, 8),
                nn.ReLU()
            )
            self.decoder = nn.Sequential(
                nn.Linear(8, 16),
                nn.ReLU(),
                nn.Linear(16, input_dim)
            )
            
        def forward(self, x):
            return self.decoder(self.encoder(x))

    input_dim = X_train.shape[1]
    model = NetworkAnomalyAutoencoder(input_dim)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("4. Starting training loop...")
    epochs = 20
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        
        for batch_data, _ in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_data)
            loss = criterion(outputs, batch_data)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item() * batch_data.size(0)
            
        epoch_loss = train_loss / len(train_loader.dataset)
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss:.4f}")

    torch.save(model.state_dict(), 'firewall_anomaly_model.pth')
    print("Model training complete and saved successfully as 'firewall_anomaly_model.pth'!")

except Exception as e:
    print("\n--- CAUGHT AN ERROR ---")
    traceback.print_exc()

input("\nPress Enter to exit...")