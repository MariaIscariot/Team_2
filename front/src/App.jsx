import { useState } from 'react';
import Subjects from './components/Subjects/Subjects';
import MainBody from './components/MainBody/MainBody';
import './App.css';

function App() {
  const [selectedMessage, setSelectedMessage] = useState(null);

  return (
    <div className="app">
      <Subjects onSelectMessage={setSelectedMessage} />
      <MainBody message={selectedMessage} />
    </div>
  );
}

export default App;
