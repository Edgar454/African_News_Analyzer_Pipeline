import { useParams, useNavigate } from 'react-router-dom'
import Header from '../components/Header/RegularHeader'
import { useNews } from '../utils/api'

const NewsDetailPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: news, error, isLoading } = useNews()

  const article = news?.find((n) => n.id.toString() === id)

  return (
    <div
      className="relative flex size-full min-h-screen flex-col bg-white group/design-root overflow-x-hidden"
      style={{ fontFamily: 'Newsreader, "Noto Sans", sans-serif' }}
    >
      <Header />

      <main className="px-40 flex flex-1 justify-center py-5">
        <div className="max-w-[960px] flex-1">
          <div className="flex flex-wrap gap-2 p-4">
            <span className="text-[#6b7580] text-base font-medium">News</span>
            <span className="text-[#6b7580] text-base font-medium">/</span>
            <span className="text-[#131416] text-base font-medium">Article</span>
          </div>

          <div className="flex flex-wrap justify-between gap-3 p-4">
            <div className="flex min-w-72 flex-col gap-3">

              {/* Loading Indicator */}
              {isLoading && (
                <div className="flex justify-center items-center py-20">
                  <svg
                    className="animate-spin h-8 w-8 text-gray-600"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                    ></path>
                  </svg>
                </div>
              )}

              {/* Error */}
              {error && <p className="text-red-600">Error loading article</p>}

              {/* Article not found */}
              {!isLoading && !error && !article && (
                <p>Article not found</p>
              )}

              {/* Article content */}
              {!isLoading && !error && article && (
                <>
                  <p className="text-[#131416] text-[32px] font-bold leading-tight">{article.title}</p>
                  <p className="text-[#6b7580] text-sm">
                    Published on {new Date(article.published_date).toLocaleDateString()} | Category: {article.category}
                  </p>
                  <div
                    className="text-[#131416] text-base font-normal leading-normal pb-3 pt-1 px-4 [&_a]:underline [&_strong]:font-semibold [&_ul]:list-disc [&_li]:ml-6"
                    dangerouslySetInnerHTML={{ __html: article.content }}
                  />
                </>
              )}

            </div>

            {!isLoading && article && (
              <button
                onClick={() => navigate('/news')}
                className="min-w-[84px] max-w-[480px] rounded-xl h-10 px-4 bg-[#f1f2f3] text-[#131416] text-sm font-bold tracking-[0.015em]"
              >
                Back to News
              </button>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default NewsDetailPage
