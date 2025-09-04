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
        self.linear_relu_stack.apply(self.init_weights)

    def init_weights(self, m):
        if isinstance(m, nn.Linear):
            #torch.nn.init.zeros_(m.weight)
            m.weight.data.uniform_(-0.01, 0.01)
            m.bias.data.fill_(0)
    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits
