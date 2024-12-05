import React, { } from 'react';
import StratagemHell from './components/StratagemHell/StratagemHell';

const App: React.FC = () => {
  // const [message, setMessage] = useState<string>('');

  // useEffect(() => {
  //   axios.get('http://localhost:5000/api/message_2')
  //     .then(response => {
  //       setMessage(response.data.message);
  //     })
  //     .catch(error => {
  //       console.error('Error fetching message:', error);
  //     });
  // }, []);

  return (
    <StratagemHell />
  );
};

export default App;
