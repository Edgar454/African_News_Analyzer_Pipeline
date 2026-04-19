export default function NewsHeader() {
  return (
    <div className="flex flex-wrap justify-between gap-3 p-4">
      <div className="flex min-w-72 flex-col gap-3">
        <p className="text-[#131416] tracking-light text-[32px] font-bold leading-tight">Recent News</p>
        <p className="text-[#6b7580] text-sm font-normal leading-normal">
          Stay updated with the latest developments across Africa.
        </p>
      </div>
    </div>
  );
}