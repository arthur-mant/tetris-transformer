import torch
from torch import nn

device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
print(f"Using {device} device")

# Define model
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.convolution_layer = nn.Conv2d(1, 20, kernel_size=4)
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(4001, 400),
            nn.ReLU(),
            nn.Linear(400, 200),
            nn.ReLU(),
            nn.Linear(200, 100),
            nn.ReLU(),
            nn.Linear(100, 1),
            nn.Tanh()
        )
        #self.linear_relu_stack.apply(self.init_weights)

    #def init_weights(self, m):
        #if isinstance(m, nn.Linear):
            #m.weight.data.uniform_(-0.01, 0.01)
            #m.bias.data.fill_(0)

    def forward(self, board, piece):
        conv_out = self.convolution_layer(board)
        x = conv_out.view(-1, 4000)
        x = torch.cat((x, piece), 1)
        logits = self.linear_relu_stack(x)
        return logits
