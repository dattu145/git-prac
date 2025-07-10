import os
import subprocess

def bisect_with_dir(repo_subdir="gitbisectg"):
    current_dir = os.getcwd()  # gitprac
    repo_path = os.path.join(current_dir, repo_subdir)  # subdir

    try:
        while True:
            os.chdir(repo_path)

            subprocess.run(["git", "stash", "--keep-index"])

            out = subprocess.run(["make", "Run"], shell=True, capture_output=True, text=True)
            output = out.stdout.strip()
            print(output)

            os.chdir(current_dir)

            if 'Hello World!' in output:
                result = subprocess.run(["git", "bisect", "good"], capture_output=True, text=True)
            else:
                result = subprocess.run(["git", "bisect", "bad"], capture_output=True, text=True)

            if "is the first bad commit" in result.stdout:
                print("Found First Bad Commit!")
                print(result.stdout)
                break

            if result.returncode != 0:
                print("Bisect command failed or already completed.")
                break

    finally:
        subprocess.run(["git", "bisect", "reset"])

subprocess.run(["git", "log", "--oneline"])

first = input("Enter Good commit hash: ").strip()
second = input("Enter Bad commit hash: ").strip()

subprocess.run(["git", "bisect", "start"])
subprocess.run(["git", "bisect", "bad", second])
subprocess.run(["git", "bisect", "good", first])

bisect_with_dir()
