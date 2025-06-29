import Header from '../components/Header/RegularHeader';
import CompareWeeklyMetrics from '../components/WeeklyComparison/CompareWeeklyMetrics';
import { useComparison } from '../utils/api';
import ReactMarkdown from 'react-markdown';

export default function ComparisonPage() {
  const { data: comparison, error } = useComparison();

  if (error) {
    return (
      <div className="relative flex size-full min-h-screen flex-col bg-white group/design-root overflow-x-hidden" style={{ fontFamily: 'Newsreader, "Noto Sans", sans-serif' }}>
        <div className="layout-container flex h-full grow flex-col">
          <Header />
          <main className="px-40 flex flex-1 justify-center py-5">
            <div className="layout-content-container flex flex-col max-w-[960px] flex-1 p-4 text-red-600 font-bold text-center">
              Error loading comparison data.
            </div>
          </main>
        </div>
      </div>
    );
  }

  const isLoading = !comparison;

  return (
    <div className="relative flex size-full min-h-screen flex-col bg-white group/design-root overflow-x-hidden" style={{ fontFamily: 'Newsreader, "Noto Sans", sans-serif' }}>
      <div className="layout-container flex h-full grow flex-col">
        <Header />

        <main className="px-40 flex flex-1 justify-center py-5">
          <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
            {/* Titre toujours affiché */}
            <div className="flex flex-wrap justify-between gap-3 p-4">
              <div className="flex min-w-72 flex-col gap-3">
                <p className="text-[#111518] tracking-light text-[32px] font-bold leading-tight">Weekly Snapshot Comparison</p>
                <p className="text-[#637688] text-sm font-normal leading-normal">
                  Compare two weekly snapshots of news to understand trends and shifts in the network.
                </p>
              </div>
            </div>

            {/* Contenu ou spinner */}
            {isLoading ? (
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
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                  />
                </svg>
              </div>
            ) : (
              <>
                <CompareWeeklyMetrics {...comparison} />

                <h2 className="text-[#111518] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
                  Network Shifts
                </h2>
                <div className="prose prose-sm max-w-none text-[#111518] pb-3 pt-1 px-4">
                  <ReactMarkdown>{comparison.summary}</ReactMarkdown>
                </div>
              </>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
