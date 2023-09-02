import cv2
import torch
from pathlib import Path
import requests  # Import the requests library for IP address lookup

# Function to get location information based on IP address
def get_location(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()
    return data

# Load the YOLOv5 model (you should have the YOLOv5 weights file, e.g., 'yolov5s.pt')
model = torch.hub.load('ultralytics/yolov5:master', 'yolov5s', pretrained=True)

# Set the device to 'cuda' if available, otherwise use 'cpu'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Initialize the USB camera (change the camera index if needed)
cap = cv2.VideoCapture(1)

# Create a directory to save detected spoon images (optional)
output_dir = Path("detected_spoons")
output_dir.mkdir(exist_ok=True)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Perform object detection
    results = model(frame)

    # Get the detected objects
    detected_objects = results.pred[0]

    for obj in detected_objects:
        class_idx = int(obj[-1])  # Get the class index
        if class_idx == 44:  
            x_center, y_center, width, height = obj[:4].cpu().numpy()
            x1 = int((x_center - width / 2) * frame.shape[1])
            y1 = int((y_center - height / 2) * frame.shape[0])
            x2 = int((x_center + width / 2) * frame.shape[1])
            y2 = int((y_center + height / 2) * frame.shape[0])

            # Read laptop's approximate location based on IP address
            public_ip = requests.get("https://api.ipify.org").text
            location_data = get_location(public_ip)

            # Print the laptop's approximate location
            print("Laptop Location:")
            print(f"Country: {location_data['country']}")
            print(f"Region: {location_data['regionName']}")
            print(f"City: {location_data['city']}")
            print(f"Latitude: {location_data['lat']}")
            print(f"Longitude: {location_data['lon']}")

            # Draw a rectangle around the detected spoon on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Save the coordinates of detected spoons
            coordinates = (x1, y1, x2, y2)

            # Do something with the coordinates (e.g., save to a list)
            print("Spoon detected at coordinates:", coordinates)

    # Display the frame with detected objects and laptop's location
    cv2.imshow('Object Detection', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
