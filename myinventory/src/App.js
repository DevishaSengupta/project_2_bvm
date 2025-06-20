import React, { useState } from 'react';
import './App.css';
import BoxesTab from './BoxesTab';
import ItemsTab from './ItemsTab';
import SubCompartmentsTab from './SubCompartmentsTab';
import TransactionsTab from './TransactionsTab';
import OperationsTab from './OperationsTab';

const TABS = [
  'Boxes',
  'Items',
  'Sub Compartments',
  'Transactions',
  'Operations',
];

function App() {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Inventory Management System</h1>
        <div className="tabs">
          {TABS.map((tab, idx) => (
            <button
              key={tab}
              className={`tab-btn${activeTab === idx ? ' active' : ''}`}
              onClick={() => setActiveTab(idx)}
            >
              {tab}
            </button>
          ))}
        </div>
        <div className="tab-content">
          {activeTab === 0 && <BoxesTab />}
          {activeTab === 1 && <ItemsTab />}
          {activeTab === 2 && <SubCompartmentsTab />}
          {activeTab === 3 && <TransactionsTab />}
          {activeTab === 4 && <OperationsTab />}
        </div>
      </header>
    </div>
  );
}

export default App;
