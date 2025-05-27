import React, { useState, useEffect } from 'react';
import ParkingForm from './components/ParkingForm';
import ExitForm from './components/ExitForm';
import SearchLogs from './components/SearchLogs';

function App() {
  const [currentCount, setCurrentCount] = useState(0);
  const [maxCapacity, setMaxCapacity] = useState(0); // maxCapacity 상태 추가

  const fetchCurrentCount = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/current_count');
      const data = await res.json();
      if (data.status === 'success') {
        setCurrentCount(data.current_parking_count);
      }
    } catch (error) {
      console.error('Error fetching current count:', error);
    }
  };

  const fetchMaxCapacity = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/max_capacity');
      const data = await res.json();
      if (data.status === 'success') {
        setMaxCapacity(data.max_capacity);
      }
    } catch (error) {
      console.error('Error fetching max capacity:', error);
    }
  };

  useEffect(() => {
    fetchCurrentCount();
    fetchMaxCapacity(); // 🔥 추가된 fetch 요청
  }, []);

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: 20 }}>
      <h1>주차 관리 시스템</h1>
      <p>현재 주차 차량 수: {currentCount} / {maxCapacity}대</p>
      <ParkingForm refreshCount={fetchCurrentCount} />
      <hr />
      <ExitForm refreshCount={fetchCurrentCount} />
      <hr />
      <SearchLogs />
    </div>
  );
}

export default App;
