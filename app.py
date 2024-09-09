from flask import Flask, jsonify
import subprocess

from llm import Multiagent


container_info = [["ollama1", "llama3.1:8b", 0], ["ollama2", "llama3.1:8b", 1]]
multiagent = Multiagent(container_info)

app = Flask(__name__)

# Route to return the result of the Python script
@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        result_dict = multiagent.forward(task="Why the sky is blue?")
        
        # Return the result as a JSON response
        return jsonify(result_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on port 5000 (or any other port you expose)
    app.run(host='0.0.0.0', port=8000)
    
    