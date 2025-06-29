// pages/NewsPage.tsx
import { useState } from 'react'
import { useNews } from '../utils/api'
import Header from '../components/Header/RegularHeader'
import NewsFilters from '../components/NewsContent/NewsFilters'
import NewsCard from '../components/NewsContent/ui/NewsCard'
import Pagination from '../components/NewsContent/Pagination'

export default function NewsPage() {
  const { data: news, error, isLoading } = useNews()

  const [page, setPage] = useState(1)
  const pageSize = 5

  const [categoryFilter, setCategoryFilter] = useState<string | null>(null)
  const [dateFilter, setDateFilter] = useState<string | null>(null)
  const [sourceFilter, setSourceFilter] = useState<string | null>(null)

  let sortedNews = [...(news || [])];
    if (dateFilter === 'Newest First') {
      sortedNews.sort((a, b) => new Date(b.published_date).getTime() - new Date(a.published_date).getTime());
    } else if (dateFilter === 'Oldest First') {
      sortedNews.sort((a, b) => new Date(a.published_date).getTime() - new Date(b.published_date).getTime());
    }

const filteredNews = sortedNews.filter((article) => {
  const matchCategory = !categoryFilter || article.category === categoryFilter;
  const matchSource = !sourceFilter || article.source === sourceFilter;
  return matchCategory && matchSource;
});


  const paginated = filteredNews.slice((page - 1) * pageSize, page * pageSize)
  const totalPages = Math.ceil(filteredNews.length / pageSize)

  return (
    <div className="relative flex size-full min-h-screen flex-col bg-white group/design-root overflow-x-hidden" style={{ fontFamily: 'Newsreader, "Noto Sans", sans-serif' }}>
      <Header />

      <main className="px-40 flex flex-1 flex-col py-5">
        <div className="max-w-[960px]">
          <h1 className="text-[#131416] text-[32px] font-bold leading-tight mb-4">All News</h1>
          <NewsFilters
            onCategoryChange={(category) => setCategoryFilter(category)}
            onDateChange={(date) => setDateFilter(date)}
            onSourceChange={(source) => setSourceFilter(source)}
            selectedCategory={categoryFilter}
            selectedDate={dateFilter}
            selectedSource={sourceFilter}
          />


          {isLoading ? (
            <div className="flex justify-center items-center py-20">
              <svg className="animate-spin h-8 w-8 text-gray-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
              </svg>
            </div>
          ) : error ? (
            <p className="text-red-600">Error loading news</p>
          ) : (
            <div className="flex flex-col gap-3">
              {paginated.map((item) => (
              <NewsCard key={item.id} item={item} />
            ))}
            </div>
          )}
          <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
        </div>
      </main>
    </div>
  )
}
