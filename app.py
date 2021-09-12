import json
from random import randint

from neuralNetwork import MLP

data = [
    {
        'inputs': [1, 0],
        'target': [1]
    },
    {
        'inputs': [0, 1],
        'target': [1]
    },
    {
        'inputs': [1, 1],
        'target': [0]
    },
    {
        'inputs': [0, 0],
        'target': [0]
    }
]


def save_data(mlp: MLP, path: str):
    file = open(path, 'w')
    data = mlp.serialise()
    file.write(data)
    file.close()


def load(path: str) -> MLP:
    file = open(path, 'r')
    data = file.read()
    json_data = json.loads(data)
    file.close()

    return MLP.deserialise(json_data)


brain = 'mlp.json'

mlp = MLP(2, [4, 2, 4], 1)

for i in range(100000):
    training_data = data[randint(0, len(data) - 1)]
    mlp.train(training_data['inputs'], training_data['target'])

print(mlp.predict(data[0]['inputs']))
print(mlp.predict(data[1]['inputs']))
print(mlp.predict(data[2]['inputs']))
print(mlp.predict(data[3]['inputs']))

save_data(mlp, brain)
