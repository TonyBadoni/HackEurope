import os
import sys
import subprocess as sp
from dotenv import load_dotenv

load_dotenv()

p1 = sp.run(["uv", "run", "python3", "backend/agents/mitre_classifier/main.py"], check=True)

if p1.returncode != 0:
    print("Classification failed")