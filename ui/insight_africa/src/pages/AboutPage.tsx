import Header from '../Components/Header/RegularHeader'
import AboutContent from '../Components/AboutPage/AboutContent'

export default function About() {
  return (
    <div
      className="relative flex size-full min-h-screen flex-col bg-white group/design-root overflow-x-hidden"
      style={{ fontFamily: 'Newsreader, "Noto Sans", sans-serif' }}
    >
      <div className="layout-container flex h-full grow flex-col">
        <Header />
        <AboutContent />
      </div>
    </div>
  )
}
