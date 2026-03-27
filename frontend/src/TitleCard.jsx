import { useState, useEffect } from 'react'

function TitleCard() {
  // const [count, setCount] = useState(0)

  return (
    <>
        <div className = "shadow-lg outline outline-black/5">
            <h1 className="font-syne font-bold text-center text-7xl leading-tight mb-6">
            <span className="text-customblue-3">University of Waterloo</span> <br />
            <span className="text-customblue-2">Bursary and Awards<br />Database</span>
            </h1>
            <p className="font-dm text-customblue-3 text-center text-lg mb-10">
            Friendly UI-alternative for parsing and viewing <br />
            <a className="text-customblue-4 text-lg max-w-lg leading-relaxed mb-10 hover:text-blue-800 visited:text-purple-600" 
            href="https://uwaterloo.ca/student-awards-financial-aid/awards/database">
              UWaterloo Undergraduate Awards Database
            </a>
            </p>
        </div>
    </>
  )
}

export default TitleCard