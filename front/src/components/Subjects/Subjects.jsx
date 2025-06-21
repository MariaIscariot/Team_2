import { useState, useEffect } from 'react';
import styles from './index.module.css';
import MessageItem from './Subcomponents/MessageItem.jsx';

const messages = [
  { sender: 'FAF', subject: 'Summer FAF x Sigmoid', time: 'Чт, 14:49' },
  { sender: 'Turcan Ana', subject: 'UTM Bioinformatics board', time: 'Чт, 13:55' },
  { sender: 'UTM DTIC', subject: 'Autorizare SIMU Student', time: 'Ср, 17:06' },
  { sender: 'Istrati Daniela', subject: 'Sesiunea de reexaminare', time: 'Ср, 11:34' },
  { sender: 'No-reply Moodle UTM', subject: 'Вы отправили свой отчет', time: '17.06, Вт' },
  { sender: 'Bagrin Veronica', subject: 'Important', time: '17.06, Вт' },
  { sender: 'FAF', subject: 'Summer FAF x Sigmoid', time: 'Чт, 14:49' },
  { sender: 'Turcan Ana', subject: 'UTM Bioinformatics board', time: 'Чт, 13:55' },
  { sender: 'UTM DTIC', subject: 'Autorizare SIMU Student', time: 'Ср, 17:06' },
  { sender: 'Istrati Daniela', subject: 'Sesiunea de reexaminare', time: 'Ср, 11:34' },
  { sender: 'No-reply Moodle UTM', subject: 'Вы отправили свой отчет', time: '17.06, Вт' },
  { sender: 'Bagrin Veronica', subject: 'Important', time: '17.06, Вт' },
  { sender: 'FAF', subject: 'Summer FAF x Sigmoid', time: 'Чт, 14:49' },
  { sender: 'Turcan Ana', subject: 'UTM Bioinformatics board', time: 'Чт, 13:55' },
  { sender: 'UTM DTIC', subject: 'Autorizare SIMU Student', time: 'Ср, 17:06' },
  { sender: 'Istrati Daniela', subject: 'Sesiunea de reexaminare', time: 'Ср, 11:34' },
  { sender: 'No-reply Moodle UTM', subject: 'Вы отправили свой отчет', time: '17.06, Вт' },
  { sender: 'Bagrin Veronica', subject: 'Important', time: '17.06, Вт' },
];

export default function Subjects({ onSelectMessage }) {
  const [selectedIndex, setSelectedIndex] = useState(null);

  return (
    <div className={styles.wrapper}>
      <div className={styles.head}><h1>Subjects</h1></div>
      <div className={styles.line}></div>
      <ul className={styles.list}>
        {messages.map((msg, index) => (
          <MessageItem
            key={index}
            sender={msg.sender}
            subject={msg.subject}
            time={msg.time}
            selected={selectedIndex === index}
            onClick={() => {
              setSelectedIndex(index);
              onSelectMessage(msg);
            }}
          />
        ))}
      </ul>
    </div>
  );
}


/* 
const [messages, setMessages] = useState([]);

useEffect(() => {
  fetch('http://localhost:3000/api/messages')  
    .then(res => res.json())
    .then(data => {
      setMessages(data); 
    })
    .catch(err => console.error('Error:', err));
}, []);
*/