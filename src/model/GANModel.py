import logging

import torch
from torch.nn import functional as F

from model.GANDiscriminator import GANDiscriminator
from model.GANGenerator import GANGenerator
from utils.typings import NNet, Optimizer, Criterion


class GANModel:
    def __init__(self):
        logging.info('Creating GAN model...')

        self.generator: NNet = GANGenerator()
        self.g_optimizer: Optimizer = torch.optim.Adam(self.generator.parameters())
        self.g_criterion: Criterion = GANModel._generator_criterion

        self.discriminator: NNet = GANDiscriminator()
        self.d_optimizer: Optimizer = torch.optim.Adam(self.discriminator.parameters())
        self.d_criterion: Criterion = GANModel._discriminator_criterion

        # with SummaryWriter(log_dir=f'{PROJECT_PATH}/res/log', comment='Generator') as w:
        #     h = self.generator(Variable(torch.zeros(BATCH_SIZE, 42, MAX_POLYPHONY), requires_grad=True))
        #     w.add_graph(self.generator, h)

        # with SummaryWriter(log_dir=f'{PROJECT_PATH}/res/log', comment='Discriminator') as w:
        #     h = self.discriminator(Variable(torch.zeros(BATCH_SIZE, 42, MAX_POLYPHONY), requires_grad=True))
        #     w.add_graph(self.discriminator, h)

    # PyTorch working modes

    def train_mode(self):
        self.generator.train()
        self.discriminator.train()

    def test_mode(self):
        self.generator.eval()
        self.discriminator.eval()

    # Loss functions

    @staticmethod
    def _generator_criterion(prediction, ones):
        return torch.mean(torch.log(ones - prediction))

    @staticmethod
    def _discriminator_criterion(y, y_hat):
        return F.binary_cross_entropy(y, y_hat)
