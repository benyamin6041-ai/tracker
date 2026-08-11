import subprocess
import sys

def main():
    # اجرای فایل اصلی در پس زمینه
    subprocess.Popen([sys.executable, "main.py"])

if __name__ == "__main__":
    main()
