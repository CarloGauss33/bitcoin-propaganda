import subprocess

if __name__ == "__main__":
    print("Starting bitcoin-propaganda")

    subprocess.Popen(["python", "chat_manager.py"],
                     shell=False)

    print("Done")