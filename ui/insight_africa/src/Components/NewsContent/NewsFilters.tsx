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

export default function NewsFilters({ onCategoryChange, onDateChange, onSourceChange, selectedCategory, selectedDate, selectedSource }) {
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
