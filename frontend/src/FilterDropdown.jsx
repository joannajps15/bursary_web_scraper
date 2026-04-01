import { useState } from 'react';

function FilterDropdown({ label, name, options, selected, onChange }) {
  const [open, setOpen] = useState(false);

  function toggle(value) {
    if (selected.length === 0) selected = ['All'];
    else if (value === 'All') selected = (selected.includes('All')) ? [] : ['All']; //all selected
    else {
        //select
        if (!selected.includes(value)) {
            selected = selected.filter(opt => opt !== 'All');
            selected.push(value);
        } 
        else selected = selected.filter(opt => opt !== value); //deselect
    }
    onChange({name:name, selected:selected});
  }

  const triggerText = selected.length == 0 ? `Select ${label}` : selected.length == 1 ? selected[0] : selected[0]+'...';

  return (
    <div className="flex flex-col gap-2 text-customblue-1">
        {/* Filter Label */}
        <span className="text-xs font-medium uppercase tracking-widest text-sky-300 font-syne">
            {label}
        </span>

        {/* Trigger */}
        <button
            onClick={() => setOpen(openStatus => !openStatus)} //toggle open status 
            className="flex items-center justify-between gap-2 p-3.5 rounded-xl bg-white/10 border border-white/20 hover:bg-white/15 transition-colors">
            <span className="w-25 truncate text-left text-sm text-blue-100">{triggerText}</span>
            <svg className={`w-3.5 h-3.5 transition-transform ${open ? 'rotate-180' : ''}`} viewBox="0 0 16 16" fill="none">
                <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
        </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute z-15 mt-19 h-43 bg-slate-800 border border-white/15 rounded-xl overflow-auto">
          {['All', ...options].map(opt => (
            <div
              key={opt}
              onClick={() => toggle(opt)}
              className="flex items-center gap-2.5 p-3.5 cursor-pointer hover:bg-white/10"
            >
              <div className={`z-15 w-4 h-4 rounded flex items-center justify-center border-[1.5px] transition-colors
                ${selected.includes(opt) ? 'bg-sky-500 border-sky-500' : 'border-white/30'}`}>
                {selected.includes(opt) && (
                  <svg viewBox="0 0 10 8" className="w-2.5 h-2.5" fill="none">
                    <path d="M1 4l3 3 5-6" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </div>
              <span className="text-sm">{opt}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default FilterDropdown