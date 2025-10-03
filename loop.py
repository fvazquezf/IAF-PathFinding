import subprocess
import os

# Define your sets
folders_sets = [
    # ("breath/3x3", "depth/3x3", "astar/3x3"),
    # ("breath/5x5", "depth/5x5", "astar/5x5"),
    # ("breath/7x7", "depth/7x7", "astar/7x7"),
    ("breath/9x9", "depth/9x9", "astar/9x9"),
]

files_sets = [
    # ["part_1.txt", "part_2.txt", "part_3.txt", "part_4.txt", "part_5.txt"],
    # ["part_6.txt", "part_7.txt", "part_8.txt", "part_9.txt", "part_10.txt"],
    # ["part_11.txt", "part_12.txt", "part_13.txt", "part_14.txt", "part_15.txt"],
    ["part_16.txt", "part_17.txt", "part_18.txt", "part_19.txt", "part_20.txt"],
]

# Loop through each set
for folders, files in zip(folders_sets, files_sets):
    for folder in folders:
        # Extract the type name from folder path, e.g., "breath/3x3" -> "breath"
        folder_type = folder.split("/")[0]
        output_dir = folder  # Save output in the same folder
        os.makedirs(output_dir, exist_ok=True)

        for file_name in files:
            input_file = file_name
            output_file = os.path.join(output_dir, f"{file_name}_output.txt")

            # Call the other script and redirect output to the file
            with open(output_file, "w") as f:
                subprocess.run(
                    ["python3", "pathFinding.py", folder_type, input_file],
                    stdout=f,
                    stderr=subprocess.STDOUT
                )

            print(f"Processed {input_file} -> {output_file}")
