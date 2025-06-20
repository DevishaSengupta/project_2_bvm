const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const { mysql: mysqlConfig } = require('./config');
const boxesRouter = require('./routes/boxes');
const itemsRouter = require('./routes/items');
const subcompartmentsRouter = require('./routes/subcompartments');
const transactionsRouter = require('./routes/transactions');
const operationsRouter = require('./routes/operations');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

// Create MySQL connection pool
const pool = mysql.createPool(mysqlConfig);
app.set('mysqlPool', pool);

// Use modular routers
app.use('/api/boxes', boxesRouter);
app.use('/api/items', itemsRouter);
app.use('/api/subcompartments', subcompartmentsRouter);
app.use('/api/transactions', transactionsRouter);
app.use('/api/operations', operationsRouter);

app.listen(PORT, () => {
  console.log(`Express server running on http://localhost:${PORT}`);
}); 