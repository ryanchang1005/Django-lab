import random

MAX_NODE = 100
NODES = [i for i in range(MAX_NODE)]


def node_generator():
    return random.choice(NODES)


def copy_and_random_nodes():
    ret = NODES.copy()
    random.shuffle(ret)
    return ret
