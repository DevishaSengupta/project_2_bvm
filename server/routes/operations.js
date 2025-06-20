const express = require('express');
const router = express.Router();

// POST add product (assign item to subcompartment)
router.post('/add-product', (req, res) => {
  const pool = req.app.get('mysqlPool');
  const { item_id, box_id, sub_id } = req.body;
  if (!item_id || !box_id || !sub_id) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  // First, update the subcompartment and set status to 'Occupied'
  pool.query(
    'UPDATE SubCompartments SET item_id = ?, status = ? WHERE box_id = ? AND sub_id = ?',
    [item_id, 'Occupied', box_id, sub_id],
    (err, result) => { 
      if (err) {
        console.error('MySQL error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      if (result.affectedRows === 0) {
        return res.status(404).json({ error: 'SubCompartment not found' });
      }
      // Get the subcom_place for the transaction
      pool.query(
        'SELECT subcom_place FROM SubCompartments WHERE box_id = ? AND sub_id = ?',
        [box_id, sub_id],
        (err2, rows) => {
          if (err2 || !rows || rows.length === 0) {
            return res.json({ success: true, warning: 'Product added, but could not log transaction (place not found).' });
          }
          const subcom_place = rows[0].subcom_place;
          // Insert transaction (action should be 'added' lowercase)
          pool.query(
            'INSERT INTO Transactions (item_id, subcom_place, action, timestamp) VALUES (?, ?, ?, NOW())',
            [item_id, subcom_place, 'added'],
            (err3) => {
              if (err3) {
                console.error('MySQL error:', err3);
                return res.json({ success: true, warning: 'Product added, but could not log transaction.' });
              }
              res.json({ success: true });
            }
          );
        }
      );
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
  // Get item_id and subcom_place before removing
  pool.query(
    'SELECT item_id, subcom_place FROM SubCompartments WHERE box_id = ? AND sub_id = ?',
    [box_id, sub_id],
    (err, rows) => {
      if (err || !rows || rows.length === 0) {
        return res.status(404).json({ error: 'SubCompartment not found' });
      }
      const { item_id, subcom_place } = rows[0];
      if (!item_id) {
        return res.status(400).json({ error: 'No product to retrieve in this subcompartment.' });
      }
      // Remove the item and set status to 'Empty'
      pool.query(
        'UPDATE SubCompartments SET item_id = NULL, status = ? WHERE box_id = ? AND sub_id = ?',
        ['Empty', box_id, sub_id],
        (err2, result) => {
          if (err2) {
            console.error('MySQL error:', err2);
            return res.status(500).json({ error: 'Database error' });
          }
          if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'SubCompartment not found' });
          }
          // Insert transaction (action should be 'retrieved' lowercase)
          pool.query(
            'INSERT INTO Transactions (item_id, subcom_place, action, timestamp) VALUES (?, ?, ?, NOW())',
            [item_id, subcom_place, 'retrieved'],
            (err3) => {
              if (err3) {
                console.error('MySQL error:', err3);
                return res.json({ success: true, warning: 'Product retrieved, but could not log transaction.' });
              }
              res.json({ success: true });
            }
          );
        }
      );
    }
  );
});

// GET item locations (where each item is stored)
router.get('/item-locations', (req, res) => {
  const pool = req.app.get('mysqlPool');
  pool.query(
    `SELECT i.item_id, i.name, 
            s.subcom_place AS place, 
            s.box_id, s.sub_id
     FROM Items i
     LEFT JOIN SubCompartments s ON i.item_id = s.item_id
     WHERE s.subcom_place IS NOT NULL`,
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