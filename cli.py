import click
import requests
import json
import os

BASE_URL = "http://localhost:8000"

@click.group()
def cli():
    """Excel AI Version Control System CLI"""
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def upload(file_path):
    """Upload an Excel file to the system."""
    url = f"{BASE_URL}/upload"
    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            result = response.json()
            click.echo(f"Successfully uploaded: {result['version_id']}")
            click.echo(json.dumps(result['metadata'], indent=2))
        else:
            click.echo(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        click.echo(f"Exception: {e}")

@cli.command()
@click.argument('v1')
@click.argument('v2')
def compare(v1, v2):
    """Compare two versions of Excel files."""
    url = f"{BASE_URL}/compare"
    params = {"v1": v1, "v2": v2}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            click.echo(json.dumps(response.json(), indent=2))
        else:
            click.echo(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        click.echo(f"Exception: {e}")

@cli.command()
@click.argument('v1')
@click.argument('v2')
@click.option('--question', '-q', help='Natural language query')
def insights(v1, v2, question):
    """Get AI-generated insights for two versions."""
    url = f"{BASE_URL}/ask"
    payload = {"v1": v1, "v2": v2, "question": question}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            click.echo(f"AI Response:\n{response.json()['answer']}")
        else:
            click.echo(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        click.echo(f"Exception: {e}")

if __name__ == '__main__':
    cli()
