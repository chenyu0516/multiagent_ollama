import pandas as pd
import subprocess
import json
from tqdm import tqdm

from llm import Multiagent


def load_dataset_drop():
    splits = {'train': 'data/train-00000-of-00001.parquet', 'validation': 'data/validation-00000-of-00001.parquet'}

    df_test = pd.read_parquet("hf://datasets/ucinlp/drop/" + splits["train"])
    df_eva = pd.read_parquet("hf://datasets/ucinlp/drop/" + splits["validation"])
    df = pd.concat([df_test, df_eva], axis=0, ignore_index=True)

    # Make the dataset to a task answer pair of dataframe
    df.rename(columns={"passage": "task"}, inplace=True)
    df["task"] = df["task"]+df["question"]
    df["answers_spans"] = df["answers_spans"].apply(lambda x: x['spans'][0])
    df.drop(columns=["section_id", "query_id", "question"], inplace=True)
    df.dropna(axis=1, inplace=True)
    
    return df

def run(task):
    try:
        container_info = [["ollama1", "llama3:8b", 11434], ["ollama1", "llama3:8b", 11434]]
        multiagent = Multiagent(container_info)
        result_dict = multiagent.forward(task=task)
        
        # Return the result as a JSON response
        return result_dict, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 500

if __name__ == '__main__':
    df = load_dataset_drop()
    data = df.iloc[:200, :]
    len_data = len(data.index)
    score = 0
    result_list = []
    for i in tqdm(range(len_data)):
        
        result, return_code = run(task=data.iloc[i, 0])    
        if return_code == 200:
            if data.iloc[i, 1] in result["result"]:
                score += 1
                result["is_right"] = True
            else:
                result["is_right"] = False
            result_list.append(result)
    
    final_score = score/len_data
    print(final_score)
    with open("result.json", "w") as file:
        json.dump({"final_score": final_score, "result_detail":result_list}, file, indent=4)