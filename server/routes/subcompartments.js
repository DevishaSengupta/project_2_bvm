const express = require('express');
const router = express.Router();

// GET all sub compartments
router.get('/', (req, res) => {
  const pool = req.app.get('mysqlPool');
  pool.query('SELECT * FROM SubCompartments', (err, results) => {
    if (err) {
      console.error('MySQL error:', err);
      return res.status(500).json({ error: 'Database error' });
    }
    res.json(results);
  });
});

// POST add a new sub compartment
router.post('/', (req, res) => {
  const pool = req.app.get('mysqlPool');
  const { place, box_id, sub_id, item_id, status } = req.body;
  if (!place || !box_id || !sub_id || !item_id || !status) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  pool.query(
    'INSERT INTO SubCompartments (place, box_id, sub_id, item_id, status) VALUES (?, ?, ?, ?, ?)',
    [place, box_id, sub_id, item_id, status],
    (err, result) => {
      if (err) {
        console.error('MySQL error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      res.json({ id: result.insertId, place, box_id, sub_id, item_id, status });
    }
  );
});

// PUT update status of a sub compartment
router.put('/:id', (req, res) => {
  const pool = req.app.get('mysqlPool');
  const { id } = req.params;
  const { status } = req.body;
  if (!status) {
    return res.status(400).json({ error: 'Missing status' });
  }
  pool.query(
    'UPDATE SubCompartments SET status = ? WHERE sub_id = ?',
    [status, id],
    (err, result) => {
      if (err) {
        console.error('MySQL error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      if (result.affectedRows === 0) {
        return res.status(404).json({ error: 'SubCompartment not found' });
      }
      res.json({ success: true });
    }
  );
});

module.exports = router; 