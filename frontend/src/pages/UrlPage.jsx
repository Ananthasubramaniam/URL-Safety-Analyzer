import React, { useState } from 'react';
import UrlForm from '../components/UrlForm';
import ResultCard from '../components/ResultCard';
import { analyzeUrl } from '../services/api';
import { ShieldCheck } from 'lucide-react';

const UrlPage = () => {
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleAnalyze = async (url) => {
        setIsLoading(true);
        setError('');
        setResult(null);

        try {
            const data = await analyzeUrl(url);
            setResult(data);
        } catch (err) {
            setError('Failed to analyze URL. Please ensure the backend is running.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container main-content col-center animate-fade-in">
            <div className="text-center" style={{ marginBottom: 'var(--spacing-xl)' }}>
                <div className="flex-center" style={{ marginBottom: 'var(--spacing-md)', color: 'var(--accent-primary)' }}>
                    <ShieldCheck size={64} />
                </div>
                <h1 className="page-title">
                    URL Safety Analyzer
                </h1>
                <p className="page-subtitle">
                    Detect phishing threats, malicious links, and dangerous websites in real-time.
                </p>
            </div>

            <UrlForm onAnalyze={handleAnalyze} isLoading={isLoading} />

            {error && (
                <div style={{
                    marginTop: 'var(--spacing-lg)',
                    padding: 'var(--spacing-md)',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    border: '1px solid var(--status-danger)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--status-danger)'
                }}>
                    {error}
                </div>
            )}

            <ResultCard result={result} />
        </div>
    );
};

export default UrlPage;
