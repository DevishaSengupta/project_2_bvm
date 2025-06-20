import React, { useEffect, useState } from 'react';
import { API_BASE_URL } from './config';

function SubCompartmentsTab() {
  const [subcomps, setSubcomps] = useState([]);
  const [boxes, setBoxes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ place: '', box_id: '', sub_id: '', item_id: '', status: '' });
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState('');
  const [statusUpdate, setStatusUpdate] = useState({});

  // Fetch boxes for mapping box_id to column_name and row_number
  const fetchBoxes = () => {
    fetch(`${API_BASE_URL}/boxes`)
      .then(res => res.json())
      .then(data => setBoxes(Array.isArray(data) ? data : []));
  };

  const fetchSubcomps = () => {
    setLoading(true);
    fetch(`${API_BASE_URL}/subcompartments`)
      .then(res => res.json())
      .then(data => {
        setSubcomps(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchBoxes();
    fetchSubcomps();
  }, []);

  const handleAdd = e => {
    e.preventDefault();
    setAdding(true);
    setError('');
    fetch(`${API_BASE_URL}/subcompartments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
      .then(res => {
        if (!res.ok) return res.json().then(data => { throw new Error(data.error || 'Add failed'); });
        return res.json();
      })
      .then(() => {
        setForm({ place: '', box_id: '', sub_id: '', item_id: '', status: '' });
        fetchSubcomps();
      })
      .catch(err => setError(err.message))
      .finally(() => setAdding(false));
  };

  const handleStatusUpdate = (sub_id, status) => {
    fetch(`${API_BASE_URL}/subcompartments/${sub_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    })
      .then(res => {
        if (!res.ok) return res.json().then(data => { throw new Error(data.error || 'Update failed'); });
        fetchSubcomps();
      })
      .catch(err => alert(err.message));
  };

  const safeSubcomps = Array.isArray(subcomps) ? subcomps : [];
  const boxMap = {};
  boxes.forEach(box => {
    boxMap[box.box_id] = box;
  });

  // Helper to get display value for Place column
  function getPlaceDisplay(sc) {
    const box = boxMap[sc.box_id];
    if (box && box.column_name && box.row_number && sc.sub_id) {
      return `${box.column_name}${box.row_number}${sc.sub_id}`;
    }
    return sc.place;
  }

  console.log('subcomps:', subcomps);

  return (
    <div>
      <form className="controls" onSubmit={handleAdd} style={{gap: 8}}>
        <input type="text" placeholder="Place" value={form.place} onChange={e => setForm(f => ({...f, place: e.target.value}))} required />
        <input type="number" placeholder="Box ID" value={form.box_id} onChange={e => setForm(f => ({...f, box_id: e.target.value}))} required />
        <input type="text" placeholder="Sub ID" value={form.sub_id} onChange={e => setForm(f => ({...f, sub_id: e.target.value}))} required />
        <input type="number" placeholder="Item ID" value={form.item_id} onChange={e => setForm(f => ({...f, item_id: e.target.value}))} required />
        <input type="text" placeholder="Status" value={form.status} onChange={e => setForm(f => ({...f, status: e.target.value}))} required />
        <button type="submit" disabled={adding}>Add SubCompartment</button>
        <button type="button" onClick={fetchSubcomps}>Refresh</button>
        {error && <span style={{color:'red',marginLeft:8}}>{error}</span>}
      </form>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Place</th>
              <th>Box ID</th>
              <th>Sub ID</th>
              <th>Item ID</th>
              <th>Status</th>
              <th>Update Status</th>
            </tr>
          </thead>
          <tbody>
            {safeSubcomps.map(sc => (
              <tr key={sc.sub_id}>
                <td>{getPlaceDisplay(sc)}</td>
                <td>{sc.box_id}</td>
                <td>{sc.sub_id}</td>
                <td>{sc.item_id}</td>
                <td>{sc.status}</td>
                <td>
                  <input
                    type="text"
                    placeholder="New Status"
                    value={statusUpdate[sc.sub_id] || ''}
                    onChange={e => setStatusUpdate(su => ({...su, [sc.sub_id]: e.target.value}))}
                    style={{width: 90}}
                  />
                  <button onClick={() => handleStatusUpdate(sc.sub_id, statusUpdate[sc.sub_id] || sc.status)} style={{marginLeft: 4}}>Update</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default SubCompartmentsTab; 