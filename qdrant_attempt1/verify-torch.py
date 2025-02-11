import torch

print(torch.cuda.is_available())

if torch.cuda.is_available():
    device = torch.device('cuda')
    print(f"Using device: {device}")
    x = torch.tensor([1, 2, 3]).to(device)
    print(x)

