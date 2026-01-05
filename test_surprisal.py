import torch
import time

# Initialisering af en agents videns-vægte (theta)
# Vi bruger 1024x1024 for at teste din AMD processors throughput
theta = torch.randn(1024, 1024, requires_grad=True)
input_latent = torch.randn(1, 1024)

print(f"--- Initiating Surprisal Test on AMD Ryzen 5 7535HS ---")
start_time = time.time()

# Forward pass: Projektion i det latente rum
prediction = input_latent @ theta

# Beregn 'Surprise' (Loss)
# I IWL er surprise kvadratet på afvigelsen i det latente rum
surprisal_loss = prediction.pow(2).sum()

# Backward pass: Beregn gradient-normen (Det faktiske læringssignal)
surprisal_loss.backward()

gradient_norm = theta.grad.norm().item()
end_time = time.time()

print(f"Status: SUCCESS")
print(f"Beregnet Gradient Norm (S_t): {gradient_norm:.4f}")
print(f"Beregningstid: {(end_time - start_time)*1000:.2f} ms")

