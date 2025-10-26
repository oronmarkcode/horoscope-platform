import { create } from 'zustand'

type UsageState = {
    tick: number
    bump: () => void
}

export const useUsage = create<UsageState>((set) => ({
    tick: 0,
    bump: () => set((s) => ({ tick: s.tick + 1 })),
}))


