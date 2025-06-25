// components/Layout/InsightsSidebar.tsx
import { FaListUl, FaProjectDiagram, FaShareAlt, FaHashtag } from 'react-icons/fa';

interface NavItem {
  label: string;
  icon: React.ComponentType;
  id: string;
}

const navItems: NavItem[] = [
  { label: 'Weekly Summary', icon: FaListUl, id: 'weekly-summary' },
  { label: 'Knowledge Graph', icon: FaProjectDiagram, id: 'knowledge-graph' },
  { label: 'Topic Modeling', icon: FaHashtag, id: 'topic-modeling' },
  { label: 'Network Analysis', icon: FaShareAlt, id: 'network-analysis' },
];

export default function InsightsSidebar() {
  const handleScrollTo = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <aside className="w-80 min-h-screen border-r border-gray-200 bg-white p-4">
      <div className="flex flex-col gap-2">
        {navItems.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => handleScrollTo(id)}
            className="flex items-center gap-3 px-3 py-2 rounded-full text-left transition-colors duration-200 text-gray-800 hover:bg-gray-100"
          >
            <span className="text-xl">
              <Icon />
            </span>
            <span className="text-sm leading-normal">{label}</span>
          </button>
        ))}
      </div>
    </aside>
  );
}
