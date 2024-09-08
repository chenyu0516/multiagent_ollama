#! bin/bash

# Check if a parameter for --gpu is provided
if [ -z "$1" ]; then
    echo "No GPU parameter provided. Usage: ./run_ollama.sh [gpu|None]"
    exit 1
fi

if [ -z "$2" ]; then
    echo "The port is set to default 11434"
    port='11434:11434'
    else
    port="$2:11434"
fi

if command -v docker &> /dev/null
then
    # Check if the nvidia-container-toolkit is installed by running 'dpkg -l | grep nvidia-container-toolkit'
    if dpkg -l | grep -q nvidia-container-toolkit
    then
        # Set the GPU flag based on the input parameter
        if [ "$1" == "None" ]; then
            # No GPU flag, will run on CPU
            echo "Running ollama on CPU"
            docker run -d -v ollama:/root/.ollama -p "$port" --name ollama ollama/ollama
        else
            echo "Running ollama with GPU $1"
            docker run -d --gpus="$1" -v ollama:/root/.ollama -p "$port" --name ollama ollama/ollama
fi
    else
        echo "nvidia-container-toolkit is not installed"
        exit 1
    fi
else
    echo "Docker is not installed"
    exit
fi

# Run the Docker command with the appropriate GPU flag
docker run -d $gpu_flag -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama