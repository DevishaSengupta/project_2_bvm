// config.js
// NOTE: React apps cannot connect directly to MySQL. This config is for API endpoints or environment info only.

const MYSQL_CONFIG = {
  host: 'localhost',
  user: 'root',
  password: 'your_password',
  database: 'inventory',
  port: 3306,
};

// Example: API base URL for backend server
export const API_BASE_URL = 'http://localhost:5000/api';

export default MYSQL_CONFIG; 