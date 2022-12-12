import matplotlib.pyplot as plt

loss = {}
loss['test_loss'] = []
loss['train_loss'] = []
accu = {}

accu["test_last"] = []
accu["train_last"] = []
accu["test_combined"] = []
accu["train_combined"] = []
epoc = []
with open ("results_test_nobk.txt", "r+") as f:
    for line in f.readlines():
        epoch, test_last, test_combined, test_loss = line.strip().split(" ")
        epoc.append(int(epoch))
        loss["test_loss"].append(float(test_loss))
        accu["test_last"].append(float(test_last))
        accu["test_combined"].append(float(test_combined))
        
with open ("results_train_nobk.txt", "r+") as f:
    for line in f.readlines():
        epoch, train_last, train_combined, train_loss, Loss1, Loss2, Loss3, Loss_concat = line.strip().split(" ")
        loss["train_loss"].append(float(train_loss))
        accu["train_last"].append(float(train_last))
        accu["train_combined"].append(float(train_combined))
        
fig = plt.figure()

# ax0 = fig.add_subplot(121, title="loss")
# ax0.plot(epoc, loss['train_loss'], 'b', label='train_loss')
# ax0.plot(epoc, loss['test_loss'], 'g', label='test_loss')
# plt.axvline(x=83, color='silver')
# plt.legend()
# plt.show()

ax1 = fig.add_subplot(121, title="accuracy")
ax1.plot(epoc, accu["test_last"], 'b', label='test_last')
ax1.plot(epoc, accu["train_last"], 'g', label='train_last')
ax1.plot(epoc, accu["test_combined"], 'r', label='test_combined')
ax1.plot(epoc, accu["train_combined"], 'c', label='train_combined')
plt.axvline(x=83, color='silver')
plt.legend()
plt.show()

# 56