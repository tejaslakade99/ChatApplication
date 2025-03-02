# Django Chat Application

A real-time chat application built using Django and Django Channels that supports multi-user chat rooms and a real-time view of online members. The application is configured to work seamlessly with the Daphne async server for handling WebSocket connections.

---

## Features

### 1. Real-Time Chat Room

- Members can join a chat room and send messages in real-time.
- Messages are broadcast to all participants in the room.
- Powered by Django Channels and WebSockets.

### 2. Online Members View

- Displays the list of members currently online.
- Updates in real-time as members join or leave the chat room.

---

## Technologies Used

- **Django**: Backend framework for handling requests and managing application logic.
- **Django Channels**: WebSocket integration for real-time communication.
- **Daphne**: ASGI server for asynchronous WebSocket handling.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/tejaslakade99/django-chat-application.git
cd django-chat-application
```

### 2. Set up a Virtual Environment

```bash
python3 -m venv venv
# For Mac: source venv/bin/activate
# For Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 7. Run the Application

```bash
python manage.py runserver
```

## Assumptions and Design Decisions

### 1. Real-Time Updates:

WebSockets are used to provide instant communication between clients.

### 2. Authentication:

Users are identified by unique session IDs; additional authentication can be implemented as needed.

### 3. Daphne Server:

While Django’s development server works for basic testing, Daphne is recommended for production.

## How to Test

1. Access the Application:
   Open your browser and navigate to: `http://127.0.0.1:8000`

2. Features to Test:
   - Join the chat room and send real-time messages.
   - Observe the online members view updating dynamically as users join/leave.

For a detailed walkthrough of the application and its features, please refer to the video provided in the repository.

## Screenshots

### Chat Room View

![Chat Room](https://github.com/tejaslakade99/tejaslakade99.github.io/blob/main/Github-Project-Images/Chat-Application/Active.png?raw=true)

### Online Members View

![Online Members](https://private-user-images.githubusercontent.com/69455769/397729930-2696ce39-a1ef-4069-8118-a15962b8a684.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ3NzI4NzMsIm5iZiI6MTczNDc3MjU3MywicGF0aCI6Ii82OTQ1NTc2OS8zOTc3Mjk5MzAtMjY5NmNlMzktYTFlZi00MDY5LTgxMTgtYTE1OTYyYjhhNjg0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjIxVDA5MTYxM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTY2NGNjNjA0NGU4NzgxNjAzMDA4YWUxOWQyZjVlMWU2MDQyYjMzNjRkMWQ4YTgzNTk3MWIwMjA0Y2JkMTIxYjEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.A5LJWv5-FNYN9GV8GJkBdeNp9xG2p1ppj9sy9qb5CyA)

### Application in Action

![App in Action](https://private-user-images.githubusercontent.com/69455769/397729933-3fe030f1-b65c-410d-aedd-f0269448937b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzQ3NzI4NzMsIm5iZiI6MTczNDc3MjU3MywicGF0aCI6Ii82OTQ1NTc2OS8zOTc3Mjk5MzMtM2ZlMDMwZjEtYjY1Yy00MTBkLWFlZGQtZjAyNjk0NDg5MzdiLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjIxVDA5MTYxM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWRjYTJmNTM2OTg0NzQ1NGEzNjAwMTlkNWFjODY5MDUwODZlYTQyMmUyMmJhMWViYTZkYzI5ZTg4ZTg1MTljMzEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.WEZ-pYxvWl2H5tISRg4SX5frFM6Ym2kQ-QR4nEKCHVk)
