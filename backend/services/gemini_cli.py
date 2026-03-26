import subprocess
import json
import os

def generate_insights(diff_data, prompt_path=None, prompt_text=None):
    """Calls the gemini CLI to generate insights based on the diff data."""
    
    # Save diff data to a temporary file
    temp_file = "temp_diff.json"
    with open(temp_file, "w") as f:
        json.dump(diff_data, f)
        
    try:
        # Construct the command
        # cat diff.json | gemini -p "Analyze these changes and provide insights"
        if prompt_text:
            final_prompt = prompt_text
        elif prompt_path and os.path.exists(prompt_path):
            with open(prompt_path, "r") as f:
                final_prompt = f.read()
        else:
            final_prompt = "Analyze these Excel diff changes and provide high-level insights, trends, and anomalies."
            
        # Escape single quotes in the prompt for the shell command
        escaped_prompt = final_prompt.replace("'", "'\\''")
        cmd = f"cat {temp_file} | gemini -p '{escaped_prompt}'"
        
        # Run the command and capture output
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error from Gemini CLI: {result.stderr.strip()}"
            
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)

def ask_question(diff_data, question):
    """Asks a specific natural language question about the diff data."""
    temp_file = "temp_diff.json"
    with open(temp_file, "w") as f:
        json.dump(diff_data, f)
        
    try:
        cmd = f"cat {temp_file} | gemini -p '{question}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error from Gemini CLI: {result.stderr.strip()}"
            
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
