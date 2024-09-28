FROM chenyu0517/rllm

COPY . /my_program

WORKDIR /my_program

# Environment setup
RUN apt-get update 

RUN python3 -m venv /my_envs

RUN /my_envs/bin/pip install --no-cache-dir -r requirements.txt
RUN service docker start

EXPOSE 8000


CMD ["/my_envs/bin/python3", "app.py"]