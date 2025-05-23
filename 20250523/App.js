import React, { useState, useEffect } from 'react';
import ParkingForm from './components/ParkingForm';
import ExitForm from './components/ExitForm';
import SearchLogs from './components/SearchLogs';

function App() {
  const [currentCount, setCurrentCount] = useState(0);

  // 현재 주차 차량 수 조회
  const fetchCurrentCount = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/current_count');
      const data = await res.json();
      if(data.status === 'success') {
        setCurrentCount(data.current_parking_count);
      }
    } catch (error) {
      console.error('Error fetching current count:', error);
    }
  };

  useEffect(() => {
    fetchCurrentCount();
  }, []);

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: 20 }}>
      <h1>주차 관리 시스템</h1>
      <p>현재 주차 차량 수: {currentCount}대</p>
      <ParkingForm refreshCount={fetchCurrentCount} />
      <hr />
      <ExitForm refreshCount={fetchCurrentCount} />
      <hr />
      <SearchLogs />
    </div>
  );
}

export default App;
