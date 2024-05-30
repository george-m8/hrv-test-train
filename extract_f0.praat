form Extract_F0
    sentence InputFileName ""
    sentence OutputFileName ""
endform

# Read the audio file
Read from file... 'InputFileName$'
# Convert the sound to a pitch object with a fixed time step of 0.01 seconds and a pitch range of 75 to 600 Hz
To Pitch... 0 75 600
# Save pitch values directly to a text file
Write to text file... 'OutputFileName$'

#75 Hz to 600 Hz: This range is a common setting for human speech. It covers the typical fundamental frequency (f0) range for adult male and female speakers.
#Adult Males: Usually have a fundamental frequency ranging from about 75 Hz to 150 Hz.
#Adult Females: Usually have a fundamental frequency ranging from about 150 Hz to 300 Hz.
#Children and Other Variations: Can have frequencies up to 600 Hz or higher.