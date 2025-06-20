const express = require('express');
const router = express.Router();

// GET all items
router.get('/', (req, res) => {
  const pool = req.app.get('mysqlPool');
  pool.query('SELECT * FROM Items', (err, results) => {
    if (err) {
      console.error('MySQL error:', err);
      return res.status(500).json({ error: 'Database error' });
    }
    res.json(results);
  });
});

// POST add a new item
router.post('/', (req, res) => {
  const pool = req.app.get('mysqlPool');
  const { name, description } = req.body;
  if (!name) {
    return res.status(400).json({ error: 'Missing name' });
  }
  pool.query(
    'INSERT INTO Items (name, description, added_on) VALUES (?, ?, NOW())',
    [name, description || ''],
    (err, result) => {
      if (err) {
        console.error('MySQL error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      res.json({ id: result.insertId, name, description });
    }
  );
});

// DELETE an item by id
router.delete('/:id', (req, res) => {
  const pool = req.app.get('mysqlPool');
  const { id } = req.params;
  pool.query('DELETE FROM Items WHERE item_id = ?', [id], (err, result) => {
    if (err) {
      console.error('MySQL error:', err);
      return res.status(500).json({ error: 'Database error' });
    }
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Item not found' });
    }
    res.json({ success: true });
  });
});

module.exports = router; 