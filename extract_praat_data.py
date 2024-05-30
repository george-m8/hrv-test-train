import os
import sys
import subprocess
import tempfile
import re
import numpy as np

import os
import subprocess
import tempfile
import json
import numpy as np

def read_praat_output(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    # Regular expressions to extract data
    general_info_re = re.compile(r'(\w+) = ([\d\.\-e]+)')
    frame_re = re.compile(r'frames \[(\d+)\]:')
    intensity_re = re.compile(r'intensity = ([\d\.\-e]+)')
    nCandidates_re = re.compile(r'nCandidates = (\d+)')
    candidate_re = re.compile(r'candidates \[(\d+)\]:')
    frequency_re = re.compile(r'frequency = ([\d\.\-e]+)')
    strength_re = re.compile(r'strength = ([\d\.\-e]+)')

    data = {}
    
    # Extract general info
    general_info = general_info_re.findall(text)
    for key, value in general_info:
        data[key] = float(value)

    # Extract frames data
    frames = []
    frame_data = frame_re.split(text)[1:]  # Split based on frame_re and ignore first split part which is before first frame

    for i in range(0, len(frame_data), 2):
        frame_dict = {}
        frame_num = frame_data[i].strip()
        frame_dict['frame'] = int(frame_num)
        
        frame_content = frame_data[i + 1]
        frame_dict['intensity'] = float(intensity_re.search(frame_content).group(1))
        frame_dict['nCandidates'] = int(nCandidates_re.search(frame_content).group(1))
        
        candidates = []
        candidate_data = candidate_re.split(frame_content)[1:]  # Split based on candidate_re and ignore first split part which is before first candidate
        for j in range(0, len(candidate_data), 2):
            candidate_dict = {}
            candidate_num = candidate_data[j].strip()
            candidate_dict['candidate'] = int(candidate_num)
            candidate_content = candidate_data[j + 1]
            candidate_dict['frequency'] = float(frequency_re.search(candidate_content).group(1))
            candidate_dict['strength'] = float(strength_re.search(candidate_content).group(1))
            candidates.append(candidate_dict)
        
        frame_dict['candidates'] = candidates
        frames.append(frame_dict)

    data['frames'] = frames
    
    return data

def extract_praat_data(wav_file_path):
    # Create a temporary file to save the Praat output
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_praat_output_file:
        temp_praat_output_path = temp_praat_output_file.name

    # Path to the Praat script
    praat_script_path = 'extract_f0.praat'

    # Command to run Praat and extract pitch data
    praat_command = [
        'praat', '--run', praat_script_path, wav_file_path, temp_praat_output_path
    ]

    # Run the Praat command
    try:
        subprocess.run(praat_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Praat: {e}")
        return []

    # Check if the output file was created
    if os.path.exists(temp_praat_output_path):
        print(f"Praat output file created: {temp_praat_output_path}")
        # Read the pitch data from the Praat output
        frames_data = read_praat_output(temp_praat_output_path)
        # Debug print to check extracted values
        #print(f"Extracted frames data: {json.dumps(frames_data, indent=2)}")
        # Clean up temporary file
        os.remove(temp_praat_output_path)
        return frames_data
    else:
        print(f"Praat output file not found: {temp_praat_output_path}")
        return []
    
def save_to_json(data, output_file_path):
    with open(output_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def get_frequencies_per_frame(praat_json_data):
    frequencies = []
    for frame in praat_json_data['frames']:
        frame_frequencies = [candidate['frequency'] for candidate in frame['candidates']]
        frequencies.append(frame_frequencies)
    return frequencies

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_f0.py <wav_file_path>")
        sys.exit(1)
    else:
        wav_file_path = sys.argv[1]
        frames_data = extract_praat_data(wav_file_path)
        #print("Extracted data:\n", json.dumps(frames_data, indent=2))

        save_json_file = False

    if save_json_file:
        output_file_path = f"praat_{wav_file_path}.json"
        save_to_json(frames_data, output_file_path)
        print(f"Data saved to {output_file_path}")

    # Example of using the data immediately:
    frame_f0_frquencies = get_frequencies_per_frame(frames_data)
    #print("Frame frequencies:", frame_f0_frquencies)
    
    max_frequencies = [max(frame_frequencies) for frame_frequencies in frame_f0_frquencies if frame_frequencies]
    #print("Max frequency per frame:", max_frequencies)

    #print("Max frame intensity per frame:", max_intensity_per_frame)
