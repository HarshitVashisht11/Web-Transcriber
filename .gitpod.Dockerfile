FROM gitpod/workspace-full

# Install essential dependencies
RUN sudo apt-get update && \
    sudo apt-get install -y python3-pip && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*

# Install PyTorch
RUN pip3 install torch==1.9.1+cpu torchvision==0.10.1+cpu torchaudio==0.9.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
