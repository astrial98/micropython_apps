import os
import sys
import gc
import machine
import time
import network
import urequests

class Windows7Kernel:
    def __init__(self):
        machine.freq(160000000)
        self.current_dir = "C:\\"
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.github_base = "https://raw.githubusercontent.com/astrial98/micropython_apps/refs/heads/main"

    def boot_animation(self):
        print("\nStarting Windows...")
        time.sleep(1)
        print("\n" + "="*50)
        print("   Microsoft Windows [Version 6.1.7601]")
        print("   Copyright (c) 2009 Microsoft Corporation. All rights reserved.")
        print("="*50 + "\n")

    def show_help(self):
        print("Available Commands:")
        print("  DIR        - Displays local files on Drive C.")
        print("  DEL / ERASE- Deletes one or more files from Drive C (e.g., DEL test_app.py).")
        print("  SYSTEMINFO - Displays physical hardware specifications and RAM.")
        print("  IPCONFIG   - Queries network configurations and Wi-Fi link status.")
        print("  PKG PULL   - Pulls an application file from your remote GitHub repo.")
        print("  CLS / SHUTDOWN")

    def run_exe(self, filename):
        if not filename.endswith(".py"):
            filename += ".py"
        if filename not in os.listdir():
            print(f"'{filename}' is not recognized as an internal or external command.")
            return
        try:
            with open(filename, 'r') as f:
                exec(f.read(), globals())
        except Exception as e:
            print(f"App Exception: {e}")
        gc.collect()

    def pkg_manager(self, args):
        if not args or args.upper() != "PULL" or len(args) < 2:
            print("Usage: PKG PULL <filename.py>")
            return
        
        filename = args
        if not filename.endswith(".py"):
            filename += ".py"
            
        if not self.wlan.isconnected():
            print("❌ Deployment Failure: No active network interface. Run IPCONFIG /CONNECT first.")
            return
            
        url = self.github_base + filename
        print(f"Connecting to remote repository: {self.github_base}")
        print(f"Fetching manifest payload: {filename}...")
        
        try:
            response = urequests.get(url)
            if response.status_code == 200:
                with open(filename, "w") as f:
                    f.write(response.text)
                print(f"✅ Success: File written to C:\\{filename} ({len(response.text)} bytes).")
                if filename == "os_kernel.py":
                    print("\n⚠️ WARNING: Core Operating System Kernel was updated over-the-air!")
                    print("Initiating immediate hardware hot-reload...")
                    time.sleep(2)
                    machine.reset()
            elif response.status_code == 404:
                print("❌ 404 Error: File not found in target GitHub branch / path.")
            else:
                print(f"❌ Network Error: Server responded with status code {response.status_code}")
            response.close()
        except Exception as e:
            print(f"❌ Transmission Error: Failed to pull script payload. Context: {e}")
        gc.collect()

    def cmd_prompt(self):
        self.boot_animation()
        while True:
            try:
                user_input = input(f"{self.current_dir}> ").strip()
                if not user_input:
                    continue
                
                parts = user_input.split()
                if not parts:
                    continue
                
                cmd = parts[0].upper()
                args = parts[1] if len(parts) > 1 else ""


                if cmd == "HELP":
                    self.show_help()
                elif cmd == "CLS":
                    print("\n" * 30)
                elif cmd == "DIR":
                    print(f" Directory of {self.current_dir}\n")
                    files = os.listdir()
                    for f in files:
                        try:
                            stats = os.stat(f)
                        except:
                            stats = 0
                        print(f"23/09/2026  07:30 PM    {stats:>10} {f}")
                elif cmd == "DEL" or cmd == "ERASE":
                    if args:
                        target_file = args
                        if not target_file.endswith(".py") and "." not in target_file:
                            target_file += ".py"
                        if target_file in os.listdir():
                            if target_file in ["main.py", "boot.py"]:
                                print(f"❌ Access Denied: Cannot delete protected system file '{target_file}'.")
                            else:
                                os.remove(target_file)
                                print(f"✅ File successfully deleted: C:\\{target_file}")
                        else:
                            print("Could Not Find File specified.")
                    else:
                        print("The syntax of the command is incorrect.")
                elif cmd == "SYSTEMINFO":
                    print("OS Name:                   Microsoft Windows 7 Ultimate")
                    print(f"Total Physical Memory:     {gc.mem_free() + gc.mem_alloc()} Bytes")
                    print(f"Available Physical Memory: {gc.mem_free()} Bytes")
                elif cmd == "SHUTDOWN":
                    machine.reset()
                elif cmd == "PKG":
                    self.pkg_manager(args)
                elif cmd == "IPCONFIG":
                    if args and args.upper() == "/CONNECT":
                        ssid = input("Enter Wi-Fi SSID (Name): ").strip()
                        pwd = input("Enter Wi-Fi Password: ").strip()
                        print(f"Connecting to {ssid}...")
                        self.wlan.connect(ssid, pwd)
                        for _ in range(10):
                            if self.wlan.isconnected(): break
                            time.sleep(1)
                        if self.wlan.isconnected():
                            print(f"✅ Link Established! Assigned IP: {self.wlan.ifconfig()}")
                        else:
                            print("❌ Connection Timeout. Check credentials.")
                    else:
                        print(f"Wireless LAN adapter Wi-Fi:")
                        if self.wlan.isconnected():
                            print(f"   Media State . . . . . . . . . . . : Connected")
                            print(f"   IPv4 Address. . . . . . . . . . . : {self.wlan.ifconfig()}")
                        else:
                            print(f"   Media State . . . . . . . . . . . : Media disconnected")
                        print("   Use 'IPCONFIG /CONNECT' to interface with a local access point.")
                else:
                    self.run_exe(parts)

            except KeyboardInterrupt:
                print("\n[Windows 7 Kernel Context Halted via Debugger]")
                break
            time.sleep_ms(5)
