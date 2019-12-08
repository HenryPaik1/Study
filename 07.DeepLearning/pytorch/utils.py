# load data
# https://towardsdatascience.com/how-to-train-an-image-classifier-in-pytorch-and-use-it-to-perform-basic-inference-on-single-images-99465a1e9bf5
# https://gist.github.com/gagejustins/76ab1f37b83684032566b276fe3a5289#file-samplers-py
# train/validation/test set: https://machinelearningmastery.com/evaluate-performance-deep-learning-models-keras/
from __future__ import print_function
import cv2
import torch
import time
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch import optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision.transforms import ToPILImage
from torch.utils.data.sampler import SubsetRandomSampler

show=ToPILImage()
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

def train_net(net, n_epochs, lr):
    # pred = F.log_softmax(x, dim=-1)
    # loss = F.nll_loss(pred, target)
    # optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    train_loader, test_loader, val_loader = load_split_train_test_datset()
    n_batches = len(train_loader)
    loss, optimizer = F.CrossEntropyLoss(), optim.Adam(net.parameters(), lr=learning_rate)
    
    running_loss = .0
    total_train_loss = 0
    #print_every = n_batches // 10
    start_time = time.time()
    train_losses, test_losses = [], []
    
    for epoch in range(n_epochs):
        for inputs, data in enumerate(train_loader, 0):
            inputs, labels = data
            inputs, labels = Variable(inputs), Variable(labels)
            optimizer.zero_grad()
            
            # forward, backward, optimize
            outputs = net(inputs)
            batch_loss = loss(outputs, labels)
            batch_loss.backward()
            optimizer.step()
            
            running_loss += batch_loss.data[0]
            total_train_loss += batch_loss.data[0]
            
            if steps % 10 == 0: # batch가 10번 돌았을 때 model의 성능
                total_val_loss = 0
                acc = 0
                net.eval()
                with torch.no_grad():
                    for inputs, labels in val_loader:
                        inputs, labels = Variable(inputs), Variable(labels)
                        val_outputs = net(inputs)
                        
                        batch_loss = loss(val_outputs, labels)
                        total_val_loss += batch_loss.data[0] # batch_loss.item()
                        
                        pred = torch.exp(val_outputs)
                        top_p, top_classes = pred.topk(1, dim=1)
                        equals = top_calsses == labels.view(*top_classes.shape)
                        accuracy += torch.mean(equals.type(torch.FloatTensor)).item()
                # 10번째 배치마다 모델성능(loss) print
                # running_loss/10는, 배치당 평균로스가 10번 더해지기 때문에, 다시 나누기 10
                train_losses.append(running_loss/len(train_loader))
                val_losses.append(total_val_loss/len(val_loader))
                print(f"epochs: {epoch+1}/{epochs} \n\
                        train loss: {running_loss/10} \n\
                        val loss: {total_val_loss/len(val_loader)} \n\
                        val acc: {accuracy/len(val_loader)} \n\
                        took: {time.time() - start_time}")
                running_loss = 0
                start_time = time.time()
                net.train()
    
        # 매 epoch당 test score
        total_test_loss = 0
        for inputs, labels in test_loader:
            inputs, labels = Variable(inputs), Variable(labels)
            test_outputs = net(inputs)
            batch_loss = loss(test_outputs, labels)
            total_test_loss += batch_loss
        print(f"test loss = {total_test_loss / len(test_loader)}")
    
                                                           
def load_split_train_test_datset():
    transform = transforms.Compose(
        [transforms.Resize(224), transforms.ToTensor(), transforms.Normalize([0.5], [0.5])]
    )
    train_set = torchvision.datasets.FashionMNIST(root='../data', train=True, download=True, transform=transform)
    test_set = torchvision.datasets.FashionMNIST(root='../data', train=True, download=False, transform=transform)
    
    # training
    n_training_samples = 20000
    train_sampler = SubsetRandomSampler(np.arange(n_training_samples, dtype=np.int64))
    
    # val
    n_val_samples = 5000
    val_sampler = SubsetRandomSampler(np.arnage(n_training_samples, n_training_samples + n_val_samples))
    
    # test
    n_test_samples = 5000
    test_sampler = SubsetRandomSampler(np.arange(n_test_samples, dtype=np.int64))
    
    # get loader
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=64, sampler=train_sampler)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=64, sampler=test_sampler)
    val_loader = torch.utils.data.DataLoader(train_set, batch_size=128, sampler=val_sampler)
    
    return train_loader, test_loader, val_loader