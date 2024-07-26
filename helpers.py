import os
import argparse

# 1. Argument parser
# 2. Directory creation


""" 1. Argument parser for model and role """

# Create a parser object
parser = argparse.ArgumentParser(description="Script to process model and role")

# Add optional 'model' argument
parser.add_argument(
    "--m",
    default="gpt-4o-mini",
    choices=[
        'gpt-4o-mini',
        'gpt-4o',
        'gpt-4',
        'gpt-4-turbo',
        'gpt-3.5-turbo',
        'meta-llama/Meta-Llama-3-8B-Instruct',
    ],
    help="The model to use (optional)"
)

# Add optional 'role' argument
parser.add_argument(
    "--r",
    default="short and concise",
    choices=[
        'short and concise',
        'correct english',
        'correct german',
        'translate to english',
        'translate to german',
        'translate to spanish',
        'translate to french',
        'translate to hungarian',
        'generate a filename',
    ],
    help="The mode to response to the prompt (optional)"
)


""" 2. Create directories if not exists """

def create_directories(main, sub):
    os.makedirs(main, exist_ok=True)
    os.makedirs(os.path.join(main, sub), exist_ok=True)


    