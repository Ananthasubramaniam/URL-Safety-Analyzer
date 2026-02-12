import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, Link as LinkIcon, Mail, FileText, History, Users, LayoutDashboard } from 'lucide-react';

const Navbar = () => {
    const location = useLocation();

    const navItems = [
        { path: '/', icon: LinkIcon, label: 'URL' },
        { path: '/email', icon: Mail, label: 'Email' },
        { path: '/attachment', icon: FileText, label: 'Attachment' },
        { path: '/bulk', icon: FileText, label: 'Bulk Scan' },
        { path: '/history', icon: History, label: 'History' },
        { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    ];

    return (
        <nav className="navbar">
            <div className="nav-container">
                <Link to="/" className="nav-logo">
                    <Shield className="nav-icon" size={28} />
                    <span>PhishGuard - URL Safety Analyzer</span>
                </Link>

                <div className="nav-links">
                    {navItems.map((item) => (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
                        >
                            <item.icon size={18} />
                            <span>{item.label}</span>
                        </Link>
                    ))}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
