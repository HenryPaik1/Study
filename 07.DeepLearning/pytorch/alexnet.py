# model code: https://github.com/dansuh17/alexnet-pytorch/blob/master/model.py
# model code2: https://github.com/pytorch/vision/blob/master/torchvision/models/alexnet.py
# cal params & pictures: https://www.learnopencv.com/number-of-parameters-and-tensor-sizes-in-convolutional-neural-network/

class Alexnet(nn.Model):
    def __init__(self, num_classes=1000):
        super(Alexnet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=96, kernel_size=11, stride=4),
            nn.ReLu(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2), 
            # input data = (227, 227, 3) <- 논문은 224라고 했지만 not make sense
            # output shape after conv = ((227-11)/4 + 1 = 55, 55, 96)
            # output shape after pool = ((55 - 3)/2 + 1 = 27, 27, 96)
            # num of params = (11*11)*3*96 + 96 ?왜 채널갯수는 다시 곱하지 않는지?
            
            nn.Conv2d(in_channels=96, out_channels=256, kernel_size=5, stride=1, padding=2),
            nn.ReLu(),
            nn.MaxPool2d(kernel_size=3, stride=2),
            # output shape after after 2nd conv = ((27 + 2*2 - 5)/1 + 1 = 27, 27, 256) 
            # output shape after pool = ((27 - 3) / 2 + 1 = 13, 13, 256)
            # num of params = (5*5)*96*256 + 256
            
            nn.Conv2d(in_channles=256, out_channels=384, kernel_size=3, stride=1, padding=1),
            nn.ReLu(),
            # output shape after after 2nd conv = ((13 + 1*2 - 5)/1 + 1 = 13, 13, 384)
            
            nn.Conv2d(in_channels=384, out_channels=384, kernel_size=3, stride=1, padding=1),
            nn.ReLu(),
            # output shape after after 2nd conv = ((13 + 1*2  - 3)/1 + 1 = 13, 13, 384) 
            
            nn.Conv2d(in_channels=384, out_channels=256, kernel_size=3, stride=1, padding=1),
            nn.ReLu(),
            nn.MaxPool2d(kernel_size=3, stride=2),
            # output shape after after 2nd conv = ((13 + 1*2  - 3)/1 + 1 = 13, 13, 256)
            # output shape after pool = ((13 - 3) / 2 + 1 = 6, 6, 256) 
            
        # FC * 3
        self.classfier = nn.Sequential(
            nn.Dropout(p=0.5, inplcae=True),
            nn.Linear(in_features=(6*6*256), out_features=4096),
            nn.ReLu(),
            nn.Linear(in_features=4096, out_features=4096),
            nn.ReLu(),
            # 마지막 레이어에는 no Non-linear func
            nn.Linear(in_features=4096, out_features=num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        output = self.classifier(x)
        return output
            
# train code: https://github.com/pytorch/examples/blob/master/mnist/main.py
            