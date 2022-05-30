from builtins import breakpoint
from multiprocessing import reduction
import sys

sys.path.append("../")
import os
import torch
from torch import nn
import json
from torch.nn import functional as F
from tqdm import tqdm
from datetime import datetime
from data import get_data
from models import get_encoder, get_decoder
from torch.nn.utils import parameters_to_vector, vector_to_parameters
from copy import deepcopy
import torchvision
import torch.nn.functional as F
import yaml
from math import sqrt, pi, log
import numpy as np
import cv2
import matplotlib.pyplot as plt
from utils import load_laplace
from helpers import BaseImputation

sys.path.append("../../Laplace")
from laplace.laplace import Laplace


class LAEPosthocImputation(BaseImputation):
    def __init__(self, config, device):
        super().__init__(config, device)

        self.model = "lae_posthoc"
        self.n_samples = 10

        path = f"{config['path']}"
        self.la = load_laplace(f"../../weights/{path}/ae.pkl")

    def forward_pass(self, xi):

        with torch.no_grad():
            xi = xi.view(xi.size(0), -1)
            x_rec = self.la._nn_predictive_samples(xi, self.n_samples)
            x_rec = x_rec.reshape(self.n_samples, 1, 28, 28)

        return x_rec, x_rec.mean(0), x_rec.var(0)


class FromNoise(LAEPosthocImputation):
    def __init__(self, config, device):
        super().__init__(config, device)
        self.name = "from_noise"

    def mask(self, x):
        x = torch.randn_like(x)
        x = (x - x.min()) / (x.max() - x.min())
        return x

    def insert_original_and_forward_again(self, x_rec, x):

        x_rec = x_rec.view(-1, 1, 28, 28)

        for i in range(x_rec.shape[0]):
            x_rec_i, _, _ = self.forward_pass(x_rec[i : i + 1])
            x_rec[i] = x_rec_i.mean(dim=0)

        return x_rec.view(-1, 1, 28, 28)


class FromHalf(LAEPosthocImputation):
    def __init__(self, config, device):
        super().__init__(config, device)
        self.name = "from_half"

    def mask(self, x):
        x_mask = torch.randn_like(x)
        x_mask = (x_mask - x_mask.min()) / (x_mask.max() - x_mask.min())
        x[:, :, : x.shape[2] // 2, :] = x_mask[:, :, : x.shape[2] // 2, :]
        return x

    def insert_original_and_forward_again(self, x_rec, x):

        x_rec = x_rec.view(-1, 1, 28, 28)
        x_rec[:, :, x.shape[2] // 2 :, :] = x[:, :, x.shape[2] // 2 :, :].repeat(
            x_rec.shape[0], 1, 1, 1
        )

        for i in range(x_rec.shape[0]):
            x_rec_i, _, _ = self.forward_pass(x_rec[i : i + 1])
            x_rec[i] = x_rec_i.mean(dim=0)

        return x_rec.view(-1, 1, 28, 28)


class FromFull(LAEPosthocImputation):
    def __init__(self, config, device):
        super().__init__(config, device)
        self.name = "from_full"

    def mask(self, x):
        return x

    def insert_original_and_forward_again(self, x_rec, x):

        x_rec = x_rec.view(-1, 1, 28, 28)

        for i in range(x_rec.shape[0]):
            x_rec_i, _, _ = self.forward_pass(x_rec[i : i + 1])
            x_rec[i] = x_rec_i.mean(dim=0)

        return x


def main(config):

    # initialize_model
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    _, val_loader = get_data(config["dataset"], 1, config["missing_data_imputation"])

    FromNoise(config, device).compute(val_loader)
    FromHalf(config, device).compute(val_loader)
    FromFull(config, device).compute(val_loader)


if __name__ == "__main__":

    # celeba
    # path = "celeba/lae_elbo/[backend_layer]_[approximation_mix]_[no_conv_False]_[train_samples_1]_"

    # mnist
    path = "mnist/lae_post_hoc"

    config = {
        "dataset": "mnist",  # "mnist", #"celeba",
        "path": path,
        "test_samples": 100,
        "missing_data_imputation": False,
    }

    main(config)
