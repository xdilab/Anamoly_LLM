from pathlib import Path
import os

def make_windows(file_path, window=20, step=20, max_windows=100):
    """
    Stream Thunderbird logs, group into fixed windows, and yield
    (label, [log_messages]) tuples.
    """
    with open(file_path, "r", errors="ignore") as f:
        buffer = []
        labels = []
        
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Split into label + rest of message
            parts = line.split(maxsplit=1)
            if len(parts) == 1:
                label, msg = "-", ""
            else:
                label, msg = parts
            
            buffer.append(msg)
            labels.append(label)
            
            # If we filled a window
            if len(buffer) == window:
                # Assign window label
                win_label = "Normal" if all(l == "-" for l in labels) else "Abnormal"
                
                yield win_label, buffer.copy()
                
                # Slide forward by step
                buffer = []
                labels = []



output_dir = "windows_output"
os.makedirs(output_dir, exist_ok=True)

max_windows = 1000000  # Set your desired limit here
abnormal_count = 0
for i, (label, logs) in enumerate(make_windows("/Users/zachariahlunsford/Downloads/tbird2", window=20, step=20)):
    if i >= max_windows:
        break
    if label == "Abnormal":
        abnormal_count += 1
        window_filename = os.path.join(output_dir, f"abnormal_window_{abnormal_count:05d}.txt")
        with open(window_filename, "w") as wf:
            wf.write(f"Label: {label}\n")
            wf.write("\n".join(logs))
            wf.write("\n")
        if abnormal_count == 1:
            print(f"First abnormal window written to {window_filename}")
if abnormal_count == 0:
    print("No abnormal windows found in the processed data.")

