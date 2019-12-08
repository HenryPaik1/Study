from torch.autograd import Variable
import torch.nn.functional as F

class SimpleCNN(torch.nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        
        # input = (3, 32, 32)
        self.features = torch.nn.Sequential(
            torch.nn.Conv2d(3, 18, kernel_size=3, stride=1, padding=1), # (18, (32 + 1 * 2 - 3) / 1 + 1 = 32, 32)
            torch.nn.ReLu(inplace=True),
            torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0) # (18, (32 - 2) / 2 + 1 = 16, 16)
        )
        
        # fully connected layer
        self.classifier = torch.nn.Sequential(
            torch.nn.Linear(18 * 16 * 16, 64),
            torch.nn.ReLu(inplace=True)
            torch.nn.Linear(64, 10)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(out, 1)
        # x = x.view(-1, 18*16*16)
        x = self.classifier(x)
        return x
