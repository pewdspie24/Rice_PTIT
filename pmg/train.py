from __future__ import print_function
import os

import torch
import torch.optim as optim
import tqdm
from utils import *


def train(
    nb_epoch,
    batch_size,
    store_name,
    resume=False,
    start_epoch=0,
    model_path=None,
    device="cpu",
    card_gpu=None,
):
    # setup output
    exp_dir = store_name
    try:
        os.stat(exp_dir)
    except:
        os.makedirs(exp_dir)

    use_cuda = torch.cuda.is_available()

    # Data
    print("==> Preparing data..")
    transform_train = transforms.Compose(
        [
            transforms.Resize((550, 550)),
            transforms.RandomCrop(448, padding=8),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )
    trainset = torchvision.datasets.ImageFolder(
        root="ngoc/data/train", transform=transform_train
    )
    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=batch_size, shuffle=True, num_workers=2
    )
    print("-------> Done data")
    # Model
    if resume:
        print("load_ckpt")
        net = torch.load(model_path)
    else:
        print("init ckpt")
        net = load_model(model_name="resnet50_pmg", pretrain=True, require_grad=True)
    netp = torch.nn.DataParallel(net, device_ids=card_gpu)  # ch

    # GPU
    device = torch.device(device=device)
    net.to(device)
    # cudnn.benchmark = True

    CELoss = nn.CrossEntropyLoss()
    optimizer = optim.SGD(
        [
            {"params": net.classifier_concat.parameters(), "lr": 0.002},
            {"params": net.conv_block1.parameters(), "lr": 0.002},
            {"params": net.classifier1.parameters(), "lr": 0.002},
            {"params": net.conv_block2.parameters(), "lr": 0.002},
            {"params": net.classifier2.parameters(), "lr": 0.002},
            {"params": net.conv_block3.parameters(), "lr": 0.002},
            {"params": net.classifier3.parameters(), "lr": 0.002},
            {"params": net.features.parameters(), "lr": 0.0002},
        ],
        momentum=0.9,
        weight_decay=5e-4,
    )

    max_val_acc = 0
    lr = [0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.0002]
    for epoch in range(start_epoch, nb_epoch):
        print("\nEpoch: %d" % epoch)
        net.train()
        train_loss = 0
        train_loss1 = 0
        train_loss2 = 0
        train_loss3 = 0
        train_loss4 = 0
        correct = 0
        correct_com = 0
        total = 0
        idx = 0
        for (inputs, targets) in tqdm.tqdm(trainloader):
            if inputs.shape[0] < batch_size:
                continue
            if use_cuda:
                inputs, targets = inputs.to(device), targets.to(device)
            inputs, targets = Variable(inputs), Variable(targets)

            # update learning rate
            for nlr in range(len(optimizer.param_groups)):
                optimizer.param_groups[nlr]["lr"] = cosine_anneal_schedule(
                    epoch, nb_epoch, lr[nlr]
                )

            # Step 1
            optimizer.zero_grad()
            inputs1 = jigsaw_generator(inputs, 8)
            output_1, _, _, _ = netp(inputs1)
            loss1 = CELoss(output_1, targets) * 1
            loss1.backward()
            optimizer.step()

            # Step 2
            optimizer.zero_grad()
            inputs2 = jigsaw_generator(inputs, 4)
            _, output_2, _, _ = netp(inputs2)
            loss2 = CELoss(output_2, targets) * 1
            loss2.backward()
            optimizer.step()

            # Step 3
            optimizer.zero_grad()
            inputs3 = jigsaw_generator(inputs, 2)
            _, _, output_3, _ = netp(inputs3)
            loss3 = CELoss(output_3, targets) * 1
            loss3.backward()
            optimizer.step()

            # Step 4
            optimizer.zero_grad()
            _, _, _, output_concat = netp(inputs)
            concat_loss = CELoss(output_concat, targets) * 2
            concat_loss.backward()
            optimizer.step()

            outputs_com = output_1 + output_2 + output_3 + output_concat

            #  training log

            _, predicted = torch.max(output_concat.data, 1)
            _, predicted_com = torch.max(outputs_com.data, 1)
            total += targets.size(0)

            correct += predicted.eq(targets.data).cpu().sum()
            correct_com += predicted_com.eq(targets.data).cpu().sum()

            train_loss += (
                loss1.item() + loss2.item() + loss3.item() + concat_loss.item()
            )
            train_loss1 += loss1.item()
            train_loss2 += loss2.item()
            train_loss3 += loss3.item()
            train_loss4 += concat_loss.item()

            idx += 1
            
        train_acc = 100.0 * float(correct) / total
        train_acc_com = 100.0 * float(correct_com) / total
        train_loss = train_loss / (idx + 1)
        info_train = (
            "Epoch %d | train_acc = %.5f | train_acc_com = %.5f | train_loss = %.5f | Loss1: %.3f | Loss2: %.5f | Loss3: %.5f | Loss_concat: %.5f |\n"
            % (
                epoch,
                train_acc,
                train_acc_com,
                train_loss,
                train_loss1 / (idx + 1),
                train_loss2 / (idx + 1),
                train_loss3 / (idx + 1),
                train_loss4 / (idx + 1),
            )
        )
        print(info_train)

        with open("ngoc/pmg/log_resnet50/results_train_resnet.txt", "a") as file:
            file.write(info_train)

        val_acc, val_acc_com, val_loss = test(net, CELoss, 2, device=device)

        # net.cpu()
        torch.save(net, "./" + store_name + "/last_cub_resnet.pth")
        if val_acc_com > max_val_acc:
            max_val_acc = val_acc_com
            torch.save(net, "./" + store_name + "/model_cub_resnet.pth")
            # net.to(device)

        info_test = (
            "Epoch %d | test_acc = %.5f, test_acc_combined | %.5f, test_loss | %.6f\n"
            % (epoch, val_acc, val_acc_com, val_loss)
        )
        print(info_test)
        with open("ngoc/pmg/log_resnet50/results_test_resnet.txt", "a") as file:
            file.write(info_test)


if __name__ == "__main__":
    train(
        nb_epoch=200,  # number of epoch
        batch_size=16,  # batch size
        store_name="ngoc/pmg/ckpt_resnet50",  # folder for output
        resume=False,  # resume training from checkpoint
        start_epoch=0,  # the start epoch number when you resume the training
        model_path="",
        device= "cuda",
        card_gpu= [0]
    )  # [0,1]   # the saved model where you want to resume the training
