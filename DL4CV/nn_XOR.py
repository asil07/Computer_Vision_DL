from pyimagesearch.nn.neuralnetwork import NeuralNetwork
import numpy as np

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

nn = NeuralNetwork([2,25, 1], alpha=0.5)
nn.fit(X, y, epochs=2000)

for (x, target) in zip(X, y):
    pred = nn.predict(x)[0][0]
    step = 1 if pred > 0.5 else 0
    print(f"[info] data={x}, ground-truth={target[0]}, pred={pred:.4f}, step={step}")
