import multiprocessing
import subprocess
import os

def run_backend():
    if os.path.exists("backend"):
        os.chdir("backend")
    
    subprocess.run(["python", "-m", "uvicorn", "backend:app", "--host", "127.0.0.1", "--port", "8000"], shell=True)

def run_frontend():
    subprocess.run(["python", "-m", "streamlit", "run", "Frontend/app.py"], shell=True)

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_backend)
    p2 = multiprocessing.Process(target=run_frontend)
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()