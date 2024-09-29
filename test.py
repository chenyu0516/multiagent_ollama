
import subprocess
import json

from llm import Multiagent


def run():
    try:
        container_info = [["ollama1", "llama3.1:8b", 11434], ["ollama1", "llama3.1:8b", 11434]]
        multiagent = Multiagent(container_info)
        task = "Why the sky is blue?"
        result_dict = multiagent.forward(task=task)
        
        # Return the result as a JSON response
        return result_dict, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    result, return_code = run()
    if return_code == 200:
        with open("result.json", "w") as file:
            json.dump(result, file, indent=4)