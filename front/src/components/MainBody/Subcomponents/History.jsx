import { useState } from 'react';
import MessageItem from '../../Subjects/Subcomponents/MessageItem.jsx';
import styles from '../index.module.css';

export default function History({ sentMessages }) {
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [summaries, setSummaries] = useState({});
  const [loading, setLoading] = useState({});

  const getBaseSubject = (subject) => {
    return subject.replace(/^(Re|Fwd|Fw):\s*/i, '').trim();
  };

  const fetchSummaryForConversation = (clickedMessage) => {
    const baseSubject = getBaseSubject(clickedMessage.subject);
    setLoading((prev) => ({ ...prev, [baseSubject]: true }));

    const conversationMessages = sentMessages.filter(
      (msg) => getBaseSubject(msg.subject) === baseSubject
    );

    const conversationBody = conversationMessages
      .map(
        (msg) =>
          `From: ${msg.sender}\nTo: ${msg.to}\nSubject: ${msg.subject}\n\n${msg.description}`
      )
      .join('\n\n---\n\n');

    const requestBody = {
      id: clickedMessage.id,
      subject: clickedMessage.subject,
      from: clickedMessage.sender,
      body: conversationBody,
    };

    fetch('http://localhost:5000/summarize-conversation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        if (data.output) {
          setSummaries((prev) => ({ ...prev, [baseSubject]: data.output }));
        } else {
          setSummaries((prev) => ({
            ...prev,
            [baseSubject]: 'Failed to load summary.',
          }));
        }
      })
      .catch((err) => {
        console.error('Error getting summary:', err);
        setSummaries((prev) => ({
          ...prev,
          [baseSubject]: 'Error loading summary.',
        }));
      })
      .finally(() => {
        setLoading((prev) => ({ ...prev, [baseSubject]: false }));
      });
  };

  const handleItemClick = (index) => {
    if (selectedIndex === index) {
      setSelectedIndex(null);
    } else {
      setSelectedIndex(index);
      const clickedMessage = sentMessages[index];
      const baseSubject = getBaseSubject(clickedMessage.subject);
      if (!summaries[baseSubject] && !loading[baseSubject]) {
        fetchSummaryForConversation(clickedMessage);
      }
    }
  };

  return (
    <div className={styles.historySection}>
      <h3>Istoric Mesaje</h3>
      <div className={styles.messageList}>
        {sentMessages.map((msg, index) => {
          const baseSubject = getBaseSubject(msg.subject);
          const summary = summaries[baseSubject];
          const isLoading = loading[baseSubject];

          return (
            <div key={index}>
              <div
                style={{ cursor: 'pointer' }}
                onClick={() => handleItemClick(index)}
              >
                <MessageItem
                  sender={msg.sender}
                  subject={msg.subject}
                  time={msg.time}
                  selected={selectedIndex === index}
                />
              </div>
              {selectedIndex === index && (
                <div className={styles.messageDescription}>
                  <strong>Summary:</strong>{' '}
                  {isLoading
                    ? 'Loading...'
                    : summary || 'Click to load summary.'}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}