import torch

# pip uninstall torch torchvision torchaudio -y
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

print(torch.cuda.is_available())
print(torch.version.cuda)
print(torch.cuda.get_device_name(0))
