import React, { useEffect, useState } from 'react';
import { API_BASE_URL } from './config';

function BoxesTab() {
  const [boxes, setBoxes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [columnName, setColumnName] = useState('');
  const [rowNumber, setRowNumber] = useState('');
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState('');

  // Fetch boxes from backend
  const fetchBoxes = () => {
    setLoading(true);
    fetch(`${API_BASE_URL}/boxes`)
      .then(res => res.json())
      .then(data => {
        setBoxes(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchBoxes();
  }, []);

  // Add box
  const handleAddBox = e => {
    e.preventDefault();
    setAdding(true);
    setError('');
    fetch(`${API_BASE_URL}/boxes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ column_name: columnName, row_number: rowNumber })
    })
      .then(res => {
        if (!res.ok) return res.json().then(data => { throw new Error(data.error || 'Add failed'); });
        return res.json();
      })
      .then(() => {
        setColumnName('');
        setRowNumber('');
        fetchBoxes();
      })
      .catch(err => setError(err.message))
      .finally(() => setAdding(false));
  };

  // Delete box
  const handleDelete = id => {
    if (!window.confirm('Delete this box?')) return;
    fetch(`${API_BASE_URL}/boxes/${id}`, { method: 'DELETE' })
      .then(res => {
        if (!res.ok) return res.json().then(data => { throw new Error(data.error || 'Delete failed'); });
        fetchBoxes();
      })
      .catch(err => alert(err.message));
  };

  const safeBoxes = Array.isArray(boxes) ? boxes : [];
  console.log('boxes:', boxes);

  return (
    <div>
      <form className="controls" onSubmit={handleAddBox} style={{gap: 8}}>
        <input
          type="text"
          placeholder="Column Name"
          value={columnName}
          onChange={e => setColumnName(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Row Number"
          value={rowNumber}
          onChange={e => setRowNumber(e.target.value)}
          required
        />
        <button type="submit" disabled={adding}>Add Box</button>
        <button type="button" onClick={fetchBoxes}>Refresh</button>
        {error && <span style={{color:'red',marginLeft:8}}>{error}</span>}
      </form>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Box ID</th>
              <th>Column Name</th>
              <th>Row Number</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {safeBoxes.map(box => (
              <tr key={box.box_id}>
                <td>{box.box_id}</td>
                <td>{box.column_name}</td>
                <td>{box.row_number}</td>
                <td>
                  <button onClick={() => handleDelete(box.box_id)} style={{background:'#d32f2f'}}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default BoxesTab; 