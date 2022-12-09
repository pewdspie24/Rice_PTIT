import torch.nn as nn
import torch

class PMG_ResNet50(nn.Module):
    def __init__(self, model, feature_size, classes_num):
        super(PMG_ResNet50, self).__init__()

        self.features = model
        self.max1 = nn.MaxPool2d(kernel_size=56, stride=56)
        self.max2 = nn.MaxPool2d(kernel_size=28, stride=28)
        self.max3 = nn.MaxPool2d(kernel_size=14, stride=14)
        self.num_ftrs = 2048 * 1 * 1
        self.elu = nn.ELU(inplace=True)

        self.classifier_concat = nn.Sequential(
            nn.BatchNorm1d(1024 * 3),
            nn.Linear(1024 * 3, feature_size),
            nn.BatchNorm1d(feature_size),
            nn.ELU(inplace=True),
            nn.Linear(feature_size, classes_num),
        )

        self.conv_block1 = nn.Sequential(
            BasicConv(self.num_ftrs//4, feature_size, kernel_size=1, stride=1, padding=0, relu=True),
            BasicConv(feature_size, self.num_ftrs//2, kernel_size=3, stride=1, padding=1, relu=True)
        )
        self.classifier1 = nn.Sequential(
            nn.BatchNorm1d(self.num_ftrs//2),
            nn.Linear(self.num_ftrs//2, feature_size),
            nn.BatchNorm1d(feature_size),
            nn.ELU(inplace=True),
            nn.Linear(feature_size, classes_num),
        )

        self.conv_block2 = nn.Sequential(
            BasicConv(self.num_ftrs//2, feature_size, kernel_size=1, stride=1, padding=0, relu=True),
            BasicConv(feature_size, self.num_ftrs//2, kernel_size=3, stride=1, padding=1, relu=True)
        )
        self.classifier2 = nn.Sequential(
            nn.BatchNorm1d(self.num_ftrs//2),
            nn.Linear(self.num_ftrs//2, feature_size),
            nn.BatchNorm1d(feature_size),
            nn.ELU(inplace=True),
            nn.Linear(feature_size, classes_num),
        )

        self.conv_block3 = nn.Sequential(
            BasicConv(self.num_ftrs, feature_size, kernel_size=1, stride=1, padding=0, relu=True),
            BasicConv(feature_size, self.num_ftrs//2, kernel_size=3, stride=1, padding=1, relu=True)
        )
        self.classifier3 = nn.Sequential(
            nn.BatchNorm1d(self.num_ftrs//2),
            nn.Linear(self.num_ftrs//2, feature_size),
            nn.BatchNorm1d(feature_size),
            nn.ELU(inplace=True),
            nn.Linear(feature_size, classes_num),
        )

    def forward(self, x):
        xf1, xf2, xf3, xf4, xf5 = self.features(x)
        # print("x1", xf1.shape)
        # print("x2", xf1.shape)
        # print("x3", xf1.shape)
        # print("x4", xf1.shape)
        # print("x5", xf1.shape)
        xl1 = self.conv_block1(xf3)
        # print('xl1: ', xl1.shape)
        xl2 = self.conv_block2(xf4)
        # print('xl2: ', xl2.shape)
        xl3 = self.conv_block3(xf5)
        # print('xl3: ', xl3.shape)
        
        xl1 = self.max1(xl1)
        # print('xl1: ', xl1.shape)
        xl1 = xl1.view(xl1.size(0), -1)
        # print('xl1: ', xl1.shape)
        xc1 = self.classifier1(xl1)
        # print('xc1: ', xc1.shape)

        xl2 = self.max2(xl2)
        # print('xl2: ', xl2.shape)
        xl2 = xl2.view(xl2.size(0), -1)
        # print('xl2: ', xl2.shape)
        xc2 = self.classifier2(xl2)
        # print('xc2: ', xc2.shape)

        xl3 = self.max3(xl3)
        # print('xl3: ', xl3.shape)
        xl3 = xl3.view(xl3.size(0), -1)
        # print('xl3: ', xl3.shape)
        xc3 = self.classifier3(xl3)
        # print('xc3: ', xc3.shape)
          
        x_concat = torch.cat((xl1, xl2, xl3), -1)
        # print('x_concat: ', x_concat.shape)
        x_concat = self.classifier_concat(x_concat)
        # print('x_concat: ', x_concat.shape)
        # print("done foward")
        return xc1, xc2, xc3, x_concat

class PMG_InceptionNetv3(nn.Module):
    def __init__(self, model, feature_size, classes_num):
        super(PMG_InceptionNetv3, self).__init__()

        self.features = model
        self.max1 = nn.MaxPool2d(kernel_size=53, stride=53)
        self.max2 = nn.MaxPool2d(kernel_size=26, stride=26)
        self.max3 = nn.MaxPool2d(kernel_size=12, stride=12)
        self.num_ftrs = 768 * 1 * 1
        self.elu = nn.ELU(inplace=True)
        self.classifier_concat = nn.Sequential(
            nn.BatchNorm1d(768 * 3),
            nn.Linear(768 * 3, feature_size),
            nn.BatchNorm1d(feature_size),
            nn.ELU(inplace=True),
            nn.Linear(feature_size, classes_num),
        )

        self.conv_block1 = nn.Sequential(
            BasicConv(288, feature_size, kernel_size=1, stride=1, padding=0, relu=True),
            BasicConv(feature_size, self.num_ftrs, kernel_size=3, stride=1, padding=1, relu=True)
        )
        self.classifier1 = nn.Sequential(
            nn.BatchNorm1d(self.num_ftrs),
            nn.Linear(self.num_ftrs, feature_size),
            nn.BatchNorm1d(feature_size),
            nn.ELU(inplace=True),
            nn.Linear(feature_size, classes_num),
        )

        self.conv_block2 = nn.Sequential(
            BasicConv(self.num_ftrs, feature_size, kernel_size=1, stride=1, padding=0, relu=True),
            BasicConv(feature_size, self.num_ftrs, kernel_size=3, stride=1, padding=1, relu=True)
        )
        self.classifier2 = nn.Sequential(
            nn.BatchNorm1d(self.num_ftrs),
            nn.Linear(self.num_ftrs, feature_size),
            nn.BatchNorm1d(feature_size),
            nn.ELU(inplace=True),
            nn.Linear(feature_size, classes_num),
        )

        self.conv_block3 = nn.Sequential(
            BasicConv(2048, feature_size, kernel_size=1, stride=1, padding=0, relu=True),
            BasicConv(feature_size, self.num_ftrs, kernel_size=3, stride=1, padding=1, relu=True)
        )
        self.classifier3 = nn.Sequential(
            nn.BatchNorm1d(self.num_ftrs),
            nn.Linear(self.num_ftrs, feature_size),
            nn.BatchNorm1d(feature_size),
            nn.ELU(inplace=True),
            nn.Linear(feature_size, classes_num),
        )

    def forward(self, x):
        # print("inpput", x.shape)

        xf1, xf2, xf3, xf4 = self.features(x)
        # print("x1", xf1.shape)
        # print("x2", xf2.shape)
        # print("x3", xf3.shape)
        # print("x4", xf4.shape)

        xl1 = self.conv_block1(xf2)
        # print('xl1: ', xl1.shape)
        xl2 = self.conv_block2(xf3)
        # print('xl2: ', xl2.shape)
        xl3 = self.conv_block3(xf4)
        # print('xl3: ', xl3.shape)
        
        xl1 = self.max1(xl1)
        # print('xl1: ', xl1.shape)
        xl1 = xl1.view(xl1.size(0), -1)
        # print('xl1: ', xl1.shape)
        xc1 = self.classifier1(xl1)
        # print('xc1: ', xc1.shape)

        xl2 = self.max2(xl2)
        # print('xl2: ', xl2.shape)
        xl2 = xl2.view(xl2.size(0), -1)
        # print('xl2: ', xl2.shape)
        xc2 = self.classifier2(xl2)
        # print('xc2: ', xc2.shape)

        xl3 = self.max3(xl3)
        # print('xl3: ', xl3.shape)
        xl3 = xl3.view(xl3.size(0), -1)
        # print('xl3: ', xl3.shape)
        xc3 = self.classifier3(xl3)
        # print('xc3: ', xc3.shape)
          
        x_concat = torch.cat((xl1, xl2, xl3), -1)
        # print('x_concat: ', x_concat.shape)
        x_concat = self.classifier_concat(x_concat)
        # print('x_concat: ', x_concat.shape)
        # print("done foward")
        return xc1, xc2, xc3, x_concat    
    
class BasicConv(nn.Module):
    def __init__(self, in_planes, out_planes, kernel_size, stride=1, padding=0, dilation=1, groups=1, relu=True, bn=True, bias=False):
        super(BasicConv, self).__init__()
        self.out_channels = out_planes
        self.conv = nn.Conv2d(in_planes, out_planes, kernel_size=kernel_size,
                              stride=stride, padding=padding, dilation=dilation, groups=groups, bias=bias)
        self.bn = nn.BatchNorm2d(out_planes, eps=1e-5,
                                 momentum=0.01, affine=True) if bn else None
        self.relu = nn.ReLU() if relu else None

    def forward(self, x):
        x = self.conv(x)
        if self.bn is not None:
            x = self.bn(x)
        if self.relu is not None:
            x = self.relu(x)
        return x
