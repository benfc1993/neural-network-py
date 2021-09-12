import json
from math import exp

from neuralNetwork import Matrix


def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


def dsigmoid(x: float) -> float:
    return x * (1 - x)


class MLP:
    def __init__(self, inputs: int, hidden_layers: list[int], outputs: int, learning_rate: float = 0.2):
        self.inputs = inputs
        self.hidden_layers_array = hidden_layers
        self.hidden_layers_count = len(hidden_layers)
        self.outputs = outputs
        self.learning_rate = learning_rate

        self.hidden_layers: list[Matrix or None] = [None] * self.hidden_layers_count
        self.layers_array: list[int] = [inputs] + hidden_layers + [outputs]
        self.layers: list[Matrix or None] = [None] * (len(self.layers_array) - 1)
        self.weights: list[Matrix] = []
        self.biases: list[Matrix] = []
        self.initialise_values()

        print(len(self.layers))
        print(len(self.weights))
        print(len(self.biases))

    def initialise_values(self):

        for i in range(len(self.layers_array)):
            if i < len(self.layers_array) - 1:
                self.weights.append(Matrix(self.layers_array[i + 1], self.layers_array[i]))
                self.weights[i].randomise()
            if i > 0:
                self.biases.append(Matrix(self.layers_array[i], 1))
                self.biases[-1].randomise()

    #
    # def initialise_values(self):
    #     self.weights.append(Matrix(self.hidden_layers_array[0], self.inputs))
    #     self.weights[0].randomise()
    #
    #     for i in range(self.hidden_layers_count):
    #         if i + 1 < self.hidden_layers_count:
    #             self.weights.append(Matrix(self.hidden_layers_array[i + 1], self.hidden_layers_array[i]))
    #             self.weights[i + 1].randomise()
    #
    #         self.biases.append(Matrix(self.hidden_layers_array[i], 1))
    #         self.biases[i].randomise()
    #
    #     self.weights.append(Matrix(self.outputs, self.hidden_layers_array[-1]))
    #     self.weights[-1].randomise()
    #
    #     self.biases.append(Matrix(self.outputs, 1))
    #     self.biases[-1].randomise()

    def train(self, input_array: list[float] or list[int], targets: list[float] or list[int]):
        c_guess: Matrix = Matrix.from_array(self.predict(input_array))
        c_inputs: Matrix = Matrix.from_array(input_array)
        c_targets: Matrix = Matrix.from_array(targets)

        # output_errors: Matrix = Matrix.subtract(targetsM, guessM)

        c_output_errors: Matrix = Matrix.s_subtract(c_targets, c_guess)

        # c_targets.print()
        # c_guess.print()
        # c_output_errors.print()
        errors_prev: Matrix = c_output_errors

        for i in range(len(self.layers) - 1, -1, -1):

            if i < len(self.layers) - 1:
                weight_t: Matrix = Matrix.s_transpose(self.weights[i + 1])
                errors_prev = Matrix.s_multiply(weight_t, errors_prev)

            gradient_prev = Matrix.s_funcmap(self.layers[i], dsigmoid)
            gradient_prev.element_wise_multiply(errors_prev)
            gradient_prev.scale(self.learning_rate)

            # gradient_prev = Matrix.map(self.layers[-1], dsigmoid)
            # gradient_prev.multiply(c_output_errors)
            # gradient_prev.scale(self.learningRate)

            next_layer_t = Matrix.s_transpose(self.layers[i - 1] if i > 0 else c_inputs)
            next_layer_deltas = Matrix.s_multiply(gradient_prev, next_layer_t)

            self.weights[i].add(next_layer_deltas)
            self.biases[i].add(gradient_prev)

    #
    # def train(self, input_array: list[float] or list[int], targets: list[float] or list[int]):
    #     c_guess: Matrix = Matrix.from_array(self.predict(input_array))
    #     c_inputs: Matrix = Matrix.from_array(input_array)
    #     c_targets: Matrix = Matrix.from_array(targets)
    #
    #     c_output_errors: Matrix = Matrix.s_subtract(c_targets, c_guess)
    #
    #     c_output_gradients = Matrix.s_funcmap(c_guess, dsigmoid)
    #
    #     c_output_gradients.element_wise_multiply(c_output_errors)
    #     c_output_gradients.scale(self.learning_rate)
    #
    #     c_hidden_t = Matrix.s_transpose(self.hidden_layers[-1])
    #     c_weight_ho_deltas = Matrix.s_multiply(c_output_gradients, c_hidden_t)
    #
    #     self.weights[-1].add(c_weight_ho_deltas)
    #     self.biases[-1].add(c_output_gradients)
    #
    #     hidden_errors_prev: Matrix = c_output_errors
    #     hidden_gradient_prev: Matrix
    #
    #     for i in range(len(self.hidden_layers) - 1, 0, -1):
    #         weight_t: Matrix = Matrix.s_transpose(self.weights[i + 1])
    #         hidden_errors_prev = Matrix.s_multiply(weight_t, hidden_errors_prev)
    #
    #         hidden_gradient_prev = Matrix.s_funcmap(self.hidden_layers[i], dsigmoid)
    #         hidden_gradient_prev.element_wise_multiply(hidden_errors_prev)
    #         hidden_gradient_prev.scale(self.learning_rate)
    #
    #         next_layer_t = Matrix.s_transpose(self.hidden_layers[i - 1] if i >= 1 else c_inputs)
    #         next_layer_deltas = Matrix.s_multiply(hidden_gradient_prev, next_layer_t)
    #
    #         self.weights[i].add(next_layer_deltas)
    #         self.biases[i].add(hidden_gradient_prev)

    def predict(self, inputs_array: list[float]) -> list[float]:
        c_inputs = Matrix.from_array(inputs_array)
        self.layers[0] = c_inputs

        for i in range(0, len(self.layers)):
            self.layers[i] = Matrix.s_multiply(self.weights[i], c_inputs if i == 0 else self.layers[i - 1])
            self.layers[i].add(self.biases[i])
            self.layers[i].funcmap(sigmoid)

        return Matrix.to_flat_array(self.layers[-1])

    # def predict(self, inputs_array: list[float]) -> list[float]:
    #     c_inputs = Matrix.from_array(inputs_array)
    #
    #     for i in range(self.hidden_layers_count):
    #         self.hidden_layers[i] = Matrix.s_multiply(self.weights[i],
    #                                                   c_inputs if i == 0 else self.hidden_layers[i - 1])
    #
    #         self.hidden_layers[i].add(self.biases[i])
    #         self.hidden_layers[i].funcmap(sigmoid)
    #
    #     outputs = Matrix.s_multiply(self.weights[-1], self.hidden_layers[-1])
    #     outputs.add(self.biases[-1])
    #     outputs.funcmap(sigmoid)
    #
    #     return Matrix.to_flat_array(outputs)

    def serialise(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def deserialise(cls, data):
        mlp = MLP(data['inputs'], data['hidden_layers_array'], data['outputs'])
        mlp.layers = list(map(Matrix.deserialise, data['layers']))
        mlp.weights = list(map(Matrix.deserialise, data['weights']))
        mlp.biases = list(map(Matrix.deserialise, data['biases']))
        mlp.learning_rate = data['learning_rate']
        return mlp
