import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import NewsPage from './pages/NewsPage'
import NewsDetailPage from './pages/NewsDetailsPage'
import AboutPage from './pages/AboutPage'
import WeeklySummaryPage from './pages/WeeklySummaryPage'
import ComparisonPage from './pages/ComparisonPage'
import SearchResultsPage from './pages/SearchResultPage';


export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/news" element={<NewsPage />} />
      <Route path="/news/:id" element={<NewsDetailPage />} />
      <Route path="/about" element={<AboutPage />} />
      <Route path="/summary" element={<WeeklySummaryPage />} />
      <Route path="/compare" element={<ComparisonPage />} />
      <Route path="/search" element={<SearchResultsPage />} />
    </Routes>
  )
}
