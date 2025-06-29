import FilterButton from './ui/FilterButton';

const categoryOptions = [
  'All',
  'Politics',
  'Economy',
  'Entertainment',
  'Science/Tech',
  'Sports',
  'Faits divers',
];

const dateOptions = ['Newest First', 'Oldest First'];

const sourceOptions = ['All', 'Reuters', 'CNN', 'BBC', 'Al Jazeera'];

// Define prop types for the component
interface NewsFiltersProps {
  onCategoryChange: (category: string | null) => void;
  onDateChange: (date: string | null) => void;
  onSourceChange: (source: string | null) => void;
  selectedCategory: string | null;
  selectedDate: string | null;
  selectedSource: string | null;
}


export default function NewsFilters({
  onCategoryChange,
  onDateChange,
  onSourceChange,
  selectedCategory,
  selectedDate,
  selectedSource,
}: NewsFiltersProps) {
  return (
    <div className="flex gap-3 p-3 flex-wrap pr-4">
      <FilterButton
        label="Category"
        options={categoryOptions}
        onSelect={onCategoryChange}
        selected={selectedCategory}
      />
      <FilterButton
        label="Date"
        options={dateOptions}
        onSelect={onDateChange}
        selected={selectedDate}
      />
      <FilterButton
        label="Source"
        options={sourceOptions}
        onSelect={onSourceChange}
        selected={selectedSource}
      />
    </div>
  );
}
