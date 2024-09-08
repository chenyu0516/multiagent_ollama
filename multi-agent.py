from .base import Ollama_Base

class Multiagent(Ollama_Base):
    def __init__(self, gpu, port, sys_promt_dir, container_info:list, is_docker_compose=False) -> None:
        super().__init__(gpu, port, sys_promt_dir, container_info, is_docker_compose)
        
    def init_multiple_agent(self):
        pass
         
        