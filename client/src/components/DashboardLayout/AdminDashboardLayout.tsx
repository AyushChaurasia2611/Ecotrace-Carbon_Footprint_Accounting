import React from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './DashboardLayout.css';
import { FiGrid, FiBarChart2, FiUpload, FiLogOut, FiEdit, FiAlertTriangle, FiUsers } from "react-icons/fi";
import { Leaf } from "lucide-react";

interface LayoutProps {
  children: React.ReactNode;
}

export const AdminDashboardLayout: React.FC<LayoutProps> = ({ children }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isExcludedPage = location.pathname === '/admin/students' || location.pathname === '/admin/reviews';

  return (
    <div className="dashboard-layout">
      <nav className="sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo-container">
            <Leaf className="sidebar-logo-icon" size={24} />
          </div>
          <h1>EcoTrace</h1>
        </div>

        <ul className="nav-links" style={{ marginTop: '20px' }}>
          {/* Dashboard */}
          <li>
            <NavLink to="/dashboard" className="nav-link" end>
              <FiGrid className="nav-icon" /><span>Dashboard</span><div className="active-dot"></div>
            </NavLink>
          </li>

          {/* Upload Data */}
          <li>
            <NavLink to="/dashboard/upload" className="nav-link">
              <FiUpload className="nav-icon" /><span>Smart Upload</span><div className="active-dot"></div>
            </NavLink>
          </li>

          {/* Manual Entry */}
          <li>
            <NavLink to="/dashboard/manual-entry" className="nav-link">
              <FiEdit className="nav-icon" /><span>Manual Entry</span><div className="active-dot"></div>
            </NavLink>
          </li>

          {/* Analytics */}
          <li>
            <NavLink to="/dashboard/analytics" className="nav-link">
              <FiBarChart2 className="nav-icon" /><span>Analytics</span><div className="active-dot"></div>
            </NavLink>
          </li>

          {/* Hotspots */}
          <li>
            <NavLink to="/dashboard/hotspots" className="nav-link">
              <FiAlertTriangle className="nav-icon" /><span>Hotspots</span><div className="active-dot"></div>
            </NavLink>
          </li>

          {/* Reports */}
          <li>
            <NavLink to="/dashboard/reports" className="nav-link">
              <FiBarChart2 className="nav-icon" /><span>Reports</span><div className="active-dot"></div>
            </NavLink>
          </li>

          {/* Student Activities Section */}
          <li className="sidebar-section-title" style={{ paddingLeft: '1rem', paddingTop: '1.5rem', paddingBottom: '0.5rem' }}>
            STUDENT ACTIVITIES
          </li>

          <li>
            <NavLink to="/admin/students" className="nav-link">
              <FiUsers className="nav-icon" /><span>Student Management</span><div className="active-dot"></div>
            </NavLink>
          </li>

          <li>
            <NavLink to="/admin/reviews" className="nav-link">
              <FiEdit className="nav-icon" /><span>Review & Assign</span><div className="active-dot"></div>
            </NavLink>
          </li>
        </ul>

        <div className="sidebar-footer">
          <button onClick={handleLogout} className="nav-link logout-btn">
            <FiLogOut className="nav-icon" /><span>Logout</span>
          </button>
        </div>
      </nav>

      <main className={`main-content ${isExcludedPage ? 'white-bg' : 'light-mint-bg'}`}>
        {children}
      </main>
    </div>
  );
};
