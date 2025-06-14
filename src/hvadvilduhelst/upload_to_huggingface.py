import json
import os
from pathlib import Path
from typing import List, Dict
from datasets import Dataset
from huggingface_hub import HfApi
from dotenv import load_dotenv
from hvadvilduhelst.load_hygdk import load_hygdk_dataset

# Load environment variables from .env file
load_dotenv()


def upload_to_huggingface(dataset: List[Dict], split: str = "train") -> None:
    """
    Upload the dataset to Hugging Face Hub.
    
    Args:
        dataset (List[Dict]): The dataset to upload
        split (str): The split name for the dataset (default: "train")
    """
    # Get token and repo_id from environment variables
    token = os.getenv("HUGGINGFACE_TOKEN")
    repo_id = os.getenv("HUGGINGFACE_REPO_ID")
    
    if not token:
        raise ValueError("HUGGINGFACE_TOKEN environment variable not set")
    if not repo_id:
        raise ValueError("HUGGINGFACE_REPO_ID environment variable not set")
    
    # Convert the dataset to a Hugging Face Dataset
    hf_dataset = Dataset.from_list(dataset)
    
    # Create a dictionary with the split
    dataset_dict = {split: hf_dataset}
    
    # Push to the Hub
    hf_dataset.push_to_hub(
        repo_id=repo_id,
        token=token,
        split=split
    )
    
    print(f"Successfully uploaded dataset to {repo_id}")

if __name__ == "__main__":
    # Load the dataset
    dataset = load_hygdk_dataset()
    
    # Upload to Hugging Face
    upload_to_huggingface(dataset=dataset) 