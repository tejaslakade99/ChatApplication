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

![Chat Room](https://github.com/user-attachments/assets/b3f824e6-ac2c-402b-84f0-af3329a8c932)

### Online Members View

![Online Members](https://github.com/user-attachments/assets/ecdfff4c-b5f4-4ecc-870e-dc616050c043)

### Application in Action

![App in Action](https://github.com/user-attachments/assets/f89c701c-bb0b-466f-b9b7-9d7d0f3e31a2)
