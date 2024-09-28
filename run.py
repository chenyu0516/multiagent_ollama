import requests

def get_data_from_webapp(task=None):

    # Define the base URL of the web app
    url = 'http://localhost:8000/run-script'
    
    # Define the parameters for the GET request
    params = {'container_info':[["ollama1", "llama3.1:8b", 11434], ["ollama1", "llama3.1:8b", 11434]],
              'task': task} if task else {}
    
    try:
        # Send the GET request to the web app
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return data
        else:
            print(f"Error: Received status code {response.status_code}")
            return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    task = "Why are there so many people riding scrooters?"
    print("start_chatting")
    result = get_data_from_webapp(task)
    print(result)