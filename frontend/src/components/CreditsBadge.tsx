import { useEffect, useState } from 'react'
import { api } from '../lib/api'
import { useAuth } from '../store/auth'
import { useUsage } from '../store/usage'

export default function CreditsBadge() {
    const [text, setText] = useState<string>('')
    const { token } = useAuth()
    const { tick } = useUsage()

    useEffect(() => {
        let mounted = true
        async function load() {
            try {
                const res = await api.get('/api/v1/usage')
                if (!mounted) return
                if (res.data.kind === 'regen_credits') {
                    const cr = Number(res.data.credits_remaining ?? 0)
                    const at = Number(res.data.attempts ?? 0)
                    const remaining = Math.max(0, cr - at)
                    setText(`${remaining} credits`)
                } else {
                    setText(`${res.data.attempts ?? 0} attempts today`)
                }
            } catch {
                // silent
            }
        }
        if (token) {
            load()
        }
        const id = token ? setInterval(load, 30000) : (null as any)
        return () => {
            mounted = false
            if (id) clearInterval(id)
        }
    }, [token, tick])

    if (!token || !text) return null
    return (
        <span className="text-xs px-2 py-1 rounded-full bg-white/10">{text}</span>
    )
}


