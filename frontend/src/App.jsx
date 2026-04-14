import { useState, useEffect, useRef } from 'react'
import { io } from 'socket.io-client'
import TitleCard from './TitleCard'
import TableResults from './TableResults'
import Filter from './Filter'

function App() {
  const [awards, setAwards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ 
    type: ['All'], 
    level: ['All'], 
    affiliation: ['All'], 
    faculty: ['All'], 
    program: ['All'], 
    term: ['All'], 
    citizenship: ['All']
  });
  const excelDownloadURL = useRef(null);
  const tableRef = useRef(null);
  const socket = io('https://uwaterloobursary.app/ws')
  const [scrapeStatus, setScrapeStatus] = useState('false');

  const fetchAwards = async () => {
    try {
      setLoading(true);
      setError(null);
      setAwards([]);
      
      const res = await fetch('/bursary/table', {
        method: 'GET'
      });

      if (!res.ok) throw new Error('Failed to Search');
      const data = await res.json();
      setAwards(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      tableRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  };
  
  const queryAwards = async () => {
    try {
      setLoading(true);
      setError(null);
      setAwards([]);

      const res = await fetch('/bursary/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filters})
      });

      if (!res.ok) throw new Error('Failed to fetch');
      const data = await res.json();
      setAwards(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const exportAwards = async () => {
    try {
      setLoading(true);
      setError(null);

      const res = await fetch('/bursary/sheet', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filters})
      });

      if (!res.ok) throw new Error('Failed to fetch');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob); 
      excelDownloadURL.current.href = url;
      excelDownloadURL.current.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);      
      fetchAwards();
    }
  };

  useEffect(() => {
    fetchAwards()
  }, [])

  useEffect(() => {
    if (awards.length > 0) {
      tableRef.current?.scrollIntoView({behavior: 'smooth' });
    }
  }, [awards]);

  useEffect(() => {
    socket.on('scrape_status', (data) => {
      setScrapeStatus(data.status) //update status
      switch (scrapeStatus) {
        case 'true':
          setLoading(true)
        case 'false':
          setLoading(false)
          fetchAwards();
        case 'error':
          setError('Error with CRON Job, Contact Administration for support')
      }
    }) 
    return () => socket.off('scrape_status')
  }, [])

  return (
    <>
      <div className="min-h-screen bg-customblue-5 flex flex-col justify-center p-12 gap-5">
        <TitleCard/>
        <Filter filters={filters} setFilters={setFilters} fetchAwards={queryAwards} exportAwards={exportAwards}/>
        <a ref={excelDownloadURL} download="bursary_web_scraper_results.xlsx" className="hidden"/>
        <div ref={tableRef}>
          <TableResults awards={awards} loading={loading} error={error}/>
        </div>
      </div>
    </>
  )
}

export default App