# control.py - Windows Control Panel Power Options
import machine
import sys

print("\n--- Control Panel \\ Hardware and Sound \\ Power Options ---")
print("1: Power Saver Mode     (Clock CPU down to 80MHz)")
print("2: Balanced Management  (Clock CPU down to 160MHz)")
print("3: High Performance     (Clock CPU up to 240MHz)")
print("4: Cancel Operations")

selection = input("\nSelect system power profile (1-4): ").strip()

if selection == "1":
    machine.freq(80000000)
    print(f"CPU clocked down to {machine.freq() // 1000000}MHz. Power footprint reduced.")
elif selection == "2":
    machine.freq(160000000)
    print(f"CPU clocked to balanced {machine.freq() // 1000000}MHz profile configuration.")
elif selection == "3":
    machine.freq(240000000)
    print(f"WARNING: Maximum system speed active ({machine.freq() // 1000000}MHz). Monitor silicon temperatures.")
else:
    print("Configuration changes aborted by user environment choice.")
