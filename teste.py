import GPUtil
gpu = GPUtil.getGPUs()[0]
print(gpu.temperature)