import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../lib/api'
import { useAuth } from '../store/auth'

export default function Signup() {
    const navigate = useNavigate()
    const { setToken } = useAuth()
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [name, setName] = useState('')
    const [dob, setDob] = useState('')
    const [timezone, setTimezone] = useState(Intl.DateTimeFormat().resolvedOptions().timeZone)
    const [error, setError] = useState<string | null>(null)
    const [ok, setOk] = useState(false)

    async function onSubmit(e: React.FormEvent) {
        e.preventDefault()
        setError(null)
        setOk(false)
        try {
            await api.post('/api/v1/auth/signup', {
                username,
                email,
                password,
                name: name || username,
                dob,
                timezone,
            })
            // Auto-login then redirect to dashboard
            const loginRes = await api.post('/api/v1/auth/login', { username, password })
            setToken(loginRes.data.access_token)
            navigate('/dashboard', { replace: true })
        } catch (err: any) {
            setError(err?.response?.data?.detail || 'Signup failed')
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
            <form onSubmit={onSubmit} className="bg-white/10 p-6 rounded w-[28rem]">
                <h1 className="text-2xl font-bold mb-4">Create account</h1>
                <div className="grid grid-cols-2 gap-3">
                    <input className="px-3 py-2 rounded bg-white/20" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
                    <input className="px-3 py-2 rounded bg-white/20" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                    <input className="px-3 py-2 rounded bg-white/20 col-span-2" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    <input className="px-3 py-2 rounded bg-white/20" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
                    <div>
                        <div className="text-xs mb-1 opacity-80">Date of birth</div>
                        <input className="w-full px-3 py-2 rounded bg-white/20" type="date" aria-label="Date of birth" value={dob} onChange={(e) => setDob(e.target.value)} required />
                    </div>
                    <input className="px-3 py-2 rounded bg-white/20 col-span-2" placeholder="Timezone" value={timezone} onChange={(e) => setTimezone(e.target.value)} />
                </div>
                {error && <p className="text-red-300 text-sm mt-3">{error}</p>}
                {ok && <p className="text-green-300 text-sm mt-3">Account created. You can login now.</p>}
                <button className="mt-4 w-full px-3 py-2 rounded bg-indigo-600 hover:bg-indigo-500">Sign up</button>
            </form>
        </div>
    )
}


