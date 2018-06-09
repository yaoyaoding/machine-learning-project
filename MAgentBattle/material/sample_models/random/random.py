"""
Random example to show the API format
"""

import os           # NECESSARY !
import numpy as np  # NECESSARY !

class Net:
    def __init__(self, env, handle):
        """Initialize object
        
        Parameters
        ----------
        env: Environment
        handle: GroupHandle
            These two parameters are used to get the game settings from environment.
            They are read-only so you cannot use them to modify the game engine (cheating).
        """
        self.num_actions = env.get_action_space(handle)[0]

    def infer_action(self, raw_obs, ids):
        """Infer action for a group of agents
        
        Parameters
        ----------
        raw_obs: tuple
            raw_obs is a tuple of (view, feature)
            view is a numpy array, its shape is n * view_width * view_height * n_channel
                                   it contains the spatial local observation for all the agents
            feature is a numpy array, its shape is n * feature_size
                                   it contains the non-spatial feature for all the agents
        ids: numpy array of int32
            the unique id of every agent
            
        Returns
        -------
        actions: numpy array of int32
            the action for every agent to execute in the next step
        """
        n = len(ids)
        act = np.random.randint(self.num_actions, size=(n,))
        return act.astype(np.int32)

    def load(self, dir_path):
        """Load model. This function will be called after initializing your model.
        
        Parameters
        ----------
        dir_path: str
            the root of your data file
            e.g.: if there is a `hello.txt` in your zip file, 
                  then you can use open(dir_path + "/hello.txt") to open it
        """
        pass

