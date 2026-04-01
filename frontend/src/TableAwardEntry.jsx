import { useState } from 'react'

function TableAwardEntry({idx, data}) {
    const [open, setOpen] = useState(false);

    return (
        <div className="overflow-x-auto rounded-xl m-2 font-dm text-customblue-1">
            <div className={idx % 2 === 0 ? 'bg-customblue-5 p-10 ' : 'bg-customblue-4/20 p-10'}>
                {/* Trigger */}
                <div className="mb-5 flex flex-wrap items-start" 
                    onClick={() => setOpen(openStatus => !openStatus)}>
                    {/* award title, value, type */}
                    <div className="flex-1 font-syne">    
                        <a href={data[2]} className="text-customblue-3 text-lg">{data[1]}</a><br/>
                        <span className="text-customblue-2 text-sm">{data[5]}</span>
                    </div>
                    <div className="font-syne text-customblue-5 text-sm rounded-full border-1 border-customblue-4/20 p-3 bg-customblue-3">
                        {data[9][0].toUpperCase()}                        
                    </div>                
                    <svg className={`w-7 h-7 transition-transform ${open ? 'rotate-180' : ''}`} viewBox="0 0 16 16" fill="none">
                        <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                </div>
                
                {/* dropdown */}
                {open && (
                    <div>
                        {/* award description */}
                        <div className="mb-10">
                            <span>{data[6]}</span>
                        </div>
                        <div className="grid grid-cols-2 gap-2 ">
                            <div className="border-l border-slate-700 pl-6">
                                {/* Selection
                                Eligibility*/}   
                                {data[3] && 
                                    <>
                                        <span className="text-customblue-2 font-syne">Selection<br/></span>
                                        <span>{data[3]}<br/><br/></span>
                                    </>
                                }  
                                {data[7]?.length > 0 &&
                                    <>
                                        <span className="text-customblue-2 font-syne">Eligibility Criteria</span>
                                        <ul className="list-disc list-inside">
                                            {data[7]?.split(',').map((item, idx) => (
                                                <li key={idx}>{item.trim()}</li>
                                            ))}
                                        </ul>
                                    </>
                                }  
                            </div>
                            <div className="border-l border-slate-700 pl-6">
                                {/* Affil
                                Term
                                Levels
                                Programs
                                Citizenship */}
                                {data[12] && data[12] != "" &&
                                    <> 
                                        <span className="text-customblue-2 font-syne">Affiliation</span>
                                        {data[12].length == 1 ? <span><br/>{data[12][0]}<br/></span>
                                        : <ul className="list-disc list-inside">
                                            {data[12].map((item, idx) => (
                                                <li key={idx}>{item.trim()}</li>
                                            ))}
                                        </ul>}
                                        <br/>
                                    </>
                                }  
                                {data[11] && data[11] != "" &&
                                    <> 
                                        <span className="text-customblue-2 font-syne">Term</span>
                                        {data[11].length == 1 ? <span><br/>{data[11][0]}<br/></span>
                                        : <ul className="list-disc list-inside">
                                            {data[11].map((item, idx) => (
                                                <li key={idx}>{item.trim()}</li>
                                            ))}
                                        </ul>}
                                        <br/>
                                    </>
                                }
                                {data[8] &&
                                    <>
                                        <span className="text-customblue-2 font-syne">Level</span>
                                        {data[11].length == 1 ? <span><br/>{data[8][0]}<br/></span>
                                        : <ul className="list-disc list-inside">
                                            {data[8].map((item, idx) => (
                                                <li key={idx}>{item.trim()}</li>
                                            ))}
                                        </ul>}
                                        <br/>
                                    </>
                                }                                
                                {data[10] &&
                                    <>
                                        <span className="text-customblue-2 font-syne">Program</span>
                                        {data[11].length == 1 ? <span><br/>{data[10][0]}<br/></span>
                                        : <ul className="list-disc list-inside">
                                            {data[10].map((item, idx) => (
                                                <li key={idx}>{item.trim()}</li>
                                            ))}
                                        </ul>}
                                        <br/>
                                    </>
                                } 
                                {data[4] && 
                                    <> 
                                        <span className="text-customblue-2 font-syne">Citizenship<br/></span>
                                        <span>{data[4]}</span>
                                    </>
                                }
                            </div>
                        </div>
                    </div>
                )}

            </div>
        </div>
    )   
}

export default TableAwardEntry