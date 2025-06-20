import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from './config';

function OperationsTab() {
  const [mode, setMode] = useState('add'); // 'add' or 'retrieve'
  const [items, setItems] = useState([]);
  const [boxes, setBoxes] = useState([]);
  const [availableProducts, setAvailableProducts] = useState([]);
  const [addForm, setAddForm] = useState({ item_id: '', box_id: '', sub_id: '' });
  const [retrieveForm, setRetrieveForm] = useState({ item_id: '', quantity: 1 });
  const [result, setResult] = useState('');
  const [showLocations, setShowLocations] = useState(false);
  const [locations, setLocations] = useState([]);
  const [locationsLoading, setLocationsLoading] = useState(false);

  // Fetch items and boxes for Add Product
  useEffect(() => {
    fetch(`${API_BASE_URL}/items`)
      .then(res => res.json())
      .then(data => setItems(Array.isArray(data) ? data : []));
    fetch(`${API_BASE_URL}/boxes`)
      .then(res => res.json())
      .then(data => setBoxes(Array.isArray(data) ? data : []));
  }, []);

  // Fetch available products for retrieval
  useEffect(() => {
    if (mode === 'retrieve') {
      fetch(`${API_BASE_URL}/operations/item-locations`)
        .then(res => res.json())
        .then(data => {
          // Count available by item_id
          const counts = {};
          (Array.isArray(data) ? data : []).forEach(row => {
            if (row.item_id) {
              counts[row.item_id] = (counts[row.item_id] || 0) + 1;
            }
          });
          // Join with item names
          fetch(`${API_BASE_URL}/items`)
            .then(res => res.json())
            .then(itemsData => {
              const itemsArr = Array.isArray(itemsData) ? itemsData : [];
              setAvailableProducts(
                itemsArr
                  .filter(item => counts[item.item_id])
                  .map(item => ({
                    item_id: item.item_id,
                    name: item.name,
                    available: counts[item.item_id] || 0,
                  }))
              );
            });
        });
    }
  }, [mode]);

  // Add Product handler
  const handleAddProduct = e => {
    e.preventDefault();
    setResult('');
    fetch(`${API_BASE_URL}/operations/add-product`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        item_id: addForm.item_id,
        box_id: addForm.box_id,
        sub_id: addForm.sub_id,
        place: '',
      })
    })
      .then(res => res.json())
      .then(data => setResult(data.success ? 'Product added.' : (data.error || 'Error')))
      .catch(() => setResult('Error'));
  };

  // Retrieve Product handler
  const handleRetrieveProduct = e => {
    e.preventDefault();
    setResult('');
    fetch(`${API_BASE_URL}/operations/retrieve-product`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        item_id: retrieveForm.item_id,
        quantity: retrieveForm.quantity,
      })
    })
      .then(res => res.json())
      .then(data => setResult(data.success ? 'Product retrieved.' : (data.error || 'Error')))
      .catch(() => setResult('Error'));
  };

  // View Item Locations handler
  const handleViewLocations = () => {
    if (showLocations) {
      setShowLocations(false);
      return;
    }
    setLocationsLoading(true);
    fetch(`${API_BASE_URL}/operations/item-locations`)
      .then(res => res.json())
      .then(data => {
        setLocations(Array.isArray(data) ? data : []);
        setShowLocations(true);
        setLocationsLoading(false);
      })
      .catch(() => {
        setLocations([]);
        setShowLocations(true);
        setLocationsLoading(false);
      });
  };

  return (
    <div>
      <div className="controls">
        <button
          style={{ background: mode === 'add' ? '#1976d2' : '#888', color: '#fff' }}
          onClick={() => setMode('add')}
        >
          Add Product
        </button>
        <button
          style={{ background: mode === 'retrieve' ? '#1976d2' : '#888', color: '#fff' }}
          onClick={() => setMode('retrieve')}
        >
          Retrieve Product
        </button>
        <button
          style={{ background: showLocations ? '#1976d2' : '#888', color: '#fff', marginLeft: 10 }}
          onClick={handleViewLocations}
        >
          View Item Locations
        </button>
      </div>
      <div className="dynamic-content" style={{ marginTop: 20 }}>
        {mode === 'add' && (
          <form onSubmit={handleAddProduct} style={{ gap: 8, display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <span style={{ color: '#111', fontWeight: 'bold' }}>Select Product Type:</span>
            {items.length === 0 && <span style={{ color: '#888' }}>No products available. Add items first in Items tab.</span>}
            {items.map(item => (
              <label key={item.item_id} style={{ marginLeft: 12 }}>
                <input
                  type="radio"
                  name="add_item_id"
                  value={item.item_id}
                  checked={addForm.item_id === String(item.item_id)}
                  onChange={e => setAddForm(f => ({ ...f, item_id: e.target.value }))}
                  required
                />{' '}
                {item.name} (ID: {item.item_id})
              </label>
            ))}
            <div style={{ marginTop: 10 }}>
              <label style={{ marginRight: 8 }}>Box ID:</label>
              <select
                value={addForm.box_id}
                onChange={e => setAddForm(f => ({ ...f, box_id: e.target.value }))}
                required
              >
                <option value="">Select Box</option>
                {boxes.map(box => (
                  <option key={box.box_id} value={box.box_id}>
                    {box.box_id}
                  </option>
                ))}
              </select>
            </div>
            <div style={{ marginTop: 10 }}>
              <label style={{ marginRight: 8 }}>Sub Compartment ID:</label>
              <input
                type="text"
                value={addForm.sub_id}
                onChange={e => setAddForm(f => ({ ...f, sub_id: e.target.value }))}
                required
                style={{ width: 120 }}
              />
            </div>
            <button type="submit" style={{ marginTop: 12 }}>Add Product to Storage</button>
          </form>
        )}
        {mode === 'retrieve' && (
          <form onSubmit={handleRetrieveProduct} style={{ gap: 8, display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <span style={{ color: '#111', fontWeight: 'bold' }}>Select Product Type to Retrieve:</span>
            {availableProducts.length === 0 && <span style={{ color: '#888' }}>No products available for retrieval.</span>}
            {availableProducts.map((prod, idx) => (
              <label key={prod.item_id} style={{ marginLeft: 12 }}>
                <input
                  type="radio"
                  name="retrieve_item_id"
                  value={prod.item_id}
                  checked={retrieveForm.item_id === String(prod.item_id) || (retrieveForm.item_id === '' && idx === 0)}
                  onChange={e => setRetrieveForm(f => ({ ...f, item_id: e.target.value }))}
                  required
                />{' '}
                {prod.name} (Available: {prod.available})
              </label>
            ))}
            <div style={{ marginTop: 10 }}>
              <label style={{ marginRight: 8 }}>Quantity to Retrieve:</label>
              <input
                type="number"
                min={1}
                value={retrieveForm.quantity}
                onChange={e => setRetrieveForm(f => ({ ...f, quantity: e.target.value }))}
                required
                style={{ width: 80 }}
              />
            </div>
            <button type="submit" style={{ marginTop: 12 }}>Retrieve Product</button>
          </form>
        )}
      </div>
      <div className="results" style={{ marginTop: 20 }}>
        {result && <p>{result}</p>}
        {showLocations && (
          locationsLoading ? (
            <p>Loading item locations...</p>
          ) : locations.length > 0 ? (
            <table className="data-table" style={{ marginTop: 20 }}>
              <thead>
                <tr>
                  <th>Item ID</th>
                  <th>Name</th>
                  <th>Place</th>
                  <th>Box ID</th>
                  <th>Sub ID</th>
                </tr>
              </thead>
              <tbody>
                {locations.map(loc => (
                  <tr key={loc.item_id + '-' + (loc.sub_id || '')}>
                    <td>{loc.item_id}</td>
                    <td>{loc.name}</td>
                    <td>{loc.place}</td>
                    <td>{loc.box_id}</td>
                    <td>{loc.sub_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No item locations found.</p>
          )
        )}
      </div>
    </div>
  );
}

export default OperationsTab; 