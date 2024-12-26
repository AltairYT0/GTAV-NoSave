import tkinter as tk
import keyboard
import subprocess
import os
import sys
import ctypes
import threading
import time
import queue
from datetime import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        print("Requesting admin privileges...")
        try:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join(sys.argv[1:])
            ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
            if ret > 32:
                sys.exit(0)
            else:
                print("Failed to get admin privileges")
                sys.exit(1)
        except Exception as e:
            print(f"Failed to get admin privileges: {e}")
            sys.exit(1)
    return True

class FirewallController:
    def __init__(self):
        self.root = None
        self.status = "Disabled"
        self.running = True
        self.gui_thread = None
        self.gui_queue = queue.Queue()
        self.notification_queue = queue.Queue()
        self.notification_processing = False
        self.current_gui_status = None
        self.animation_running = False
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== GTA V NoSave Firewall Controller ===")
        print("Running and waiting for hotkeys...")
        print("Controls:")
        print("- CTRL + F9  : Enable Firewall Rule")
        print("- CTRL + F12 : Disable Firewall Rule")
        print("Note: 2 second cooldown between switches")
        print("\nLog:")
        
        self.notification_thread = threading.Thread(target=self.process_notifications)
        self.notification_thread.daemon = True
        self.notification_thread.start()
        
        self.monitor_thread = threading.Thread(target=self.hotkey_monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def process_notifications(self):
        while self.running:
            try:
                notification = self.notification_queue.get()
                if notification is None:
                    break
                
                while not self.notification_queue.empty():
                    self.notification_queue.get()
                
                self.notification_processing = True
                
                if self.current_gui_status != notification:
                    self.safe_close_gui()
                
                self.current_gui_status = notification
                self.gui_queue.put(notification)
                if not self.gui_thread or not self.gui_thread.is_alive():
                    self.gui_thread = threading.Thread(target=self.create_gui)
                    self.gui_thread.daemon = True
                    self.gui_thread.start()
                
                self.notification_processing = False
                self.notification_queue.task_done()
            except:
                self.notification_processing = False
            time.sleep(0.1)

    def log_action(self, action):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Firewall rule {action}")

    def safe_close_gui(self):
        if self.root:
            try:
                self.animation_running = False
                if self.root:
                    self.root.quit()
                    self.root.destroy()
            except:
                pass
            self.root = None

    def create_gui(self):
        try:
            self.root = tk.Tk()
            self.root.geometry("221x79")
            self.root.configure(bg="#252525")
            self.root.overrideredirect(True)
            self.root.attributes('-topmost', True)
            
            self.root.bind("<Button-1>", lambda e: "break")
            self.root.bind("<Button-2>", lambda e: "break")
            self.root.bind("<Button-3>", lambda e: "break")
            self.root.bind("<Motion>", lambda e: "break")

            window_width = 221
            window_height = 79
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            final_x = screen_width - window_width - 20
            y = (screen_height - window_height) // 2
            self.root.geometry(f"{window_width}x{window_height}+{screen_width}+{y}")

            content_frame = tk.Frame(self.root, bg="#252525")
            content_frame.place(x=0, y=0, width=window_width, height=window_height)

            title_label = tk.Label(
                content_frame,
                text="GTA V | NoSave",
                fg="white",
                bg="#252525",
                font=("Arial", 10)
            )
            title_label.place(x=5, y=5)

            current_status = self.gui_queue.get()
            status_label = tk.Label(
                content_frame,
                text=current_status,
                fg="red" if current_status == "Disabled" else "green",
                bg="#252525",
                font=("Arial", 10)
            )
            status_label.place(x=5, y=25)

            canvas = tk.Canvas(content_frame, height=2, width=window_width, bg="#252525", highlightthickness=0)
            canvas.place(x=0, y=77)
            line = canvas.create_line(0, 1, 0, 1, fill="red" if current_status == "Disabled" else "green", width=2, smooth=True)

            self.animation_running = True

            def slide_in(current_x=screen_width):
                if not self.animation_running:
                    return
                if current_x > final_x:
                    new_x = current_x - (current_x - final_x) * 0.2
                    if abs(new_x - final_x) < 1:
                        new_x = final_x
                    self.root.geometry(f"{window_width}x{window_height}+{int(new_x)}+{y}")
                    self.root.after(16, lambda: slide_in(new_x))

            def slide_out(current_x=final_x):
                if not self.animation_running:
                    return
                if current_x < screen_width:
                    new_x = current_x + (screen_width - current_x) * 0.2
                    if abs(new_x - screen_width) < 1:
                        new_x = screen_width
                    self.root.geometry(f"{window_width}x{window_height}+{int(new_x)}+{y}")
                    if new_x < screen_width:
                        self.root.after(16, lambda: slide_out(new_x))
                    else:
                        self.safe_close_gui()

            def update_line(current_width=0):
                if not self.animation_running:
                    return
                if current_width < window_width:
                    new_width = current_width + (window_width - current_width) * 0.1
                    canvas.coords(line, 0, 1, new_width, 1)
                    if new_width < window_width - 0.5:
                        self.root.after(16, lambda: update_line(new_width))
                    else:
                        canvas.coords(line, 0, 1, window_width, 1)
                        self.root.after(500, slide_out)

            self.root.after(50, slide_in)
            self.root.after(100, update_line)
            self.root.mainloop()
        except Exception as e:
            print(f"GUI Error: {e}")
            self.safe_close_gui()

    def show_notification(self):
        self.notification_queue.put(self.status)

    def enable_firewall(self):
        try:
            command = 'netsh advfirewall firewall add rule name="R-NS" dir=out action=block remoteip=192.81.241.171'
            subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            self.status = "Enabled"
            self.log_action("ENABLED")
            self.show_notification()
        except subprocess.CalledProcessError as e:
            self.log_action(f"ENABLE FAILED - {e.stderr.strip()}")

    def disable_firewall(self):
        try:
            command = 'netsh advfirewall firewall delete rule name="R-NS"'
            subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            self.status = "Disabled"
            self.log_action("DISABLED")
            self.show_notification()
        except subprocess.CalledProcessError as e:
            self.log_action(f"DISABLE FAILED - {e.stderr.strip()}")

    def hotkey_monitor(self):
        last_action_time = 0
        cooldown = 2.0
        
        while self.running:
            current_time = time.time()
            if current_time - last_action_time >= cooldown:
                if keyboard.is_pressed('ctrl+f9'):
                    self.status = "Enabled"
                    self.enable_firewall()
                    last_action_time = current_time
                    print(f"\n[COOLDOWN] Please wait {cooldown} seconds before next switch")
                elif keyboard.is_pressed('ctrl+f12'):
                    self.status = "Disabled"
                    self.disable_firewall()
                    last_action_time = current_time
                    print(f"\n[COOLDOWN] Please wait {cooldown} seconds before next switch")
            time.sleep(0.1)

    def quit_program(self):
        self.running = False
        self.notification_queue.put(None)
        self.safe_close_gui()
        try:
            subprocess.run('netsh advfirewall firewall delete rule name="R-NS"', 
                         shell=True, check=True, capture_output=True)
            self.log_action("CLEANUP - Firewall rule removed")
        except:
            self.log_action("CLEANUP - No firewall rule to remove")
        self.log_action("PROGRAM TERMINATED")
        os._exit(0)

def main():
    if run_as_admin():
        app = FirewallController()
        try:
            while app.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            app.quit_program()

if __name__ == "__main__":
    main()
