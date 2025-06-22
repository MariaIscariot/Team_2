import { useState, useEffect } from 'react';
import styles from './index.module.css';
import MessageItem from './Subcomponents/MessageItem.jsx';


export default function Subjects({ onSelectMessage }) {
    const [selectedIndex, setSelectedIndex] = useState(null);
    const [messages, setMessages] = useState([]);

    const handleClick = (msg, index) => {
        setSelectedIndex(index);
        onSelectMessage(msg);
        
        msg.seen = true;
        // if (!msg.seen) {
        //     fetch(`http://localhost:3000/api/messages/seen/${msg.id}`, { method: 'POST' })
        //     .then(res => {
        //         if (res.ok) {
        //             msg.seen = true;
        //         } else {
        //             console.error('Error marking message as seen:', res.statusText);
        //         }
        //     }) 
        // }
    };

    useEffect(() => {
        fetch('http://localhost:5000/get-subjects')  
        .then(res => res.json())
        .then(data => {
            if (data.messages && Array.isArray(data.messages)) {
                setMessages(data.messages); 
            } else {
                console.error('Invalid data structure:', data);
                setMessages([]);
            }
        })
        .catch(err => {
            console.error('Error fetching subjects:', err);
            setMessages([]);
        });
    }, []);

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

