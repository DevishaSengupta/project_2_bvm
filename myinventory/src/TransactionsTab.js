import React, { useEffect, useState } from 'react';
import { API_BASE_URL } from './config';

function TransactionsTab() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ item: '', location: '', action: '' });
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState('');
  const [sort, setSort] = useState('asc');
  const [actionFilter, setActionFilter] = useState('');

  const fetchTransactions = () => {
    setLoading(true);
    let url = `${API_BASE_URL}/transactions?sort=${sort === 'newest' ? 'newest' : ''}`;
    if (actionFilter) url += `&action=${actionFilter}`;
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setTransactions(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchTransactions();
    // eslint-disable-next-line
  }, [sort, actionFilter]);

  const handleAdd = e => {
    e.preventDefault();
    setAdding(true);
    setError('');
    fetch(`${API_BASE_URL}/transactions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
      .then(res => {
        if (!res.ok) return res.json().then(data => { throw new Error(data.error || 'Add failed'); });
        return res.json();
      })
      .then(() => {
        setForm({ item: '', location: '', action: '' });
        fetchTransactions();
      })
      .catch(err => setError(err.message))
      .finally(() => setAdding(false));
  };

  const safeTransactions = Array.isArray(transactions) ? transactions : [];
  console.log('transactions:', transactions);

  return (
    <div>
      <form className="controls" onSubmit={handleAdd} style={{gap: 8}}>
        <input type="text" placeholder="Item" value={form.item} onChange={e => setForm(f => ({...f, item: e.target.value}))} required />
        <input type="text" placeholder="Location" value={form.location} onChange={e => setForm(f => ({...f, location: e.target.value}))} required />
        <input type="text" placeholder="Action" value={form.action} onChange={e => setForm(f => ({...f, action: e.target.value}))} required />
        <button type="submit" disabled={adding}>Add Transaction</button>
        <button type="button" onClick={fetchTransactions}>Refresh</button>
        {error && <span style={{color:'red',marginLeft:8}}>{error}</span>}
        <label style={{marginLeft: 20}}>Sort By:
          <select value={sort} onChange={e => setSort(e.target.value)}>
            <option value="asc">Transaction ID (asc)</option>
            <option value="newest">Newest First</option>
          </select>
        </label>
        <label style={{marginLeft: 20}}>
          <select value={actionFilter} onChange={e => setActionFilter(e.target.value)}>
            <option value="">All Actions</option>
            <option value="Added">Added Only</option>
            <option value="Retrieved">Retrieved Only</option>
          </select>
        </label>
      </form>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Transaction ID</th>
              <th>Item</th>
              <th>Location</th>
              <th>Action</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {safeTransactions.map(tr => (
              <tr key={tr.transaction_id}>
                <td>{tr.transaction_id}</td>
                <td>{tr.item}</td>
                <td>{tr.location}</td>
                <td>{tr.action}</td>
                <td>{tr.time ? tr.time.replace('T', ' ').substring(0, 16) : ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default TransactionsTab;

 