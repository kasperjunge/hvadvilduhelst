import json
import os
from pathlib import Path
from typing import List, Dict

def load_hygdk_dataset(data_dir: str = "/Users/kasperjunge/gitrepo/datasets/hvadvilduhelst/data/hygdk") -> List[Dict]:
    """
    Load the hygdk dataset from JSONL files.
    
    Args:
        data_dir (str): Path to the directory containing the JSONL files
        
    Returns:
        List[Dict]: List of dictionaries containing questions, answers, and categories
    """
    dataset = []
    data_path = Path(data_dir)
    
    # Iterate through all JSONL files in the directory
    for file_path in data_path.glob("*.jsonl"):
        # Get category name from filename (remove .jsonl extension)
        category = file_path.stem
        
        # Read and process each line in the file
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                entry = {
                    'questions': data['question'],
                    'answer_A': data['answer_A'],
                    'answer_B': data['answer_B'],
                    'category': category
                }
                dataset.append(entry)
    
    return dataset