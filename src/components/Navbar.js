import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={{
      padding: '1rem',
      backgroundColor: '#f8f9fa',
      marginBottom: '20px'
    }}>
      <ul style={{
        listStyle: 'none',
        display: 'flex',
        gap: '20px',
        margin: 0,
        padding: 0
      }}>
        <li>
          <Link to="/">냉장고 보기</Link>
        </li>
        <li>
          <Link to="/add">물품 추가</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar; 