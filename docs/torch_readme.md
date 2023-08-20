# Proper torch installation

PyTorch is completely broken in Poetry, have to use pip
https://github.com/python-poetry/poetry/issues/6409

None of this works in `pyproject.toml`: 

torch = {url = "https://download.pytorch.org/whl/nightly/cu121/torch-2.1.0.dev20230819%2Bcu121-cp311-cp311-linux_x86_64.whl", platform = "linux", python = "~3.11"}

This also does not work, since it will download ALL combinations of ARCH x OS X CUDA:

torch = {version = "2.1.0.dev20230819+cu121", platform = "linux", source = "torch_cuda"}
torchaudio = {version = "2.1.0.dev20230819+cu121", platform = "linux", source = "torch_cuda"}
torchvision = {version = "0.16.0.dev20230819+cu121", platform = "linux", source = "torch_cuda"}

[START LOCALLY](https://pytorch.org/get-started/locally/)

```shell
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
```