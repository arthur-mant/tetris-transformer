import torch
from torch import nn

device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
print(f"Using {device} device")

# Define model
class MLP(nn.Module):
    def __init__(self, use_encoding):
        if use_encoding:
            layer_size = 120
        else:
            layer_size = 201
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(layer_size, 100),
            nn.ReLU(),
            nn.Linear(100, 100),
            nn.ReLU(),
            nn.Linear(100, 100),
            nn.ReLU(),
            nn.Linear(100, 1),
            nn.Tanh()
        )
    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits
