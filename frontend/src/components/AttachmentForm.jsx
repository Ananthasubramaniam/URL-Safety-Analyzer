import React, { useState } from 'react';
import { FileText, Upload, AlertCircle } from 'lucide-react';

const AttachmentForm = () => {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Placeholder for future implementation
        alert('Attachment analysis feature coming soon!');
    };

    return (
        <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto">
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                <div className="flex items-center gap-3 mb-4">
                    <FileText className="w-6 h-6 text-purple-400" />
                    <h2 className="text-xl font-semibold text-white">Analyze Attachment</h2>
                </div>

                <div className="mb-6">
                    <label className="flex flex-col items-center justify-center w-full h-48 border-2 border-slate-600 border-dashed rounded-lg cursor-pointer bg-slate-900/50 hover:bg-slate-800 transition-colors">
                        <div className="flex flex-col items-center justify-center pt-5 pb-6">
                            <Upload className="w-10 h-10 mb-3 text-slate-400" />
                            <p className="mb-2 text-sm text-slate-400">
                                <span className="font-semibold">Click to upload</span> or drag and drop
                            </p>
                            <p className="text-xs text-slate-500">
                                PDF, DOCX, EXE, ZIP (MAX. 10MB)
                            </p>
                        </div>
                        <input type="file" className="hidden" onChange={handleFileChange} />
                    </label>
                    {file && (
                        <div className="mt-2 text-sm text-blue-400 font-medium">
                            Selected: {file.name}
                        </div>
                    )}
                </div>

                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-yellow-500 text-sm">
                        <AlertCircle className="w-4 h-4" />
                        <span>This feature is currently in development.</span>
                    </div>
                    <button
                        type="submit"
                        disabled={!file}
                        className="bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-6 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Scan File
                    </button>
                </div>
            </div>
        </form>
    );
};

export default AttachmentForm;
