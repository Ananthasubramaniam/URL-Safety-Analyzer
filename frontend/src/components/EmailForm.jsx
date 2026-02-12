import React, { useState } from 'react';
import { Mail, AlertCircle, Loader2, Send } from 'lucide-react';
import { analyzeEmail } from '../services/api';
import ResultCard from './ResultCard';

const EmailForm = () => {
    const [emailContent, setEmailContent] = useState('');
    const [subject, setSubject] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!emailContent.trim() || !subject.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await analyzeEmail(subject, emailContent);
            setResult(data);
        } catch (err) {
            setError('Failed to analyze email. Please ensure the backend is running.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="email-form-container">
            <form onSubmit={handleSubmit}>
                <div className="email-form-header">
                    <div className="email-icon-box">
                        <Mail size={24} />
                    </div>
                    <div>
                        <h2 style={{ fontSize: '1.25rem', fontWeight: '700', color: 'var(--text-primary)' }}>Analyze Email Content</h2>
                        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Check email headers and body for phishing indicators</p>
                    </div>
                </div>

                <div className="email-input-group">
                    <label className="email-label">Email Subject</label>
                    <input
                        type="text"
                        className="email-input-field"
                        placeholder="e.g. Urgent: Account Verification Required"
                        value={subject}
                        onChange={(e) => setSubject(e.target.value)}
                        required
                        disabled={loading}
                    />
                </div>

                <div className="email-input-group">
                    <label className="email-label">Email Body Content</label>
                    <textarea
                        className="email-input-field email-textarea"
                        placeholder="Paste the full email content (headers and body) here..."
                        value={emailContent}
                        onChange={(e) => setEmailContent(e.target.value)}
                        required
                        disabled={loading}
                    ></textarea>
                </div>

                {error && (
                    <div className="error-message" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <AlertCircle size={16} />
                        <span>{error}</span>
                    </div>
                )}

                <div className="email-submit-container">
                    <button
                        type="submit"
                        disabled={loading || !subject || !emailContent}
                        className="email-submit-btn"
                    >
                        {loading ? (
                            <>
                                <Loader2 className="animate-spin" size={18} />
                                <span>Scanning...</span>
                            </>
                        ) : (
                            <>
                                <Send size={18} />
                                <span>Analyze Email</span>
                            </>
                        )}
                    </button>
                </div>
            </form>

            {result && (
                <div style={{ marginTop: 'var(--spacing-xl)', width: '100%', display: 'flex', justifyContent: 'center' }}>
                    <ResultCard result={result} />
                </div>
            )}
        </div>
    );
};

export default EmailForm;
