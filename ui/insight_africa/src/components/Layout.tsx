import type { ReactNode } from 'react'
import Header from './Header/HomepageHeader'
import Footer from './Footer'

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div
      className="relative flex size-full min-h-screen flex-col bg-white group/design-root overflow-x-hidden"
      style={{ fontFamily: 'Newsreader, "Noto Sans", sans-serif' }}
    >
      <div className="layout-container flex h-full grow flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </div>
    </div>
  )
}
