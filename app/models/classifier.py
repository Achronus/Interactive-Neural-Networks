import numpy as np


class SimpleNeuralNetwork:
    """A simple Artificial Neural Network (ANN) containing two input and output nodes."""
    def __init__(self, weights: list[float]) -> None:
        self.weights = np.asarray(weights)

    def calc(self, data: np.array) -> list[int]:
        preds = []
        for row in data:
            output_1 = row[0] * self.weights[0] + row[1] * self.weights[2]
            output_2 = row[0] * self.weights[1] + row[1] * self.weights[3]
            preds.append(0 if (output_1 > output_2) else 1)
        return preds
