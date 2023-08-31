import torch
import time

if torch.cuda.is_available():
   print ("CUDA is available")
   device = torch.cuda.current_device()
   gpu_properties = torch.cuda.get_device_properties(device)
   print("Found %d GPUs available.\nUsing GPU %d (%s) of compute capability %d.%d with "
          "%.1fGb total memory.\n" %
          (torch.cuda.device_count(),
          device,
          gpu_properties.name,
          gpu_properties.major,
          gpu_properties.minor,
          gpu_properties.total_memory / 1e9))
else:
   print ("CUDA is not available")

