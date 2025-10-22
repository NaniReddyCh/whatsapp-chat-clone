import { io } from 'socket.io-client';

// Socket.IO client configuration
const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:8000';

class SocketService {
  constructor() {
    this.socket = null;
    this.connected = false;
  }

  /**
   * Initialize and connect to Socket.IO server
   */
  connect() {
    if (this.socket && this.connected) {
      console.log('Socket already connected');
      return this.socket;
    }

    this.socket = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    this.socket.on('connect', () => {
      console.log('Connected to Socket.IO server:', this.socket.id);
      this.connected = true;
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from Socket.IO server');
      this.connected = false;
    });

    this.socket.on('connect_error', (error) => {
      console.error('Connection error:', error);
    });

    this.socket.on('connection_established', (data) => {
      console.log('Connection established:', data);
    });

    return this.socket;
  }

  /**
   * Disconnect from Socket.IO server
   */
  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.connected = false;
      console.log('Socket disconnected');
    }
  }

  /**
   * Emit user online event
   * @param {Object} userData - User data {user_id, username}
   */
  emitUserOnline(userData) {
    if (this.socket && this.connected) {
      this.socket.emit('user_online', userData);
      console.log('User online event emitted:', userData);
    } else {
      console.warn('Socket not connected. Cannot emit user_online event');
    }
  }

  /**
   * Emit user offline event
   * @param {Object} userData - User data {user_id}
   */
  emitUserOffline(userData) {
    if (this.socket && this.connected) {
      this.socket.emit('user_offline', userData);
      console.log('User offline event emitted:', userData);
    }
  }

  /**
   * Send a message
   * @param {Object} messageData - Message data {sender_id, receiver_id, message, timestamp}
   */
  sendMessage(messageData) {
    if (this.socket && this.connected) {
      this.socket.emit('send_message', messageData);
      console.log('Message sent:', messageData);
    } else {
      console.warn('Socket not connected. Cannot send message');
    }
  }

  /**
   * Listen for incoming messages
   * @param {Function} callback - Callback function to handle received message
   */
  onReceiveMessage(callback) {
    if (this.socket) {
      this.socket.on('receive_message', (data) => {
        console.log('Message received:', data);
        callback(data);
      });
    }
  }

  /**
   * Listen for message sent confirmation
   * @param {Function} callback - Callback function to handle confirmation
   */
  onMessageSent(callback) {
    if (this.socket) {
      this.socket.on('message_sent', (data) => {
        console.log('Message sent confirmation:', data);
        callback(data);
      });
    }
  }

  /**
   * Listen for message errors
   * @param {Function} callback - Callback function to handle errors
   */
  onMessageError(callback) {
    if (this.socket) {
      this.socket.on('message_error', (data) => {
        console.error('Message error:', data);
        callback(data);
      });
    }
  }

  /**
   * Listen for user online events
   * @param {Function} callback - Callback function to handle user online event
   */
  onUserOnline(callback) {
    if (this.socket) {
      this.socket.on('user_online', (data) => {
        console.log('User came online:', data);
        callback(data);
      });
    }
  }

  /**
   * Listen for user offline events
   * @param {Function} callback - Callback function to handle user offline event
   */
  onUserOffline(callback) {
    if (this.socket) {
      this.socket.on('user_offline', (data) => {
        console.log('User went offline:', data);
        callback(data);
      });
    }
  }

  /**
   * Emit typing indicator
   * @param {Object} typingData - Typing data {sender_id, receiver_id, is_typing}
   */
  emitTyping(typingData) {
    if (this.socket && this.connected) {
      this.socket.emit('typing', typingData);
    }
  }

  /**
   * Listen for typing events
   * @param {Function} callback - Callback function to handle typing event
   */
  onTyping(callback) {
    if (this.socket) {
      this.socket.on('typing', (data) => {
        callback(data);
      });
    }
  }

  /**
   * Emit message read receipt
   * @param {Object} readData - Read data {message_id, reader_id}
   */
  emitMessageRead(readData) {
    if (this.socket && this.connected) {
      this.socket.emit('message_read', readData);
    }
  }

  /**
   * Listen for message read events
   * @param {Function} callback - Callback function to handle message read event
   */
  onMessageRead(callback) {
    if (this.socket) {
      this.socket.on('message_read', (data) => {
        callback(data);
      });
    }
  }

  /**
   * Remove all event listeners
   */
  removeAllListeners() {
    if (this.socket) {
      this.socket.removeAllListeners();
    }
  }

  /**
   * Check if socket is connected
   * @returns {boolean}
   */
  isConnected() {
    return this.connected && this.socket && this.socket.connected;
  }
}

// Create and export a singleton instance
const socketService = new SocketService();
export default socketService;
