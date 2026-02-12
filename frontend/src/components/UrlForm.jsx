import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

const UrlForm = ({ onAnalyze, isLoading }) => {
    const [url, setUrl] = useState('');
    const [error, setError] = useState('');

    const validateUrl = (string) => {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        if (!url) {
            setError('Please enter a URL');
            return;
        }

        let urlToAnalyze = url;
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            urlToAnalyze = 'https://' + url;
        }

        if (!validateUrl(urlToAnalyze)) {
            setError('Please enter a valid URL');
            return;
        }

        onAnalyze(urlToAnalyze);
    };

    return (
        <form onSubmit={handleSubmit} className="url-form-container">
            <div className="url-input-wrapper">
                <Search className="search-icon" size={20} />
                <input
                    type="text"
                    className="url-input"
                    placeholder="Enter URL to analyze (e.g., google.com)"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    disabled={isLoading}
                />
                <button
                    type="submit"
                    disabled={isLoading}
                    className="analyze-btn"
                >
                    {isLoading ? (
                        <>
                            <Loader2 className="animate-spin" size={18} />
                            <span>Scanning...</span>
                        </>
                    ) : (
                        'Analyze'
                    )}
                </button>
            </div>
            {error && <p className="error-message">{error}</p>}
        </form>
    );
};

export default UrlForm;
