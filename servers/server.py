from godot_rl.wrappers.stable_baselines_wrapper import StableBaselinesGodotEnv
from typing import Any, Dict, List, Optional, Tuple
import pathlib
import argparse
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env.vec_monitor import VecMonitor
from godot_rl.core.utils import can_import, lod_to_dol
import os
class ServerEnv(StableBaselinesGodotEnv):
    def step(self, action: np.ndarray) -> Tuple[Dict[str, np.ndarray], np.ndarray, np.ndarray, List[Dict[str, Any]]]:
        # Initialize lists for collecting results
        all_obs = []
        all_rewards = []
        all_term = []
        all_trunc = []
        all_info = []
        # Get the number of environments
        num_envs = self.envs[0].num_envs

        # Send actions to each environment
        for i in range(self.n_parallel):
            self.envs[i].step_send(action[i * num_envs : (i + 1) * num_envs])

        # Receive results from each environment
        for i in range(self.n_parallel):
            obs, reward, term, trunc, info = self.envs[i].step_recv()
            all_obs.extend(obs)
            all_rewards.extend(reward)
            all_term.extend(term)
            all_trunc.extend(trunc)
            all_info.extend(info)

        # Convert list of dictionaries to dictionary of lists
        obs = lod_to_dol(all_obs)
        obs=self.process_obs(obs)
        # Return results
        return (
            {k: np.array(v) for k, v in obs.items()},
            np.array(all_rewards, dtype=np.float32),
            np.array(all_term),
            all_info,
        )

parser = argparse.ArgumentParser(allow_abbrev=False)
parser.add_argument(
    "--opponent_path",
    default="model_0307-2.zip",
    type=str,
    help="预训练ai文件地址，如果给出，将会使用agent控制对方ai",
)
args, extras = parser.parse_known_args()




env = ServerEnv(
    seed=0
)
path_zip = pathlib.Path(args.opponent_path)
print("Loading model: " + os.path.abspath(path_zip))
model = PPO.load(path_zip, env=env)

env = VecMonitor(env)
obs = env.reset()
while True:
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)