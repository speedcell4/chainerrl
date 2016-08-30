from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import dict
from future import standard_library
standard_library.install_aliases()

from chainer import links as L


def copy_param(target_link, source_link):
    """Copy parameters of a link to another link.
    """
    target_params = dict(target_link.namedparams())
    for param_name, param in source_link.namedparams():
        target_params[param_name].data[:] = param.data


def soft_copy_param(target_link, source_link, tau):
    """Soft-copy parameters of a link to another link.
    """
    target_params = dict(target_link.namedparams())
    for param_name, param in source_link.namedparams():
        target_params[param_name].data[:] *= (1 - tau)
        target_params[param_name].data[:] += tau * param.data
    if isinstance(target_link, L.BatchNormalization):
        target_link.avg_mean[:] *= (1 - tau)
        target_link.avg_mean[:] += tau * source_link.avg_mean
        target_link.avg_var[:] *= (1 - tau)
        target_link.avg_var[:] += tau * source_link.avg_var


def copy_grad(target_link, source_link):
    """Copy gradients of a link to another link.
    """
    target_params = dict(target_link.namedparams())
    for param_name, param in source_link.namedparams():
        target_params[param_name].grad[:] = param.grad
