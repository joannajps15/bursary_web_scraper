import { useState } from 'react'
import TableAwardEntry from './TableAwardEntry'

function TableResults({awards, loading, error}) {
    const ITEMS_PER_PAGE = 25;
    const [page, setPage] = useState(0);

    const totalPages = Math.ceil(awards.length / ITEMS_PER_PAGE);
    const start = page * ITEMS_PER_PAGE;
    const visible = awards.slice(start, start + ITEMS_PER_PAGE);

    if (loading) return (        
        <div className="m-12 flex items-center justify-center text-customblue-2">
            <p className="text-center text-3xl mr-3">Loading</p>
            <svg className="mr-3 size-10 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
        </div>
    )

    if (error) return <p className="text-red-400">Error: {error}</p>

    return (
        <div className="overflow-x-auto rounded-xl bg-customblue-4/20 p-7">
            {Array.isArray(visible) && visible.map((award, idx) => (
                <TableAwardEntry idx={idx} data={award}
                key={idx}>
                </TableAwardEntry>
            ))}
        
            <div className="text-slate-50 flex flex-wrap gap-1.5 mt-4">
                <button
                onClick={() => setPage(p => p - 1)}
                disabled={page === 0}
                className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg disabled:opacity-30 hover:bg-gray-50"
                >
                ← Prev
                </button>

                {Array.from({ length: totalPages }, (_, i) => (
                <button
                    key={i}
                    onClick={() => setPage(i)}
                    className={`px-3 py-1.5 text-sm border rounded-lg text-black
                    ${i === page
                        ? 'border-gray-400 font-medium bg-customblue-2'
                        : 'border-gray-200 hover:bg-gray-50 bg-sky-200'
                    }`}
                >
                    {i + 1}
                </button>
                ))}

                <button
                onClick={() => setPage(p => p + 1)}
                disabled={page === totalPages - 1}
                className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg disabled:opacity-30 hover:bg-gray-50"
                >
                Next →
                </button>
            </div>
        </div>
    )
}

export default TableResults