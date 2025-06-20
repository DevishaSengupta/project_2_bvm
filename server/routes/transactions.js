const express = require('express');
const router = express.Router();

// GET all transactions (with optional filters)
router.get('/', (req, res) => {
  const pool = req.app.get('mysqlPool');
  let query = 'SELECT * FROM Transactions';
  const { sort, action } = req.query;
  const params = [];

  if (action) {
    query += ' WHERE action = ?';
    params.push(action);
  }
  if (sort === 'newest') {
    query += ' ORDER BY time DESC';
  } else {
    query += ' ORDER BY transaction_id ASC';
  }

  pool.query(query, params, (err, results) => {
    if (err) {
      console.error('MySQL error:', err);
      return res.status(500).json({ error: 'Database error' });
    }
    res.json(results);
  });
});

// POST add a new transaction
router.post('/', (req, res) => {
  const pool = req.app.get('mysqlPool');
  const { item, location, action } = req.body;
  if (!item || !location || !action) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  pool.query(
    'INSERT INTO Transactions (item, location, action, time) VALUES (?, ?, ?, NOW())',
    [item, location, action],
    (err, result) => {
      if (err) {
        console.error('MySQL error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      res.json({ id: result.insertId, item, location, action });
    }
  );
});

module.exports = router; 