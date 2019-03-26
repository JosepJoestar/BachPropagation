from model.GANDiscriminator import GANDiscriminator
from model.GANGenerator import GANGenerator
from utils.typings import NNet, Optimizer


class GANModel:
    def __init__(self):
        self.generator: NNet = None
        self.g_optimizer: Optimizer = None

        self.discriminator: NNet = None
        self.d_optimizer: NNet = None

    def initialize_generator(self, hid_dim: int, optimizer: Optimizer):
        self.generator = GANGenerator(layers=2, hid_dim=hid_dim)
        self.g_optimizer = optimizer(self.generator.parameters())

    def initialize_discriminator(self, hid_dim: int, optimizer: Optimizer):
        self.discriminator = GANDiscriminator(layers=2, hid_dim=hid_dim)
        self.d_optimizer = optimizer(self.discriminator.parameters())

    def train_mode(self):
        self.generator.train()
        self.discriminator.train()

    def test_mode(self):
        self.generator.eval()
        self.discriminator.eval()
