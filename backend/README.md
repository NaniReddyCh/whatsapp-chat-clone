# WhatsApp Chat Clone - Backend

## Overview
This is the backend API for the WhatsApp Chat Clone application, built with FastAPI and MongoDB. It provides a robust and scalable REST API with real-time messaging capabilities.

## Features

### 🔐 Authentication & Authorization
- **User Registration**: Secure user registration with email and password
- **JWT Authentication**: Token-based authentication using JSON Web Tokens
- **Password Hashing**: Secure password storage using bcrypt
- **Login/Logout**: Complete authentication flow with token management
- **Protected Routes**: Middleware-based route protection

### 💬 Chat Management
- **Create Chats**: Create private and group chats
- **Get User Chats**: Retrieve all chats for authenticated user
- **Chat Details**: Get specific chat information
- **Delete Chats**: Remove chat conversations
- **Last Message Tracking**: Track and display last message in each chat

### 📨 Real-time Messaging
- **Send Messages**: Send text, image, video, and file messages
- **Message History**: Retrieve chat message history with pagination
- **Read Receipts**: Mark messages as read
- **Message Types**: Support for multiple message types (text, image, video, file)
- **Real-time Updates**: WebSocket support for instant message delivery

### 👥 User Management
- **User Profiles**: View and update user profiles
- **User Search**: Search users by username, email, or full name
- **Status Updates**: Update user online/offline status
- **Avatar Management**: Profile picture support
- **Account Deletion**: Complete account removal with data cleanup

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Motor**: Async MongoDB driver for Python
- **PyMongo**: MongoDB driver for Python
- **Python-JOSE**: JSON Web Token implementation
- **Passlib**: Password hashing library
- **Pydantic**: Data validation using Python type annotations
- **Python-SocketIO**: WebSocket support for real-time features
- **Uvicorn**: ASGI server for running FastAPI

## MongoDB Configuration

### Database Structure

#### Collections:
1. **users**: Store user information
   - username, email, password (hashed), full_name, avatar, status, bio
   - created_at, updated_at timestamps

2. **chats**: Store chat conversations
   - participants (array of user IDs)
   - chat_type (private/group)
   - group_name, group_avatar (for group chats)
   - last_message, last_message_time
   - created_at, updated_at timestamps

3. **messages**: Store individual messages
   - content, sender_id, receiver_id, chat_id
   - message_type (text/image/video/file)
   - is_read status
   - created_at, updated_at timestamps

### Environment Variables

Create a `.env` file in the backend directory with the following:

```env
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=your-secret-key-here
```

## Installation & Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MongoDB**:
   - Install MongoDB locally or use MongoDB Atlas
   - Update the `MONGODB_URL` in `.env` file

3. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/auth`)
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info
- `POST /auth/logout` - Logout user

### Chats (`/chats`)
- `POST /chats/` - Create new chat
- `GET /chats/` - Get all user chats
- `GET /chats/{chat_id}` - Get specific chat
- `DELETE /chats/{chat_id}` - Delete chat
- `POST /chats/{chat_id}/messages` - Send message
- `GET /chats/{chat_id}/messages` - Get chat messages
- `PUT /chats/{chat_id}/messages/{message_id}/read` - Mark message as read

### Users (`/users`)
- `GET /users/` - Get all users (paginated)
- `GET /users/{user_id}` - Get specific user
- `GET /users/search/{query}` - Search users
- `PUT /users/me` - Update user profile
- `PUT /users/me/status` - Update user status
- `DELETE /users/me` - Delete user account

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic models for data validation
├── routes/
│   ├── auth.py         # Authentication routes
│   ├── chat.py         # Chat and messaging routes
│   └── user.py         # User management routes
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
