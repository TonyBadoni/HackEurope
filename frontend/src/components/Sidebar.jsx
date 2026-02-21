import { NavLink } from 'react-router-dom';
import '../styles/Sidebar.css';

const Sidebar = () => {
  const navigationItems = [
    {
      section: 'Main',
      items: [
        { name: 'Dashboard', path: '/', icon: '📊' },
        { name: 'Updates', path: '/updates', icon: '🔔', badge: 'Live' },
        { name: 'Analytics', path: '/analytics', icon: '📈' },
      ]
    },
    {
      section: 'Management',
      items: [
        { name: 'Projects', path: '/projects', icon: '📁' },
        { name: 'Tasks', path: '/tasks', icon: '✓' },
        { name: 'Team', path: '/team', icon: '👥' },
      ]
    },
    {
      section: 'Settings',
      items: [
        { name: 'Configuration', path: '/settings', icon: '⚙️' },
        { name: 'API Keys', path: '/api-keys', icon: '🔑' },
      ]
    }
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar__header">
        <div className="sidebar__logo">
          <div className="sidebar__logo-icon">H</div>
          <span>HackEurope</span>
        </div>
      </div>

      <div className="sidebar__status">
        <div className="sidebar__status-dot connected"></div>
        <span className="sidebar__status-text">Connected</span>
      </div>

      <nav className="sidebar__nav">
        {navigationItems.map((section, idx) => (
          <div key={idx} className="sidebar__section">
            <div className="sidebar__section-title">{section.section}</div>
            <ul className="sidebar__menu">
              {section.items.map((item) => (
                <li key={item.path} className="sidebar__menu-item">
                  <NavLink
                    to={item.path}
                    end={item.path === '/'}
                    className={({ isActive }) =>
                      `sidebar__link ${isActive ? 'active' : ''}`
                    }
                  >
                    <span className="sidebar__icon">{item.icon}</span>
                    <span>{item.name}</span>
                    {item.badge && (
                      <span className="sidebar__badge">{item.badge}</span>
                    )}
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>

      <div className="sidebar__footer">
        <div className="sidebar__user">
          <div className="sidebar__avatar">U</div>
          <div className="sidebar__user-info">
            <div className="sidebar__user-name">User</div>
            <div className="sidebar__user-email">user@hackeurope.dev</div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
