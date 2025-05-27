import React, { useState, useEffect } from 'react';

export default function SearchLogs() {
  const [carNumber, setCarNumber] = useState('');
  const [logs, setLogs] = useState([]);
  const [currentCars, setCurrentCars] = useState([]);
  const [message, setMessage] = useState('');
  const [isAllLogs, setIsAllLogs] = useState(false);

  // 주차 중인 차량 목록 초기 로드
  useEffect(() => {
    fetchCurrentCars();
  }, []);

  const fetchCurrentCars = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/parking/current');
      const data = await res.json();
      if (data.status === 'success') {
        setCurrentCars(data.cars);
      }
    } catch (error) {
      console.error('주차 중 차량 조회 실패:', error);
    }
  };

  const handleSearch = async () => {
    if (!carNumber) {
      setMessage('차량 번호를 입력하세요.');
      setLogs([]);
      setIsAllLogs(false);
      return;
    }
    try {
      const res = await fetch(`http://localhost:5000/api/logs?car_number=${carNumber}`);
      const data = await res.json();
      if (data.status === 'success') {
        setLogs(data.logs);
        setMessage('');
        setIsAllLogs(false);
      } else {
        setMessage(data.message);
        setLogs([]);
      }
    } catch (error) {
      setMessage('서버 오류가 발생했습니다.');
      console.error(error);
    }
  };

  const handleFetchAllLogs = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/logs/all');
      const data = await res.json();
      if (data.status === 'success') {
        setLogs(data.logs);
        setMessage('');
        setIsAllLogs(true);
      } else {
        setMessage('전체 기록을 불러오는 데 실패했습니다.');
        setLogs([]);
      }
    } catch (error) {
      setMessage('서버 오류가 발생했습니다.');
      console.error(error);
    }
  };

  return (
    <div>
      <h2>출입 기록 조회</h2>
      <input
        type="text"
        placeholder="차량 번호 입력"
        value={carNumber}
        onChange={(e) => setCarNumber(e.target.value)}
      />
      <button onClick={handleSearch}>조회</button>
      <button onClick={handleFetchAllLogs} style={{ marginLeft: 10 }}>
        전체 기록 조회
      </button>
      {message && <p>{message}</p>}

      {logs.length > 0 && (
        <table border="1" cellPadding="5" style={{ marginTop: 10, width: '100%' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>차량 번호</th>
              <th>차량 종류</th>
              <th>입차 시간</th>
              <th>출차 시간</th>
              <th>요금(원)</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td>{log.id}</td>
                <td>{log.car_number}</td>
                <td>{log.car_type}</td>
                <td>{log.entry_time}</td>
                <td>{log.exit_time || (isAllLogs ? '-' : '')}</td>
                <td>{log.fee !== undefined ? log.fee : (isAllLogs ? '-' : '')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h2 style={{ marginTop: 40 }}>주차 중인 차량 목록</h2>
      {currentCars.length === 0 ? (
        <p>현재 주차 중인 차량이 없습니다.</p>
      ) : (
        <table border="1" cellPadding="5" style={{ marginTop: 10, width: '100%' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>차량 번호</th>
              <th>차량 종류</th>
              <th>입차 시간</th>
            </tr>
          </thead>
          <tbody>
            {currentCars.map((car) => (
              <tr key={car.id}>
                <td>{car.id}</td>
                <td>{car.car_number}</td>
                <td>{car.car_type}</td>
                <td>{car.entry_time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
