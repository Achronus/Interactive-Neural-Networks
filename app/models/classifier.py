import numpy as np


class Classify:
    def __init__(self, weights: list[float]) -> None:
        self.weights = np.asarray(weights)

    def calc(self, data: np.array) -> list[int]:
        preds = []
        for row in data:
            output_1 = row[0] * self.weights[0] + row[1] * self.weights[2]
            output_2 = row[0] * self.weights[1] + row[1] * self.weights[3]
            preds.append(0 if (output_1 > output_2) else 1)
        return preds


"""
Weights: 
- Determines the strength of the connection between neurons (nodes). 
  For example, the steepness of a slope.

Biases:
- Adjusts the activation threshold of a neuron, shifting it left or right.

Node calculations (without bias):
- output_1 = input_1 x weight_1_1 + input_2 x weight_2_1
- output_2 = input_1 x weight_1_2 + input_2 x weight_2_2
"""
