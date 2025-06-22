import React from 'react';
import styles from './index.module.css';

const CheckmarkIcon = () => (
  <svg
    width="16"
    height="16"
    viewBox="0 0 16 16"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={styles.checkmarkIcon}
  >
    <path
      d="M13.3337 4L6.00033 11.3333L2.66699 8"
      stroke="#22C55E"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

const AnalysisResultDisplay = ({ analysisText }) => {
  if (!analysisText) {
    return null;
  }

  const sections = {
    topic: 'N/A',
    keyPoints: [],
    conclusion: 'N/A',
    relevantQuotes: 'N/A',
  };

  try {
    const topicMatch = analysisText.match(/Topic:(.*?)(Key Points:|$)/s);
    if (topicMatch) sections.topic = topicMatch[1].trim();

    const keyPointsMatch = analysisText.match(/Key Points:(.*?)(Conclusion:|$)/s);
    if (keyPointsMatch) {
      sections.keyPoints = keyPointsMatch[1]
        .split('*')
        .map(pt => pt.trim())
        .filter(pt => pt.length > 0);
    }

    const conclusionMatch = analysisText.match(/Conclusion:(.*?)(Relevant Quotes:|$)/s);
    if (conclusionMatch) sections.conclusion = conclusionMatch[1].trim();
    
    const quotesMatch = analysisText.match(/Relevant Quotes:(.*)/s);
    if (quotesMatch) sections.relevantQuotes = quotesMatch[1].trim();
    if (sections.relevantQuotes.toLowerCase() === 'none.') {
        sections.relevantQuotes = '';
    }

  } catch (error) {
    console.error("Failed to parse analysis text:", error);
    // Fallback to preformatted text if parsing fails
    return <pre>{analysisText}</pre>;
  }


  return (
    <div className={styles.analysisResultContainer}>
      <h3 className={styles.analysisTopic}>{sections.topic}</h3>

      <h4 className={styles.analysisSectionTitle}>Key Points</h4>
      <ul className={styles.analysisKeyPoints}>
        {sections.keyPoints.map((point, index) => (
          <li key={index}>
            <CheckmarkIcon />
            <span>{point}</span>
          </li>
        ))}
      </ul>

      <h4 className={styles.analysisSectionTitle}>Conclusion</h4>
      <p className={styles.analysisConclusion}>{sections.conclusion}</p>

      {sections.relevantQuotes && (
        <>
            <h4 className={styles.analysisSectionTitle}>Relevant Quotes</h4>
            <blockquote className={styles.analysisQuote}>
                {sections.relevantQuotes}
            </blockquote>
        </>
      )}
    </div>
  );
};

export default AnalysisResultDisplay; 