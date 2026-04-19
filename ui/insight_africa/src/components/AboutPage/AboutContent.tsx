import SectionTitle from './ui/SectionTitle'
import Paragraph from './ui/Paragraph'
import IconGrid from './IconGrid'

const AboutContent = () => {
  return (
    <main className="px-40 flex flex-1 justify-center py-5">
      <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
        <div className="flex flex-wrap justify-between gap-3 p-4">
          <p className="text-[#131416] tracking-light text-[32px] font-bold leading-tight min-w-72">
            About Insight Africa
          </p>
        </div>

        <Paragraph>
          Insight Africa is a news intelligence dashboard focused on African current affairs. It provides weekly summaries,
          knowledge graphs, and network analysis to help users understand complex events and trends across the continent.
        </Paragraph>

        <SectionTitle>Use Cases</SectionTitle>
        <Paragraph>
          This dashboard can be used by journalists, researchers, policymakers, and anyone interested in African affairs to:
          <ul className="list-disc pl-6 mt-1">
            <li>Stay informed about the latest developments across different regions and countries.</li>
            <li>Identify key actors and their relationships in specific events or issues.</li>
            <li>Analyze trends and patterns in news coverage over time.</li>
            <li>Gain a deeper understanding of the context and dynamics of current events.</li>
          </ul>
        </Paragraph>

        <SectionTitle>Methodology</SectionTitle>
        <Paragraph>
          Our analysis is based on a combination of natural language processing (NLP) techniques, network analysis, and
          knowledge graph construction. We collect news articles from various sources, extract key entities and
          relationships, and visualize them in an interactive dashboard. Weekly summaries are generated using advanced
          summarization algorithms, providing concise overviews of the most important news of the week.
        </Paragraph>

        <SectionTitle>Contact</SectionTitle>
        <Paragraph>For any questions or feedback, please contact us at support@insightafrica.com.</Paragraph>

        <IconGrid />
      </div>
    </main>
  )
}

export default AboutContent
