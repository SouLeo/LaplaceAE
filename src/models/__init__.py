from models.mnist import Encoder_conv, Encoder_mnist, Decoder_conv, Decoder_mnist
from models.mnist_stochman import (
    Encoder_stochman_conv,
    Encoder_stochman_mnist,
    Decoder_stochman_conv,
    Decoder_stochman_mnist,
)
from models.svhn_stochman import Encoder_stochman_svhn_conv, Decoder_stochman_svhn_conv
from models.svhn import Encoder_svhn_conv, Decoder_svhn_conv
from models.cifar10_stochman import (
    Encoder_cifar10_stochman_conv,
    Decoder_cifar10_stochman_conv,
)
from models.cifar10 import Encoder_cifar10_conv, Decoder_cifar10_conv
from models.fashionmnist import (
    Encoder_fashionmnist,
    Encoder_fashionmnist_conv,
    Decoder_fashionmnist,
    Decoder_fashionmnist_conv,
)
from models.fashionmnist_stochman import (
    Encoder_stochman_fashionmnist,
    Encoder_stochman_fashionmnist_conv,
    Decoder_stochman_fashionmnist,
    Decoder_stochman_fashionmnist_conv,
)

encoders = {
    "mnist": Encoder_mnist,
    "mnist_conv": Encoder_conv,
    "fashionmnist": Encoder_fashionmnist,
    "fashionmnist_conv": Encoder_fashionmnist_conv,
    "cifar10_conv": Encoder_cifar10_conv,
    "svhn_conv": Encoder_svhn_conv,
}

stochman_encoders = {
    "mnist": Encoder_stochman_mnist,
    "mnist_conv": Encoder_stochman_conv,
    "fashionmnist": Encoder_stochman_fashionmnist,
    "fashionmnist_conv": Encoder_stochman_fashionmnist_conv,
    "cifar10_conv": Encoder_cifar10_stochman_conv,
    "svhn_conv": Encoder_stochman_svhn_conv,
}

decoders = {
    "mnist": Decoder_mnist,
    "mnist_conv": Decoder_conv,
    "fashionmnist": Decoder_fashionmnist,
    "fashionmnist_conv": Decoder_fashionmnist_conv,
    "cifar10_conv": Decoder_cifar10_conv,
    "svhn_conv": Decoder_svhn_conv,
}

stochman_decoders = {
    "mnist": Decoder_stochman_mnist,
    "mnist_conv": Decoder_stochman_conv,
    "fashionmnist": Decoder_stochman_fashionmnist,
    "fashionmnist_conv": Decoder_stochman_fashionmnist_conv,
    "cifar10_conv": Decoder_cifar10_stochman_conv,
    "svhn_conv": Decoder_stochman_svhn_conv,
}


def get_encoder(config, latent_size=2, dropout=0):

    name = config["dataset"]
    if not config["no_conv"]:
        name += "_conv"

    if "backend" in config and config["backend"] == "layer":
        encoder = stochman_encoders[name](latent_size, dropout)
    else:
        encoder = encoders[name](latent_size, dropout)

    return encoder


def get_decoder(config, latent_size=2, dropout=0):

    name = config["dataset"]
    if not config["no_conv"]:
        name += "_conv"

    if "backend" in config and config["backend"] == "layer":
        decoder = stochman_decoders[name](latent_size, dropout)
    else:
        decoder = decoders[name](latent_size, dropout)

    return decoder
