import subprocess
import os
import sys



def run_script(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution de {script_name} : {result.stderr}")
    else:
        print(f"Succès de l'exécution de {script_name} : {result.stdout}")

def main():
    scripts = [
        'scripts/data_cleaning.py',
        'scripts/data_fetching.py',
        'scripts/data_ingestion.py'
    ]

    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()