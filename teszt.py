import torch
import os

# pip uninstall torch torchvision torchaudio -y
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

cls = None

try:
    if os.name == "nt":
        cls= "cls"  
    else:
        cls = "clear" 

    os.system(cls)
except Exception:
    pass

print(f"torch.cuda.is_available(): {torch.cuda.is_available()}")
print(f"torch.version.cuda: {torch.version.cuda}")
print(f"torch.cuda.get_device_name(0): {torch.cuda.get_device_name(0)}")
