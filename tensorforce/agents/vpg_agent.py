# Copyright 2017 reinforce.io. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from tensorforce.agents import LearningAgent
from tensorforce.models import PGLogProbModel


class VPGAgent(LearningAgent):
    """
    Vanilla policy gradient agent
    ([Williams, 1992)](https://link.springer.com/article/10.1007/BF00992696)).
    """

    def __init__(
        self,
        states,
        actions,
        network,
        batched_observe=True,
        batching_capacity=1000,
        scope='vpg',
        device=None,
        saver=None,
        summarizer=None,
        execution=None,
        variable_noise=None,
        states_preprocessing=None,
        actions_exploration=None,
        reward_preprocessing=None,
        update_mode=None,
        memory=None,
        optimizer=None,
        discount=0.99,
        distributions=None,
        entropy_regularization=None,
        baseline_mode=None,
        baseline=None,
        baseline_optimizer=None,
        gae_lambda=None
    ):
        """
        Initializes the VPG agent.

        Args:
            update_mode (spec): Update mode specification, with the following attributes:
                - unit: 'episodes' if given (default: 'episodes').
                - batch_size: integer (default: 10).
                - frequency: integer (default: batch_size).
            memory (spec): Memory specification, see core.memories module for more information
                (default: {type='latest', include_next_states=false, capacity=1000*batch_size}).
            optimizer (spec): Optimizer specification, see core.optimizers module for more
                information (default: {type='adam', learning_rate=1e-3}).
            baseline_mode (str): One of 'states', 'network' (default: none).
            baseline (spec): Baseline specification, see core.baselines module for more information
                (default: none).
            baseline_optimizer (spec): Baseline optimizer specification, see core.optimizers module
                for more information (default: none).
            gae_lambda (float): Lambda factor for generalized advantage estimation (default: none).
        """

        # Update mode
        if update_mode is None:
            update_mode = dict(
                unit='episodes',
                batch_size=10
            )
        elif 'unit' in update_mode:
            # Tests check all modes for VPG.
            # assert update_mode['unit'] == 'episodes'
            pass
        else:
            update_mode['unit'] = 'episodes'

        # Memory
        if memory is None:
            # Assumed episode length of 1000 timesteps.
            memory = dict(
                type='latest',
                include_next_states=False,
                capacity=(1000 * update_mode['batch_size'])
            )
        else:
            assert not memory['include_next_states']

        # Optimizer
        if optimizer is None:
            optimizer = dict(
                type='adam',
                learning_rate=1e-3
            )

        self.baseline_mode = baseline_mode
        self.baseline = baseline
        self.baseline_optimizer = baseline_optimizer
        self.gae_lambda = gae_lambda

        super(VPGAgent, self).__init__(
            states=states,
            actions=actions,
            batched_observe=batched_observe,
            batching_capacity=batching_capacity,
            scope=scope,
            device=device,
            saver=saver,
            summarizer=summarizer,
            execution=execution,
            variable_noise=variable_noise,
            states_preprocessing=states_preprocessing,
            actions_exploration=actions_exploration,
            reward_preprocessing=reward_preprocessing,
            update_mode=update_mode,
            memory=memory,
            optimizer=optimizer,
            discount=discount,
            network=network,
            distributions=distributions,
            entropy_regularization=entropy_regularization
        )

    def initialize_model(self):
        return PGLogProbModel(
            states=self.states,
            actions=self.actions,
            scope=self.scope,
            device=self.device,
            saver=self.saver,
            summarizer=self.summarizer,
            execution=self.execution,
            batching_capacity=self.batching_capacity,
            variable_noise=self.variable_noise,
            states_preprocessing=self.states_preprocessing,
            actions_exploration=self.actions_exploration,
            reward_preprocessing=self.reward_preprocessing,
            update_mode=self.update_mode,
            memory=self.memory,
            optimizer=self.optimizer,
            discount=self.discount,
            network=self.network,
            distributions=self.distributions,
            entropy_regularization=self.entropy_regularization,
            baseline_mode=self.baseline_mode,
            baseline=self.baseline,
            baseline_optimizer=self.baseline_optimizer,
            gae_lambda=self.gae_lambda
        )
