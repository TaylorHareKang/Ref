import React, { useState } from 'react';
import './AddItem.css';

function AddItem() {
  const [newItem, setNewItem] = useState({
    name: '',
    expiryDate: '',
    quantity: 1
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // 여기에 아이템 추가 로직 구현
    console.log('새로운 아이템:', newItem);
  };

  return (
    <div className="add-item-container">
      <h2>새 물품 추가</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>물품명:</label>
          <input
            type="text"
            value={newItem.name}
            onChange={(e) => setNewItem({...newItem, name: e.target.value})}
          />
        </div>
        <div>
          <label>유통기한:</label>
          <input
            type="date"
            value={newItem.expiryDate}
            onChange={(e) => setNewItem({...newItem, expiryDate: e.target.value})}
          />
        </div>
        <div>
          <label>수량:</label>
          <input
            type="number"
            value={newItem.quantity}
            onChange={(e) => setNewItem({...newItem, quantity: parseInt(e.target.value)})}
          />
        </div>
        <button type="submit">추가하기</button>
      </form>
    </div>
  );
}

export default AddItem; 