import { create } from 'zustand';

type Toast = { id: number; message: string; type?: 'success' | 'error' }

type ToastState = {
    toasts: Toast[]
    push: (t: Omit<Toast, 'id'>) => void
    remove: (id: number) => void
}

export const useToast = create<ToastState>((set) => ({
    toasts: [],
    push: (t) =>
        set((s) => ({ toasts: [...s.toasts, { id: Date.now(), ...t }] })),
    remove: (id) => set((s) => ({ toasts: s.toasts.filter((x) => x.id !== id) })),
}))

export function ToastHost() {
    const { toasts, remove } = useToast()
    return (
        <div className="fixed top-4 right-4 z-50 space-y-2">
            {toasts.map((t) => (
                <div
                    key={t.id}
                    className={`px-4 py-2 rounded shadow text-white ${t.type === 'error' ? 'bg-rose-600' : 'bg-emerald-600'
                        }`}
                    onAnimationEnd={() => remove(t.id)}
                >
                    {t.message}
                </div>
            ))}
        </div>
    )
}


