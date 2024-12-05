import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    axios.get('http://localhost:5000/api/message_2')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('Error fetching message:', error);
      });
  }, []);

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h1>Fullstack Project Example</h1>
      <p>{message || 'Loading...'}</p>
    </div>
  );
};

export default App;
