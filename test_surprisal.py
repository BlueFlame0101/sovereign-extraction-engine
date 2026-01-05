"""
Surprisal Computation Benchmark - Gradient-Based Learning Signal Test.

This module validates tensor computation throughput by executing a forward-backward
pass through a simulated agent weight matrix. Measures gradient norm as a proxy
for learning signal magnitude in In-Context Weight Learning (IWL) architectures.

Metrics:
    - Gradient Norm (S_t): Magnitude of parameter update signal.
    - Computation Latency: End-to-end inference time in milliseconds.
"""

import torch
import time

theta = torch.randn(1024, 1024, requires_grad=True)
input_latent = torch.randn(1, 1024)

print(f"--- Initiating Surprisal Computation Benchmark ---")
start_time = time.time()

prediction = input_latent @ theta

surprisal_loss = prediction.pow(2).sum()

surprisal_loss.backward()

gradient_norm = theta.grad.norm().item()
end_time = time.time()

print(f"Status: SUCCESS")
print(f"Gradient Norm (S_t): {gradient_norm:.4f}")
print(f"Computation Latency: {(end_time - start_time)*1000:.2f} ms")
