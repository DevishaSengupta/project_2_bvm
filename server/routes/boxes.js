const express = require('express');
const router = express.Router();

// GET all boxes
router.get('/', (req, res) => {
  const pool = req.app.get('mysqlPool');
  pool.query('SELECT * FROM Boxes', (err, results) => {
    if (err) {
      console.error('MySQL error:', err);
      return res.status(500).json({ error: 'Database error' });
    }
    res.json(results);
  });
});

// POST add a new box
router.post('/', (req, res) => {
  const pool = req.app.get('mysqlPool');
  const { column_name, row_number } = req.body;
  if (!column_name || !row_number) {
    return res.status(400).json({ error: 'Missing column_name or row_number' });
  }
  pool.query(
    'INSERT INTO Boxes (column_name, row_number) VALUES (?, ?)',
    [column_name, row_number],
    (err, result) => {
      if (err) {
        console.error('MySQL error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      res.json({ id: result.insertId, column_name, row_number });
    }
  );
});

// DELETE a box by id
router.delete('/:id', (req, res) => {
  const pool = req.app.get('mysqlPool');
  const { id } = req.params;
  pool.query('DELETE FROM Boxes WHERE box_id = ?', [id], (err, result) => {
    if (err) {
      console.error('MySQL error:', err);
      return res.status(500).json({ error: 'Database error' });
    }
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Box not found' });
    }
    res.json({ success: true });
  });
});

module.exports = router; 