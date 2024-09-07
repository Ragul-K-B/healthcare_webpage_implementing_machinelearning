import torch
import torch.optim as optim
from model import Model
from dataloader import load_data

# Configuration
input_dim = 13
learning_rate = 0.001
num_epochs = 10  # Number of training epochs

# Initialize model, loss function, and optimizer
model = Model(input_dim)
criterion = torch.nn.BCELoss()  # Binary Cross-Entropy Loss for binary classification
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Load data
train_loader, test_loader = load_data('heart.csv', input_dim)  # Update 'data.csv' to your dataset path

# Training loop
for epoch in range(num_epochs):
    model.train()  # Set model to training mode
    running_loss = 0.0

    for features, targets in train_loader:
        optimizer.zero_grad()  # Clear previous gradients

        outputs = model(features)  # Forward pass
        loss = criterion(outputs, targets)  # Compute loss

        loss.backward()  # Backward pass
        optimizer.step()  # Update model weights

        running_loss += loss.item() * features.size(0)  # Accumulate loss

    epoch_loss = running_loss / len(train_loader.dataset)
    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {epoch_loss:.4f}')

# Save the trained model
torch.save(model.state_dict(), 'model.pth')
print('Model saved to model.pth')

