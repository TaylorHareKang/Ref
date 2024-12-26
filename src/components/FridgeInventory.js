import React, { useState } from 'react';
import './FridgeInventory.css';

function FridgeInventory() {
  const [items, setItems] = useState([
    { id: 1, name: '우유', expiryDate: '2024-03-25', quantity: 1 },
    { id: 2, name: '계란', expiryDate: '2024-03-30', quantity: 12 },
  ]);

  const deleteItem = (id) => {
    setItems(items.filter(item => item.id !== id));
  };

  return (
    <div className="inventory-container">
      <h2>냉장고 내용물</h2>
      <div className="inventory-list">
        {items.map(item => (
          <div key={item.id} className="inventory-item">
            <h3>{item.name}</h3>
            <p>유통기한: {item.expiryDate}</p>
            <p>수량: {item.quantity}</p>
            <button onClick={() => deleteItem(item.id)}>삭제</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default FridgeInventory; 