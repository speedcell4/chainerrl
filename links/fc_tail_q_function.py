from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()
import chainer
from chainer import links as L

import q_function
from q_output import DiscreteQOutput


class FCTailQFunction(chainer.ChainList, q_function.QFunction):

    def __init__(self, head, head_output_size, n_actions):

        self.n_actions = n_actions

        layers = [
            head.copy(),
            L.Linear(head_output_size, n_actions, bias=0.1),
        ]

        super(FCTailQFunction, self).__init__(*layers)

    def __call__(self, state, test=False):
        h = self[0](state)
        return DiscreteQOutput(self[1](h))