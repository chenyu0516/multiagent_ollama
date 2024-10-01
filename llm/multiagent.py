from .base import Ollama_Base
from .prompt import *

import requests
import re
import time

class Multiagent(Ollama_Base):
    def __init__(self, container_info:list) -> None:
        super(Multiagent, self).__init__(container_info)
        
    def forward(self, task, max_token_refute = 4096):
        refute_history = []
        refuting = ""
        refute_history_text = ""
        general_prompt_ans = ANSWERING_PROMPT+task+'\n **Refuting History**:\n'
        general_prompt_ref = REFUTING_PROMPT+task+'\n **Refuting History**:\n'
        general_prompt_sum = SUMMARY_PROMPT+task+'\n **Refuting History**:\n'
        
        while ('OK' not in refuting):
            answer = self.generate_text(self.container_info[0][1],
                                        port=self.container_info[0][2],
                                       prompt=general_prompt_ans+'\n'.join(refute_history[-6:-1])+'\n**The Refuting**:\n'+refuting,
                                       max_token=max_token_refute)
            
            refute_history.append(f"Answer: {answer}")
            time.sleep(1)
            refuting = self.generate_text(self.container_info[0][1],
                                          port=self.container_info[0][2],
                                          prompt=general_prompt_ref+'\n'.join(refute_history[-6:-1])+'\n**The Answer**:\n'+answer,
                                          max_token=max_token_refute)
            refute_history.append(f"Refuting: {refuting}")
            refute_history_text = self.generate_text(self.container_info[0][1],
                                  port=self.container_info[0][2],
                                prompt=general_prompt_sum+'\n'.join(refute_history[-10:])+'\n The Summary:\n',
                                max_token=4096)
        time.sleep(1)
        return {"result":
            self.generate_text(self.container_info[0][1],
                                  port=self.container_info[0][2],
                                prompt=general_prompt_sum+refute_history_text+'\n**The Summary**:\n',
                                max_token=4096),
                "refute_history": refute_history
        }
         
    def generate_text(self, model_name:str, port:int, prompt:str, max_token=4096) -> dict: 
        url = f"http://localhost:{port}/api/generate"
        data = {
            "model": model_name,
            "prompt": prompt,
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
            response_text_list = re.findall(pattern, data)
            response_text = ''.join(response_text_list)

            return response_text
        else:
            return 0
    def forward_without_refute(self, task):
        
        answer = self.generate_text(self.container_info[0][1],
                                    port=self.container_info[0][2],
                                   prompt=task,
                                   max_token=4096)
        
        return {"result": answer}