import { useState } from 'react'
import FilterDropdown from './FilterDropdown'
import {TYPE, LEVEL, AFFILIATION, FACULTY, PROGRAM, TERM, CITIZENSHIP} from './constants'

function Filter({filterUpdate, fetchAwards, ingestAwards, exportAwards}) {
  const [filters, setFilters] = useState({ 
    type: ['All'], 
    level: ['All'], 
    affiliation: ['All'], 
    faculty: ['All'], 
    program: ['All'], 
    term: ['All'], 
    citizenship: ['All']
  });

  function handleChange(change) {
    const updated = { ...filters, [change.name]: change.selected };
    setFilters(updated);
    filterUpdate(updated);
  }

  return (
    <div className="rounded-xl bg-customblue-3/70 p-7">
      <div className="p-7 flex flex-wrap gap-5 justify-around">
        <FilterDropdown label="Award Type" name="type" options={TYPE} selected={filters.type} onChange={handleChange} />
        <FilterDropdown label="Level" name="level" options={LEVEL} selected={filters.level} onChange={handleChange} />
        <FilterDropdown label="Affiliation" name="affiliation" options={AFFILIATION} selected={filters.affiliation} onChange={handleChange} />
        <FilterDropdown label="Faculty" name="faculty" options={FACULTY} selected={filters.faculty} onChange={handleChange} />
        <FilterDropdown label="Program" name="program" options={PROGRAM} selected={filters.program} onChange={handleChange} />
        <FilterDropdown label="Term" name="term" options={TERM} selected={filters.term} onChange={handleChange} />
        <FilterDropdown label="Citizenship" name="citizenship" options={CITIZENSHIP} selected={filters.citizenship} onChange={handleChange} />
      </div>

      <div className="flex justify-around gap-5">
        <div className="group relative m-5 flex justify-center">
          <button className="font-syne text-customblue-5 text-sm rounded-full mb-5 border border-customblue-5/20 p-5 bg-customblue-4 grow"
          onClick={fetchAwards}>
              Fetch Awards
          </button>
          <span className="absolute top-12 scale-0 rounded bg-gray-800 p-2 text-xs text-white group-hover:scale-100">
            Select filters and load related awards
          </span>
        </div>

        <div className="group relative m-5 flex justify-center">
          <button className="font-syne text-customblue-5 text-sm rounded-full mb-5 border border-customblue-5/20 p-5 bg-customblue-4 grow"
          onClick={ingestAwards}>
              Refresh Award Data
          </button>
          <span className="absolute top-12 scale-0 rounded bg-gray-800 p-2 text-xs text-white group-hover:scale-100">Reingest and rescrape all award data</span>
        </div>

        <div className="group relative m-5 flex justify-center">
          <button className="font-syne text-customblue-5 text-sm rounded-full mb-5 border border-customblue-5/20 p-5 bg-customblue-4 grow"
          onClick={exportAwards}>
            Export Data
          </button>
          <span className="absolute top-12 scale-0 rounded bg-gray-800 p-2 text-xs text-white group-hover:scale-100">Export queried award data to excel file</span>
        </div>


      </div>
    </div>
  )
}

export default Filter