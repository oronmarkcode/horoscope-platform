import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../lib/api'
import { useAuth } from '../store/auth'

export default function Login() {
    const { setToken } = useAuth()
    const navigate = useNavigate()
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState<string | null>(null)

    async function onSubmit(e: React.FormEvent) {
        e.preventDefault()
        setError(null)
        try {
            const res = await api.post('/api/v1/auth/login', { username, password })
            setToken(res.data.access_token)
            navigate('/dashboard', { replace: true })
        } catch (err: any) {
            setError(err?.response?.data?.detail || 'Login failed')
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
            <form onSubmit={onSubmit} className="bg-white/10 p-6 rounded w-80">
                <h1 className="text-2xl font-bold mb-4">Login</h1>
                <input className="w-full mb-3 px-3 py-2 rounded bg-white/20" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                <input className="w-full mb-3 px-3 py-2 rounded bg-white/20" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                {error && <p className="text-red-300 text-sm mb-2">{error}</p>}
                <button className="w-full px-3 py-2 rounded bg-indigo-600 hover:bg-indigo-500">Sign in</button>
            </form>
        </div>
    )
}


