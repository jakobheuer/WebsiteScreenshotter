import os
import json
import time
import threading
from tkinter import Tk, Label, DoubleVar, ttk, Toplevel, Message
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class ScreenshotApp:
    def __init__(self, master, data):
        self.master = master
        self.data = data
        self.start_time = datetime.now()
        self.lock = threading.Lock()
        self.valid_ports = {"80", "443", "8080", "8443"}
        self.total_tasks = sum(1 for value in data.values() for port in value["ports"] if port in self.valid_ports)
        self.completed_count = 0
        self.failures = 0
        self.screenshots_per_port = {port: 0 for port in self.valid_ports}

        self.master.title("Screenshot Progress")
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(master, variable=self.progress_var, maximum=self.total_tasks)
        self.progress_bar.pack(fill="x", expand=1, padx=20, pady=20)
        self.status_label = Label(master, text="Starting...")
        self.status_label.pack(padx=20, pady=10)

        threading.Thread(target=self.start_screenshot_process).start()

    def take_screenshot(self, hostname, port):
        url = f"http://{hostname}:{port}" if port in ["80", "8080"] else f"https://{hostname}:{port if port else ''}"
        path = f'./screenshots/{port}/{hostname}.png'

        chrome_options = Options()
        chrome_options.add_argument('ignore-certificate-errors')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)

        try:
            driver.get(url)
            driver.save_screenshot(path)
            with self.lock:
                self.screenshots_per_port[port] += 1
        except Exception as e:
            with self.lock:
                self.failures += 1
        finally:
            driver.quit()

        with self.lock:
            self.completed_count += 1
            self.progress_var.set(self.completed_count)
            percentage = (self.completed_count / self.total_tasks) * 100
            self.status_label.config(text=f"Completed {self.completed_count}/{self.total_tasks} screenshots... ({percentage:.2f}%)")
            if self.completed_count == self.total_tasks:
                self.show_statistics()

    def start_screenshot_process(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            for ip, value in self.data.items():
                hostname = value["hostname"]
                for port in value["ports"]:
                    if port in self.valid_ports:
                        executor.submit(self.take_screenshot, hostname, port)
        
    def show_statistics(self):
        end_time = datetime.now()
        runtime = (end_time - self.start_time).total_seconds()
        stats_message = f"Runtime: {runtime} seconds\n"
        stats_message += f"Total Screenshots: {sum(self.screenshots_per_port.values())}\n"
        stats_message += f"Failures: {self.failures}\n"
        for port, count in self.screenshots_per_port.items():
            stats_message += f"Screenshots for port {port}: {count}\n"

        # Statistics Display
        stats_window = Toplevel(self.master)
        stats_window.title("Statistics")
        Message(stats_window, text=stats_message, width=400).pack(padx=20, pady=20)
        stats_window.transient(self.master)

if __name__ == "__main__":
    with open('scan.json', 'r') as f:
        data = json.load(f)

    os.makedirs("./screenshots/80", exist_ok=True)
    os.makedirs("./screenshots/8080", exist_ok=True)
    os.makedirs("./screenshots/443", exist_ok=True)
    os.makedirs("./screenshots/8443", exist_ok=True)

    root = Tk()
    app = ScreenshotApp(root, data)
    root.mainloop()
