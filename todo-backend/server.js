require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const todoRoutes = require('./routes/todos');

const app = express();

// Enhanced CORS configuration
app.use(cors({
  origin: 'http://localhost:3000', // Your frontend URL
  methods: ['GET', 'POST', 'PATCH', 'DELETE'],
  credentials: true
}));

// Middleware
app.use(express.json());

// Request logging middleware
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
});

// Routes
app.use('/api/todos', todoRoutes);

// Enhanced MongoDB connection
mongoose.set('strictQuery', true); // Prepare for Mongoose 7 change

const connectWithRetry = () => {
  mongoose.connect(process.env.MONGO_URI)
    .then(() => {
      console.log('✅ Connected to MongoDB');
      
      // MongoDB event listeners
      mongoose.connection.on('connected', () => {
        console.log('Mongoose connected to DB');
      });
      
      mongoose.connection.on('error', (err) => {
        console.error('Mongoose connection error:', err);
      });
      
      mongoose.connection.on('disconnected', () => {
        console.log('Mongoose disconnected');
      });
    })
    .catch(err => {
      console.error('❌ MongoDB connection error:', err);
      console.log('Retrying connection in 5 seconds...');
      setTimeout(connectWithRetry, 5000);
    });
};

// Start connection
connectWithRetry();

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// Start server
const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});