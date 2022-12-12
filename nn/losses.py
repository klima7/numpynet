from abc import ABC, abstractmethod

import numpy as np

from .exceptions import InvalidParameterException


class Loss(ABC):

    def __repr__(self):
        return self.__class__.__name__

    @abstractmethod
    def call(self, prediction, target):
        pass

    @abstractmethod
    def deriv(self, prediction, target):
        pass


class MseLoss(Loss):

    def call(self, prediction, target):
        return np.sum(np.power(target - prediction, 2))

    def deriv(self, prediction, target):
        return target - prediction


class CceLoss(Loss):

    def call(self, prediction, target):
        logs = np.log(prediction, where=prediction > 0)
        return - logs @ target

    def deriv(self, prediction, target):
        return np.divide(target, prediction, out=np.zeros_like(prediction), where=prediction != 0)


class SoftmaxCceLoss(Loss):

    def call(self, prediction, target):
        prediction = self.__softmax(prediction)
        logs = np.log(prediction, where=prediction > 0)
        return - logs @ target

    def deriv(self, prediction, target):
        prediction = self.__softmax(prediction)
        one_pos = self.__get_one_position(target)
        delta = -prediction
        delta[one_pos] = 1 - prediction[one_pos]
        return delta

    @staticmethod
    def __softmax(x):
        x = x - np.max(x)
        e = np.exp(x)
        s = np.sum(e)
        return e / s if s != 0 else np.zeros_like(e)

    @staticmethod
    def __get_one_position(target):
        return np.where(target == 1)[0][0]


def get_loss(loss):
    if isinstance(loss, str):
        return get_loss_from_name(loss)
    elif isinstance(loss, Loss):
        return loss
    else:
        raise InvalidParameterException(f'Invalid loss: {loss}')


def get_loss_from_name(name):
    losses = {
        'mse': MseLoss,
        'cce': CceLoss,
        'softmax_cce': SoftmaxCceLoss,
    }

    if name not in losses.keys():
        raise InvalidParameterException(f'Unknown loss name: {name}')

    return losses[name]()
