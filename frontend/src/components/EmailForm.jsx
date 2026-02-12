import React, { useState } from 'react';
import { Mail, AlertCircle } from 'lucide-react';

const EmailForm = () => {
    const [emailContent, setEmailContent] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Placeholder for future implementation
        alert('Email analysis feature coming soon!');
    };

    return (
        <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto">
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                <div className="flex items-center gap-3 mb-4">
                    <Mail className="w-6 h-6 text-blue-400" />
                    <h2 className="text-xl font-semibold text-white">Analyze Email Content</h2>
                </div>

                <div className="mb-4">
                    <label className="block text-slate-400 text-sm font-medium mb-2">
                        Paste email headers and body
                    </label>
                    <textarea
                        className="w-full h-48 bg-slate-900 border border-slate-700 rounded-lg p-4 text-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
                        placeholder="Paste the raw email content here..."
                        value={emailContent}
                        onChange={(e) => setEmailContent(e.target.value)}
                    ></textarea>
                </div>

                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-yellow-500 text-sm">
                        <AlertCircle className="w-4 h-4" />
                        <span>This feature is currently in development.</span>
                    </div>
                    <button
                        type="submit"
                        className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-md transition-colors"
                    >
                        Analyze Email
                    </button>
                </div>
            </div>
        </form>
    );
};

export default EmailForm;
