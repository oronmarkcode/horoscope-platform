import { create } from 'zustand'

type AuthState = {
    token: string | null
    setToken: (t: string | null) => void
    logout: () => void
}

export const useAuth = create<AuthState>((set) => ({
    token: typeof localStorage !== 'undefined' ? localStorage.getItem('token') : null,
    setToken: (t) => {
        if (t) localStorage.setItem('token', t)
        else localStorage.removeItem('token')
        set({ token: t })
    },
    logout: () => {
        localStorage.removeItem('token')
        set({ token: null })
        window.location.href = '/'
    },
}))


