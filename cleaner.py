import ctypes
import sys
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        print("Requesting admin privileges...")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1)
            sys.exit()
        except:
            print("Failed to get admin privileges")
            sys.exit(1)
    return True

def clean_firewall():
    try:
        subprocess.run('netsh advfirewall firewall delete rule name="R-NS"', 
                      shell=True, check=True, capture_output=True)
        print("Firewall rule 'R-NS' successfully removed")
    except subprocess.CalledProcessError:
        print("No firewall rule 'R-NS' found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if run_as_admin():
        clean_firewall()
        input("Press Enter to exit...")
