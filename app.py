from flask import Flask, request, jsonify
import subprocess

from llm import Multiagent



app = Flask(__name__)
    

@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        container_info = request.args.get('container_info', default=[["ollama1", "llama3.1:70b", 11434], ["ollama1", "llama3.1:70b", 11434]])
        multiagent = Multiagent(container_info)
        task = request.args.get('task', default = "Why the sky is blue?")
        result_dict = multiagent.forward(task=task)
        
        # Return the result as a JSON response
        return jsonify(result_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on port 5000 (or any other port you expose)
    app.run(host='0.0.0.0', port=8000)
    
    