import subprocess
import os
import requests
import re


class Ollama_Base():
    def __init__(self, gpu, port, sys_promt_dir, container_info:list, is_docker_compose=False) -> None:
        self.gpu = gpu
        self.port = port
        self.sys_prompt_dir = sys_promt_dir
        self.is_docker_compose = is_docker_compose
        self.is_init_need = True
        
        self.init_ollama_model(container_info)
        
    def generate_text(self, model_name:str, prompt:str, task:str, max_token=4096) -> dict: 
        
        url = f"http://localhost:{self.port}/api/generate"
        data = {
            "model": model_name,
            "prompt": prompt+task,
            "options": {
                "num_ctx": max_token
            }
        }
        
        response = requests.post(url, json=data)

        # Check the response status and content
        if response.status_code == 200:
            data = (response.text)
            # Regular expression pattern to match "response" fields
            pattern = r'"response":"(.*?)"'

            # Extract all response values using re.findall
            response_text = re.findall(pattern, data)
            return ''.join(response_text)
        else:
            raise f"Error: {response.status_code}, {response.text}"
    
    # def init_ollama_docker(self) -> None:
    #     # Path to the .sh file you want to execute
    #     script_path = "./run_ollama.sh"
    #     # Run the shell script using subprocess
    #     try:
    #         result = subprocess.run([script_path, str(self.gpu), str(self.port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    #         # Print the output of the script
    #         print("Initializing ollama dokcer:\n", result.stdout)
    #     except subprocess.CalledProcessError as e:
    #         # Print error message if the script fails
    #         print(f"Error occurred: {e.stderr}")
    
    def init_ollama_docker_compose(self) -> None:
        try:
            result = subprocess.run(['docker', 'compose', 'up'], stderr=subprocess.PIPE, text=True, check=True)
        except subprocess.CalledProcessError as e:
            # Print error message if the script fails
            print(f"Error occurred: {e.stderr}")
    
    def init_ollama_model(self, model_name_list:list, method:str):
        # if method == "dokcerfile":
        #     self.init_ollama_docker()
        if method == "dockercompose":
            self.init_ollama_docker_compose()
        else:
            raise "ValueError: method should be either \"dockerfile\" or \"dockercompose\""
        
        for container_info in model_name_list:
            # container_info = [container_name:str, model_name:str]
            self.is_model_init(container_info[0], container_info[1])
            if self.is_init_need:
                try:
                    result = subprocess.run(
                        ['docker', 'exec', '-it', container_info[0], 'ollama', 'pull', container_info[1]],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    # Check if the command was successful
                    if result.returncode == 0:
                        return f"Model pull successful:\n{result.stdout}"
                    else:
                        return f"Error during model pull:\n{result.stderr}"
                except Exception as e:
                    return f"An error occurred: {str(e)}"            
            
    
    def is_model_init(self, contianer_name:str, model_name:str) -> None:
        try:
             # Run the docker command to list models
            result = subprocess.run(
                ['docker', 'exec', '-it', contianer_name, 'ollama', 'list'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
 
            # Check if the model name is in the result
            if model_name in result.stdout:
                self.is_init_need = False
            else:
                self.is_init_need = True
        
        except Exception as e:
            return f"An error occurred: {str(e)}"