from .base import Ollama_Base
from .prompt import *

class Multiagent(Ollama_Base):
    def __init__(self, gpu, port, sys_promt_dir, container_info:list, is_docker_compose=False) -> None:
        super().__init__(gpu, port, sys_promt_dir, container_info, is_docker_compose)
        
    def forward(self, task, max_token_refute = 1024):
        refute_history = []
        refuting = ''
        general_prompt_ans = ANSWERING_PROMPT+task+'\n Refuting History:\n'
        general_prompt_ref = QUESTION_PROMPT+task+'\n Refuting History:\n'
        general_prompt_sum = SUMMARY_PROMPT+task+'\n Refuting History:\n'
        while ("OK" not in refuting):
            refute_history = '\n'.join(refute_history)
            answer = self.generate_text(self.container_info[0][1],
                                       prompt=general_prompt_ans+refute_history+'\n The Refuting:\n'+refuting+'\n The Answer:\n',
                                       max_token=max_token_refute)
            refute_history.append(f"Answer: {answer}")
            
            refuting = self.generate_text(self.container_info[1][1],
                                          prompt=general_prompt_ref+refute_history+'\n The Answer:\n'+answer+'\n The Refuting:\n',
                                          max_token=max_token_refute)
            refute_history.append(f"Refuting: {refuting}")
            
        refute_history = '\n'.join(refute_history)
        return self.generate_text(self.container_info[0][1],
                                prompt=general_prompt_sum+refute_history+'\n The Summary:\n',
                                max_token=4096)    
         
        