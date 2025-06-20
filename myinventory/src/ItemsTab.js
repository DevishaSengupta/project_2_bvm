import React, { useEffect, useState } from 'react';
import { API_BASE_URL } from './config';

function ItemsTab() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState('');

  const fetchItems = () => {
    setLoading(true);
    fetch(`${API_BASE_URL}/items`)
      .then(res => res.json())
      .then(data => {
        setItems(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleAddItem = e => {
    e.preventDefault();
    setAdding(true);
    setError('');
    fetch(`${API_BASE_URL}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description })
    })
      .then(res => {
        if (!res.ok) return res.json().then(data => { throw new Error(data.error || 'Add failed'); });
        return res.json();
      })
      .then(() => {
        setName('');
        setDescription('');
        fetchItems();
      })
      .catch(err => setError(err.message))
      .finally(() => setAdding(false));
  };

  const handleDelete = id => {
    if (!window.confirm('Delete this item?')) return;
    fetch(`${API_BASE_URL}/items/${id}`, { method: 'DELETE' })
      .then(res => {
        if (!res.ok) return res.json().then(data => { throw new Error(data.error || 'Delete failed'); });
        fetchItems();
      })
      .catch(err => alert(err.message));
  };

  const safeItems = Array.isArray(items) ? items : [];
  console.log('items:', items);

  return (
    <div>
      <form className="controls" onSubmit={handleAddItem} style={{gap: 8}}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={e => setDescription(e.target.value)}
        />
        <button type="submit" disabled={adding}>Add Item</button>
        <button type="button" onClick={fetchItems}>Refresh</button>
        {error && <span style={{color:'red',marginLeft:8}}>{error}</span>}
      </form>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Item ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Added On</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {safeItems.map(item => (
              <tr key={item.item_id}>
                <td>{item.item_id}</td>
                <td>{item.name}</td>
                <td>{item.description}</td>
                <td>{item.added_on ? item.added_on.substring(0, 10) : ''}</td>
                <td>
                  <button onClick={() => handleDelete(item.item_id)} style={{background:'#d32f2f'}}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ItemsTab; 