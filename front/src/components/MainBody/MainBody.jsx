import React, { useState } from 'react';
import './MainBody.css';

const MainBody = () => {
  const [activeTab, setActiveTab] = useState('Main');
  const [activeAction, setActiveAction] = useState('Send message');
  const [toField, setToField] = useState('');
  const [ccField, setCcField] = useState('');
  const [messageText, setMessageText] = useState('');
  const [sentMessages, setSentMessages] = useState([]);

  const handleSend = () => {
    if (toField && messageText) {
      const newMessage = {
        id: Date.now(),
        to: toField,
        cc: ccField,
        text: messageText,
        timestamp: new Date().toLocaleString()
      };
      setSentMessages([...sentMessages, newMessage]);
      setToField('');
      setCcField('');
      setMessageText('');
    }
  };

  const renderContent = () => {
    switch (activeAction) {
      case 'Send message':
        return (
          <div className="message-composer">
            <div className="message-fields">
              <div className="field-row">
                <label>To:</label>
                <input
                  type="email"
                  value={toField}
                  onChange={(e) => setToField(e.target.value)}
                  placeholder="Enter the email address"
                />
              </div>
              <div className="field-row">
                <label>CC:</label>
                <input
                  type="email"
                  value={ccField}
                  onChange={(e) => setCcField(e.target.value)}
                  placeholder="CC addresses (optional)"
                />
              </div>
            </div>
            <div className="message-body">
              <textarea
                value={messageText}
                onChange={(e) => setMessageText(e.target.value)}
                placeholder="Write your message here..."
                rows="10"
              />
            </div>
            <button className="send-button" onClick={handleSend}>
              Send
            </button>
          </div>
        );
      
      case 'History':
        return (
          <div className="history-section">
            <h3>Message history</h3>
            {sentMessages.length === 0 ? (
              <p>There are no messages sent yet.</p>
            ) : (
              sentMessages.map(message => (
                <div key={message.id} className="message-item">
                  <div className="message-header">
                    <strong>To:</strong> {message.to}
                    {message.cc && <span> | <strong>CC:</strong> {message.cc}</span>}
                    <span className="timestamp">{message.timestamp}</span>
                  </div>
                  <div className="message-content">{message.text}</div>
                </div>
              ))
            )}
          </div>
        );
      
      case 'Resume':
        return (
          <div className="resume-section">
            <h3>Summary</h3>
            <p>Total messages sent: {sentMessages.length}</p>
            <p>Last activity: {sentMessages.length > 0 ? sentMessages[sentMessages.length - 1].timestamp : 'N/A'}</p>
          </div>
        );
      
      default:
        return <div>Select an action</div>;
    }
  };

  return (
    <div className="main-body-outlook">
      {/* Navbar principal */}
      <nav className="main-navbar">
        {['Main', 'HR', 'Instagram'].map(tab => (
          <button
            key={tab}
            className={`nav-tab ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </nav>

      {/* Butoane acțiuni */}
      <div className="action-buttons">
        {['Send message', 'History', 'Resume'].map(action => (
          <button
            key={action}
            className={`action-btn ${activeAction === action ? 'active' : ''}`}
            onClick={() => setActiveAction(action)}
          >
            {action}
          </button>
        ))}
      </div>

      {/* Conținut principal */}
      <div className="main-content">
        <div className="content-header">
          <h2>{activeTab} - {activeAction}</h2>
        </div>
        <div className="content-body">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default MainBody;