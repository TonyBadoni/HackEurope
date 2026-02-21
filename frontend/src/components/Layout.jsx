import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import '../styles/Layout.css';

const Layout = () => {
  return (
    <div className="layout">
      <div className="layout__sidebar">
        <Sidebar />
      </div>
      <main className="layout__main">
        <div className="layout__content">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default Layout;
