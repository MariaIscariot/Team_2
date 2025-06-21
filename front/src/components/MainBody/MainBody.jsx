import { useState } from 'react';
import styles from './index.module.css';
import History from './Subcomponents/History.jsx';
import SendMessage from './Subcomponents/SendMessage.jsx'
import Rezume from './Subcomponents/Rezume.jsx';

export default function MainBody({ message }) {
  const [activeTab, setActiveTab] = useState('Main');
  const [activeAction, setActiveAction] = useState('Send message'); 
  const [sentMessages, setSentMessages] = useState([
  { id: 1, sender: 'Bagrin Veronica', reciever: 'DimaPro', subject: 'Important', description: 'Привет! Нужно обсудить проект.', time: '17.06, Вт', seen: false },
  { id: 2, sender: 'DimaPro', reciever: 'Bagrin Veronica', subject: 'Important', description: 'Привет! Конечно, что именно?', time: '17.06, Вт', seen: false },
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

const renderContent = () => {
  if (activeTab === 'Main') {
    switch (activeAction) {
      case 'Send message':
        return <SendMessage message={message} />;
      case 'History':
        return (
          <div className={styles.historySection}>
            {sentMessages.length === 0 ? (
              <p>Nu există mesaje trimise încă.</p>
            ) : <History sentMessages={sentMessages} />}
          </div>
        );
      case 'Resume':
        return <Rezume />;
      default:
        return null;
    }
  }
  if (activeTab === 'HR' || activeTab === 'Instagram') {
    return (
      <div className={styles.hrInstagramInfo}>
        <div style={{marginBottom: 12, fontWeight: 500}}>
          {sentMessages.length} mesaje
        </div>
      </div>
    );
  }
  return null;
};

  return (
    <div className={styles.mainBodyOutlook}>
      <aside className={styles.sidebar}>
        <nav className={styles.mainNavbar}>
          {['Main', 'HR', 'Instagram'].map((tab) => (
            <button
              key={tab}
              className={`${styles.navTab} ${activeTab === tab ? styles.active : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </nav>

        {activeTab === 'Main' && (
          <div className={styles.actionButtons}>
            {['Send message', 'History', 'Resume'].map((action) => (
              <button
                key={action}
                className={`${styles.actionBtn} ${activeAction === action ? styles.active : ''}`}
                onClick={() => setActiveAction(action)}
              >
                {action}
              </button>
            ))}
          </div>
        )}
      </aside>

      <main className={styles.mainContent}>
        <div className={styles.contentHeader}>
          <h2>{activeTab} - {activeAction}</h2>
        </div>
        <div className={styles.contentBody}>
          {renderContent()}
        </div>
      </main>
    </div>
  );
}
