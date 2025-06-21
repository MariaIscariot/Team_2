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
        fetch('http://localhost:3000/api/messages')  
        .then(res => res.json())
        .then(data => {
            setMessages(data); 
        })
        .catch(err => {
            console.error('Error:', err);
            setMessages([
  { id: 1, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'Привет! Нужно обсудить проект.', time: '17.06, Вт', seen: false },
  { id: 2, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Hoh', description: 'Привет! Конечно, что именно?', time: '17.06, Вт', seen: false },
  { id: 3, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'По поводу сроков сдачи.', time: '17.06, Вт', seen: true },
  { id: 4, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Important', description: 'Я думаю, успеем к пятнице.', time: '17.06, Вт', seen: true },
  { id: 5, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'Хорошо, тогда начинаем завтра.', time: '18.06, Ср', seen: false },
  { id: 6, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Important', description: 'Окей, какие задачи на меня?', time: '18.06, Ср', seen: false },
  { id: 7, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'Сделай макет и опиши архитектуру.', time: '18.06, Ср', seen: true },
  { id: 8, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Important', description: 'Принято, к вечеру отправлю.', time: '18.06, Ср', seen: true },
  { id: 9, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'Спасибо, жду!', time: '18.06, Ср', seen: true },
  { id: 10, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Important', description: 'Отправил на почту, проверь.', time: '18.06, Ср', seen: false },
  { id: 11, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'Всё отлично, только пара правок.', time: '18.06, Ср', seen: false },
  { id: 12, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Important', description: 'Исправлю сейчас.', time: '18.06, Ср', seen: true },
  { id: 13, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'Спасибо большое!', time: '18.06, Ср', seen: true },
  { id: 14, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Important', description: 'Всегда рад помочь!', time: '18.06, Ср', seen: true },
  { id: 15, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'Давай ещё обсудим UI?', time: '19.06, Чт', seen: false },
  { id: 16, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Important', description: 'Да, у меня есть пара идей.', time: '19.06, Чт', seen: false },
  { id: 17, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'Круто, покажешь вечером?', time: '19.06, Чт', seen: true },
  { id: 18, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Important', description: 'Да, подготовлю всё.', time: '19.06, Чт', seen: true },
  { id: 19, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'Жду, удачи!', time: '19.06, Чт', seen: true },
  { id: 20, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Important', description: 'Спасибо!', time: '19.06, Чт', seen: true },
            ]);
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

