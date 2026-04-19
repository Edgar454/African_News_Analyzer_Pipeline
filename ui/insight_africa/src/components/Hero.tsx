import { Link } from 'react-router-dom'

export default function Hero() {
  return (
    <div className="px-40 flex flex-1 justify-center py-5 container">
      <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
        <div className="p-4 @[480px]:p-4">
          <div
            className="flex min-h-[480px] flex-col gap-6 bg-cover bg-center bg-no-repeat @[480px]:gap-8 @[480px]:rounded-xl items-center justify-center p-4"
            style={{
              backgroundImage:
                "linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.4)), url('https://lh3.googleusercontent.com/aida-public/AB6AXuB14sYFEGPs4om51tyTA95zJDFVo1sRkEogwtWjQHHypd5oZamlbzfA7w0a7a5EloViNsM2KOyUFSEnMDFTjBi6THLdWPbfwtrWarOfxuXhQSky_Y0vpWuKGlIQhCBcQk3vjoayPCRlsiosNKfj9HYszPr_aDdA7jo-ShzRxSetPb8ZhOX6qoN0MvUsLNY_5wVB84UsH0rav0_DwtvHgFP9XQ35-eY5pA_oxwU0FQ4B29T9FWKfeLI6nQY2IoW9VMOKrWgogwRzED0')",
            }}
          >
            <div className="flex flex-col gap-2 text-center">
              <h1 className="text-white text-4xl font-black leading-tight tracking-[-0.033em] @[480px]:text-5xl @[480px]:font-black @[480px]:leading-tight @[480px]:tracking-[-0.033em]">
                Understand African Current Affairs
              </h1>
              <h2 className="text-white text-sm font-normal leading-normal @[480px]:text-base @[480px]:font-normal @[480px]:leading-normal">
                Get weekly summaries, knowledge graphs, and network analysis of African current affairs.
              </h2>
            </div>
            <div className="flex-wrap gap-3 flex justify-center">
              <Link
                to="/summary"
                className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 @[480px]:h-12 @[480px]:px-5 bg-[#b8cee4] text-[#131416] text-sm font-bold leading-normal tracking-[0.015em] @[480px]:text-base @[480px]:font-bold @[480px]:leading-normal @[480px]:tracking-[0.015em]"
              >
                <span className="truncate">Explore Summaries</span>
              </Link>
              <Link
                to="/news"
                className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 @[480px]:h-12 @[480px]:px-5 bg-[#f1f2f3] text-[#131416] text-sm font-bold leading-normal tracking-[0.015em] @[480px]:text-base @[480px]:font-bold @[480px]:leading-normal @[480px]:tracking-[0.015em]"
              >
                <span className="truncate">Browse News</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
