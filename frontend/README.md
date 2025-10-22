# WhatsApp Chat Clone - Frontend

Modern WhatsApp-inspired chat application built with React.

## Features

### 🎨 Modern WhatsApp Chat UI
- Clean and intuitive interface matching WhatsApp's design language
- Responsive layout for desktop and mobile devices
- Real-time message updates
- Message bubbles with sender/receiver differentiation
- Typing indicators
- Online/offline status indicators
- Message timestamps and read receipts
- Emoji support

### 🔐 Authentication
- Secure user authentication and authorization
- JWT-based session management
- Login and registration pages
- Protected routes
- User profile management

### 💬 Chat Features
- One-on-one messaging
- Group chat support
- Message search functionality
- Chat history
- Media sharing (images, files)
- Voice message support
- Message reactions

### 👥 User Management
- Contact list
- User search
- Profile pictures
- Status updates
- Last seen information

## Tech Stack

- **React** - Frontend framework
- **React Router** - Navigation and routing
- **Socket.io Client** - Real-time bidirectional communication
- **Axios** - HTTP client for API requests
- **Material-UI / Styled Components** - UI components and styling
- **Redux / Context API** - State management
- **Formik / React Hook Form** - Form handling
- **Yup** - Form validation

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Chat/
│   │   ├── Sidebar/
│   │   ├── Auth/
│   │   └── Common/
│   ├── pages/
│   │   ├── Login.js
│   │   ├── Register.js
│   │   ├── Chat.js
│   │   └── Profile.js
│   ├── services/
│   │   ├── api.js
│   │   └── socket.js
│   ├── store/
│   │   ├── actions/
│   │   ├── reducers/
│   │   └── store.js
│   ├── utils/
│   ├── App.js
│   └── index.js
├── package.json
└── README.md
```

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### Environment Variables

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_SOCKET_URL=http://localhost:5000
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT
