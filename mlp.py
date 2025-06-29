import torch
from torch import nn

device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
print(f"Using {device} device")

# Define model
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(120, 120),
            nn.ReLU(),
            nn.Linear(120, 120),
            nn.ReLU(),
            nn.Linear(120, 120),
            nn.ReLU(),
            nn.Linear(120, 120),
            nn.ReLU(),
            nn.Linear(120, 1),
        )
    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits
