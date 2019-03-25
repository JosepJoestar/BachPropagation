import torch
from torch import nn
from torch.autograd import Variable
from torch.utils.data import DataLoader

from dataset.MusicDataset import MusicDataset
from model.GANModel import GANModel
from model.GANGenerator import GANGenerator
from utils.constants import BATCH_SIZE
from utils.typings import Optimizer, Criterion, NNet


def train_generator(optimizer: Optimizer, criterion: Criterion, discriminator: NNet, fake_data):
    # Reset gradients
    optimizer.zero_grad()

    # Forwards pass to get logits
    prediction = discriminator(fake_data)

    # Calculate gradients w.r.t parameters and backpropagate
    loss = criterion(prediction, torch.Variable(torch.ones(fake_data.size(0), 1)))
    loss.backward()

    # Update parameters
    optimizer.step()
    return loss


def train_discriminator(optimizer: Optimizer, criterion: Criterion, discriminator: NNet, real_data, fake_data):
    def train_data(data, fake: bool):
        # Forwards pass to get logits
        prediction = discriminator(data)

        # Calculate gradients w.r.t parameters and backpropagate
        n = real_data.size(0)
        target = torch.Variable(torch.zeros(n)) if fake else torch.Variable(torch.ones(n))
        loss = criterion(prediction, target)
        loss.backward()

        return loss

    # Reset gradients
    optimizer.zero_grad()

    # Train on real data
    loss_real = train_data(real_data, fake=False)

    # Train on fake data
    loss_fake = train_data(fake_data, fake=True)

    # Update parameters
    optimizer.step()
    return loss_real + loss_fake


def train_epoch(model: GANModel, criterion: Criterion, loader: DataLoader) -> float:
    model.train_mode()
    for batch in loader:
        n = batch.size(0)

        # Train Discriminator
        real_data = Variable(batch)
        noise_data = GANGenerator.noise(n)
        fake_data = model.generator(noise_data).detach()

        d_loss = train_discriminator(optimizer=model.d_optimizer,
                                     criterion=criterion,
                                     discriminator=model.discriminator,
                                     real_data=real_data,
                                     fake_data=fake_data)

        # Train Generator
        noise_data = GANGenerator.noise(n)
        fake_data = model.generator(noise_data)

        g_loss = train_generator(optimizer=model.g_optimizer,
                                 criterion=criterion,
                                 discriminator=model.discriminator,
                                 fake_data=fake_data)

        return d_loss + g_loss


def test_epoch(model: GANModel, loader: DataLoader) -> float:
    model.test_mode()
    for _ in loader:
        pass
    return 42.0


def train(model: GANModel, epochs: int, train_loader: DataLoader, test_loader: DataLoader):
    criterion = nn.BCELoss()

    for epoch in range(epochs):
        loss = train_epoch(model=model, criterion=criterion, loader=train_loader)
        accuracy = test_epoch(model=model, loader=test_loader)
        print(f'Epoch {epoch}: Training loss = {loss}, Test accuracy = {accuracy}')


if __name__ == '__main__':
    def main():
        model = GANModel()
        model.initialize_generator(100, torch.optim.Adam)
        model.initialize_discriminator(100, torch.optim.Adam)

        train_songs = MusicDataset()
        test_songs = MusicDataset()

        train(model=model,
              epochs=100,
              train_loader=train_songs.get_dataloader(BATCH_SIZE),
              test_loader=test_songs.get_dataloader(BATCH_SIZE))

    main()
