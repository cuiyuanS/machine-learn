import shutil
import time

import torch
from config import opt
import os


# 仪表
class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


# 准确率
def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


# 保存模型参数以及优化器参数
def save_checkpoint(state):
    prefix = './checkpoint/' + opt.model + '_'
    filename = time.strftime(prefix + '%m%d_%H-%M-%S.pth.tar')
    torch.save(state, filename)
    print("Get Better top1 : %s saving weights to %s" % (state["best_precision"], filename))  # 打印精确度