import React, {useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import './Hello.css';
import axios_instance from '../services/api';

function Hello() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        await axios_instance.post('/auth/logout', {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
    }
      navigate('/login');
    } finally {
      localStorage.removeItem('access_token');
    }
  };

  return (
    <div className="hello-container">
      <header className="hello-header">
        <button className="logout-button" onClick={handleLogout}>Logout</button>
        
      </header>
    </div>
  );
}

export default Hello;