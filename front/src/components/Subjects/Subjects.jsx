import { useState, useEffect } from 'react';
import styles from './index.module.css';
import MessageItem from './Subcomponents/MessageItem.jsx';

const messages = [
  { sender: 'FAF', subject: 'Summer FAF x Sigmoid', time: 'Чт, 14:49', seen: true, id: 1 },
  { sender: 'Turcan Ana', subject: 'UTM Bioinformatics board', time: 'Чт, 13:55', seen: false, id: 2 },
  { sender: 'UTM DTIC', subject: 'Autorizare SIMU Student', time: 'Ср, 17:06', seen: true, id: 3 },
  { sender: 'Istrati Daniela', subject: 'Sesiunea de reexaminare', time: 'Ср, 11:34', seen: false,  id: 4 },
  { sender: 'No-reply Moodle UTM', subject: 'Вы отправили свой отчет', time: '17.06, Вт', seen: true, id: 5 },
  { sender: 'Bagrin Veronica', subject: 'Important', time: '17.06, Вт', seen: false, id: 6 },
  { sender: 'FAF', subject: 'Summer FAF x Sigmoid', time: 'Чт, 14:49', seen: true, id: 7 },
  { sender: 'Turcan Ana', subject: 'UTM Bioinformatics board', time: 'Чт, 13:55', seen: false, id: 8 },
  { sender: 'UTM DTIC', subject: 'Autorizare SIMU Student', time: 'Ср, 17:06', seen: false, id: 9 },
  { sender: 'Istrati Daniela', subject: 'Sesiunea de reexaminare', time: 'Ср, 11:34', seen: true, id: 10 },
  { sender: 'No-reply Moodle UTM', subject: 'Вы отправили свой отчет', time: '17.06, Вт', seen: false, id: 11 },
  { sender: 'Bagrin Veronica', subject: 'Important', time: '17.06, Вт', seen: true, id: 12 },
  { sender: 'FAF', subject: 'Summer FAF x Sigmoid', time: 'Чт, 14:49', seen: false, id: 13 },
  { sender: 'Turcan Ana', subject: 'UTM Bioinformatics board', time: 'Чт, 13:55', seen: true, id: 14 },
  { sender: 'UTM DTIC', subject: 'Autorizare SIMU Student', time: 'Ср, 17:06', seen: false, id: 15 },
  { sender: 'Istrati Daniela', subject: 'Sesiunea de reexaminare', time: 'Ср, 11:34', seen: true, id: 16 },
  { sender: 'No-reply Moodle UTM', subject: 'Вы отправили свой отчет', time: '17.06, Вт', seen: true, id: 17 },
  { sender: 'Bagrin Veronica', subject: 'Important', time: '17.06, Вт', seen: false, id: 18 },
];

export default function Subjects({ onSelectMessage }) {
  const [selectedIndex, setSelectedIndex] = useState(null);

  const handleClick = (msg, index) => {
    setSelectedIndex(index);
    onSelectMessage(msg);

    if (!msg.seen) {
        msg.seen = true;

        // fetch(`http://localhost:3000/api/messages/${msg.id}/mark-seen`, {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        // })
        // .then(res => {
        //   if (res.ok) {
        //     msg.seen = true;
        //   } else {
        //     console.error('Error marking message as seen:', res.statusText);
        //   }
        // })
        // .catch(err => console.error('Fetch error:', err));
    }
  };

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
            seen={msg.seen}
            selected={selectedIndex === index}
            onClick={() => handleClick(msg, index)}
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