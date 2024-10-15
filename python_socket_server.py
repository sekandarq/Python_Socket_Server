import os
import socket
from datetime import datetime

class SocketServer:
    def __init__(self):
        self.bufsize = 1024
        with open(r'C:\Users\USER\Desktop\KHU_Bachelor Degree in Computer Engineering\SEM 6 - KHU\Mobile_Web_Service_Project\Assignment_3\response.bin', 'rb') as file:
            self.RESPONSE = file.read()

        self.DIR_PATH = './request'
        self.IMAGE_PATH = './images'
        self.createDir(self.DIR_PATH)
        self.createDir(self.IMAGE_PATH)

    def createDir(self, path):
        """Create the directory if it doesn't exist."""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error: Failed to create the directory.")

    def saveRequestAsBinary(self, data):
        """Save client request data as a binary file."""
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file_path = os.path.join(self.DIR_PATH, f'{timestamp}.bin')

        with open(file_path, 'wb') as file:
            file.write(data)
        print(f"Saved client request to {file_path}")

    def saveImage(self, image_data):
        """Save the image data as a file."""
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        image_path = os.path.join(self.IMAGE_PATH, f'{timestamp}.jpg')

        with open(image_path, 'wb') as img_file:
            img_file.write(image_data)
        print(f"Saved image to {image_path}")

    def extractImageData(self, data):
        """Extract image data from multipart request."""
        boundary = b'--'
        parts = data.split(boundary)
        for part in parts:
            if b'Content-Type: image/' in part:
                image_data = part.split(b'\r\n\r\n')[1].strip()
                return image_data
        return None

    def run(self, ip, port):
        """Run the socket server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(10)
        print("Start the socket server...")
        print("\n[Ctrl+C] for stopping the server\n\n")

        try:
            while True:
                clnt_sock, req_addr = self.sock.accept()
                clnt_sock.settimeout(15.0)
                print("Request message...\n\n")

                response = b""
                try:
                    while True:
                        data = clnt_sock.recv(self.bufsize)
                        if not data:
                            break
                        response += data
                except socket.timeout:
                    print("Connection timed out while receiving data\n\n")

                # Debug print to show the received data
                print(f"Received data: {response}")

                # Save the received data as a binary file
                self.saveRequestAsBinary(response)

                # Extract image data if present and save it
                image_data = self.extractImageData(response)
                if image_data:
                    self.saveImage(image_data)

                # Send response back to the client
                print("Sending response to client...\n\n")

                clnt_sock.sendall(self.RESPONSE)
                print("Response sent to client successfully\n\n")

                clnt_sock.close()
        except KeyboardInterrupt:
            print("\n\nStop the server...")

        self.sock.close()

if __name__ == "__main__":
    server = SocketServer()
    server.run('127.0.0.1', 8000)
