import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import CreditsBadge from './components/CreditsBadge'
import { ToastHost } from './components/Toast'
import Dashboard from './pages/Dashboard'
import History from './pages/History'
import Home from './pages/Home'
import Login from './pages/Login'
import Profile from './pages/Profile'
import Signup from './pages/Signup'
import { useAuth } from './store/auth'

export default function App() {
    const { token, logout } = useAuth()
    return (
        <BrowserRouter>
            <header className="bg-slate-900 text-white">
                <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
                    <Link to="/" className="font-bold">MyHoroscope</Link>
                    <nav className="flex items-center gap-4 text-sm">
                        <Link to="/">Home</Link>
                        <CreditsBadge />
                        {token ? (
                            <>
                                <Link to="/dashboard">Dashboard</Link>
                                <Link to="/profile">Profile</Link>
                                <button onClick={logout} className="px-2 py-1 rounded bg-indigo-600 hover:bg-indigo-500">Logout</button>
                            </>
                        ) : (
                            <>
                                <Link to="/login">Login</Link>
                                <Link to="/signup">Signup</Link>
                            </>
                        )}
                    </nav>
                </div>
            </header>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/history" element={<History />} />
                <Route path="/profile" element={<Profile />} />
            </Routes>
            <ToastHost />
        </BrowserRouter>
    )
}


