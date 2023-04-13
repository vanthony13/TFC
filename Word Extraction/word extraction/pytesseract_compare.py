import os
import csv
import cv2
import pytesseract
from Levenshtein import distance
import matplotlib.pyplot as plt

# Set the path to the dataset
dataset_path = r"C:\Users\Vitoria\Desktop\TFC\mltu-main (copy)\Word Extraction\word extraction\Datasets\Testing"

# Create lists to store the CER values and the image filenames
cer_values = []
acc_values = []
image_filenames = []

# Configure the pytesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Loop over all the images in the dataset directory
for filename in os.listdir(dataset_path):
    if filename.endswith(".png"):
        # Load the image and convert it to grayscale
        image_path = os.path.join(dataset_path, filename)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use pytesseract to extract the text from the image
        text = pytesseract.image_to_string(gray).strip()

        # Get the label from the filename
        label = os.path.splitext(filename)[0]

        # Calculate the CER and append it to the list of CER values
        cer_value = distance(text, label) / max(len(text), len(label))
        cer_values.append(cer_value)

        # Calculate the accuracy and append it to the list of accuracy values
        accuracy = (1 - cer_value) * 100
        acc_values.append(accuracy)

        # Append the image filename to the list of image filenames
        image_filenames.append(filename)

# Calculate the average CER and accuracy
avg_cer = sum(cer_values) / len(cer_values)
avg_acc = sum(acc_values) / len(acc_values)

# Print the average CER and accuracy
print("\nAverage CER:", avg_cer)
print("\nAverage accuracy:", avg_acc)

# Write the CER values and image filenames to a CSV file
with open("cer_results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "CER"])
    for i in range(len(cer_values)):
        writer.writerow([image_filenames[i], cer_values[i]])

# Write the accuracy values and image filenames to a CSV file
with open("acc_results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "Accuracy"])
    for i in range(len(acc_values)):
        writer.writerow([image_filenames[i], acc_values[i]])

# Generate the CER graph
plt.plot(image_filenames, cer_values)
plt.title("Character Error Rate (CER) for pytesseract")
plt.xlabel("Image filename")
plt.xticks(rotation=90)
plt.ylabel("CER")
plt.tight_layout()
plt.savefig("cer_graph_pytesseract.png")
plt.show()

# Generate the accuracy graph
plt.plot(image_filenames, acc_values)
plt.title("Accuracy for pytesseract")
plt.xlabel("Image filename")
plt.xticks(rotation=90)
plt.ylabel("Accuracy")
plt.tight_layout()
plt.savefig("accuracy_graph_pytesseract.png")
plt.show()
