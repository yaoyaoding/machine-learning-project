# Coursework 3 : Many-agent Battle

## Goal
* Learn deep q network (Mnih, Volodymyr, et al. "Human-level control through deep reinforcement learning." Nature 518.7540 (2015): 529.)
* Implement and train your own AI system to manipulate a large population of soldiers

## Links
Online Judge: http://magent.apexlab.org/  
MAgent tutorial: https://github.com/geek-ai/MAgent/blob/master/doc/get_started.md

It is recommended that you read the tutorial of MAgent before reading the 
following part of this document.

## How to run your model on OJ

You should write your model in a single python file.

### Requirements

- python >= 3.5
- tensorflow >= 1.3
- mxnet >= 1.2.0
- pytorch >= 0.1.12

### Python Code

The model class you write must be named as `Net`. It should support two APIs `infer_action` and `load`.

Here is an exmaple of a random model.
```python
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
```

A more complicated deep q network in tensorflow is also attached.

### Data File
When you save your model in deep learning frameworks (e.g. tensorflow), 
these frameworks will use several files to store the computation graph definition
and weight matrices. You should zip them into an archieve file and upload it.

Note that `zip` is the only supported format.

### Uploading
You can upload your model after logging in

1. Name your new model: it is optional, default is [Unknown]
2. Paste your python code into the text area
3. Upload your data in zip format

## Others
1. Currently, the size of zip archive cannot be larger than 50MB
2. Large file will cost more time to upload, possibly you need to wait for several minutes (I will try to add a progress bar on the upload page, if I have time)
3. You can dowload video file from Demo page, and render it (see tutorial in MAgent repo for how to render them)

## Evaluation
* Deadline : 6.10 (15th week)
* Final evaluation: Swiss-system tournament

## Guide for This Courcework
This coursework is the most complicated one in CS420. Because you should 
learn the theory of reinforcement learning, the usage of one deep learning framework and the usage of MAgent/OJ.

Here are the recommended steps for you to get started

* Get familiar with RL/DQN:
  * Read course slides by Weinan
  * Read the paper of DQN
* Know how to implement RL algorithms in a deep learning framework:
  * This is a good tutorial: https://morvanzhou.github.io/tutorials/machine-learning/reinforcement-learning/
* Know how to use MAgent:
  * Read tutorial of MAgent
  * Read the DQN implementation in MAgent
  * Try the example in MAgent `python3 examples/train_battle.py`. 
    It will train a dqn which can work well for this coursework.
* Make your improvement to the model/algorithm.
* Contact TA when you need help
