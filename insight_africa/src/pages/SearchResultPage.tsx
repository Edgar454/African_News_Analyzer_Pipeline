// pages/SearchResultsPage.tsx
import { useLocation } from 'react-router-dom';
import { useNews } from '../utils/api';
import Header from '../components/Header/RegularHeader';
import NewsCard from '../components/NewsContent/ui/NewsCard';

export default function SearchResultsPage() {
  const { data: news, isLoading, error } = useNews();
  const location = useLocation();

  const queryParams = new URLSearchParams(location.search);
  const rawQuery = queryParams.get('q') || '';
  const searchQuery = rawQuery.trim().toLowerCase();

  const tokenize = (text: string) =>
    text
      .toLowerCase()
      .normalize('NFD') // remove accents
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s]/gi, ' ') // remove punctuation
      .split(/\s+/)
      .filter(Boolean);

  const queryTokens = tokenize(searchQuery);

  const matchesQuery = (text: string) => {
    const textTokens = tokenize(text);
    const matchCount = queryTokens.filter((word) => textTokens.includes(word)).length;
    return matchCount / queryTokens.length >= 0.6; // match at least 60% of words
  };

  const results =
    news?.filter(
      (article) =>
        matchesQuery(article.title) ||
        matchesQuery(article.content)
    ) || [];

  return (
    <div className="relative flex size-full min-h-screen flex-col bg-white overflow-x-hidden" style={{ fontFamily: 'Newsreader, Noto Sans, sans-serif' }}>
      <Header />

      <main className="px-40 flex flex-1 flex-col py-5">
        <div className="max-w-[960px]">
          <h1 className="text-[#131416] text-[32px] font-bold leading-tight mb-4">
            🔍 Résultats pour : <span className="text-[#1e40af]">{rawQuery}</span>
          </h1>

          {isLoading ? (
            <div className="flex justify-center items-center py-20">
              <svg className="animate-spin h-8 w-8 text-gray-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
              </svg>
            </div>
          ) : error ? (
            <p className="text-red-600">Erreur lors du chargement des articles</p>
          ) : results.length === 0 ? (
            <p className="text-gray-600 text-base italic">Aucun résultat pour « {rawQuery} »</p>
          ) : (
            <div className="flex flex-col gap-3">
              {results.map((item) => (
                <NewsCard key={item.id} item={item} />
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
