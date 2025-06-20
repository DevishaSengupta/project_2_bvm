const express = require('express');
const router = express.Router();

// POST add product (assign item to subcompartment)
router.post('/add-product', (req, res) => {
  const pool = req.app.get('mysqlPool');
  const { item_id, box_id, sub_id } = req.body;
  if (!item_id || !box_id || !sub_id) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  pool.query(
    'UPDATE SubCompartments SET item_id = ? WHERE box_id = ? AND sub_id = ?',
    [item_id, box_id, sub_id],
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

// POST retrieve product (remove item from subcompartment)
router.post('/retrieve-product', (req, res) => {
  const pool = req.app.get('mysqlPool');
  const { box_id, sub_id } = req.body;
  if (!box_id || !sub_id) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  pool.query(
    'UPDATE SubCompartments SET item_id = NULL WHERE box_id = ? AND sub_id = ?',
    [box_id, sub_id],
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

// GET item locations (where each item is stored)
router.get('/item-locations', (req, res) => {
  const pool = req.app.get('mysqlPool');
  pool.query(
    `SELECT i.item_id, i.name, 
            s.subcompartment_place AS place, 
            s.box_id, s.sub_id
     FROM Items i
     LEFT JOIN SubCompartments s ON i.item_id = s.item_id
     WHERE s.subcompartment_place IS NOT NULL`,
    (err, results) => {
      if (err) {
        console.error('MySQL error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      res.json(results);
    }
  );
});

module.exports = router;