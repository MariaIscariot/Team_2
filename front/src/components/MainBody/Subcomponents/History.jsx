import React, { useState } from 'react';
import MessageItem from '../../Subjects/Subcomponents/MessageItem.jsx';

const messages = [
  {
    sender: 'FAF',
    subject: 'Summer FAF x Sigmoid',
    time: 'Thu, 14:49',
    message: 'Join our special summer event in collaboration with Sigmoid. Details inside.'
  },
  {
    sender: 'Turcan Ana',
    subject: 'UTM Bioinformatics board',
    time: 'Thu, 13:55',
    message: 'Please check the updated agenda for the Bioinformatics board meeting.'
  },
  {
    sender: 'UTM DTIC',
    subject: 'SIMU Student Authorization',
    time: 'Wed, 17:06',
    message: 'Your SIMU student account has been authorized successfully.'
  },
  {
    sender: 'Istrati Daniela',
    subject: 'Re-examination Session',
    time: 'Wed, 11:34',
    message: 'You are registered for the re-examination session. Please review the schedule.'
  },
  {
    sender: 'No-reply Moodle UTM',
    subject: 'You have submitted your report',
    time: 'Tue, 17.06',
    message: 'Your report has been successfully submitted on the Moodle platform.'
  },
  {
    sender: 'Bagrin Veronica',
    subject: 'Important',
    time: 'Tue, 17.06',
    message: 'Please read the attached document carefully. It contains important information.'
  },
  {
    sender: 'FAF',
    subject: 'Summer FAF x Sigmoid',
    time: 'Thu, 14:49',
    message: 'Join our special summer event in collaboration with Sigmoid. Details inside.'
  },
  {
    sender: 'Turcan Ana',
    subject: 'UTM Bioinformatics board',
    time: 'Thu, 13:55',
    message: 'Please check the updated agenda for the Bioinformatics board meeting.'
  },
  {
    sender: 'UTM DTIC',
    subject: 'SIMU Student Authorization',
    time: 'Wed, 17:06',
    message: 'Your SIMU student account has been authorized successfully.'
  },
  {
    sender: 'Istrati Daniela',
    subject: 'Re-examination Session',
    time: 'Wed, 11:34',
    message: 'You are registered for the re-examination session. Please review the schedule.'
  },
  {
    sender: 'No-reply Moodle UTM',
    subject: 'You have submitted your report',
    time: 'Tue, 17.06',
    message: 'Your report has been successfully submitted on the Moodle platform.'
  },
  {
    sender: 'Bagrin Veronica',
    subject: 'Important',
    time: 'Tue, 17.06',
    message: 'Please read the attached document carefully. It contains important information.'
  },
  {
    sender: 'FAF',
    subject: 'Summer FAF x Sigmoid',
    time: 'Thu, 14:49',
    message: 'Join our special summer event in collaboration with Sigmoid. Details inside.'
  },
  {
    sender: 'Turcan Ana',
    subject: 'UTM Bioinformatics board',
    time: 'Thu, 13:55',
    message: 'Please check the updated agenda for the Bioinformatics board meeting.'
  },
  {
    sender: 'UTM DTIC',
    subject: 'SIMU Student Authorization',
    time: 'Wed, 17:06',
    message: 'Your SIMU student account has been authorized successfully.'
  },
  {
    sender: 'Istrati Daniela',
    subject: 'Re-examination Session',
    time: 'Wed, 11:34',
    message: 'You are registered for the re-examination session. Please review the schedule.'
  },
  {
    sender: 'No-reply Moodle UTM',
    subject: 'You have submitted your report',
    time: 'Tue, 17.06',
    message: 'Your report has been successfully submitted on the Moodle platform.'
  },
  {
    sender: 'Bagrin Veronica',
    subject: 'Important',
    time: 'Tue, 17.06',
    message: 'Please read the attached document carefully. It contains important information.'
  },
];

export default function History() {
  const [selectedIndex, setSelectedIndex] = useState(null);

  return (
    <div className={styles.historySection}>
      <h3>Istoric Mesaje</h3>
      <ul className={styles.messageList}>
        {messages.map((msg, index) => (
          <MessageItem
            key={index}
            sender={msg.sender}
            subject={msg.subject}
            time={msg.time}
            selected={selectedIndex === index}
            onClick={() => setSelectedIndex(index)}
          />
        ))}
      </ul>
    </div>
  );
}