import React, { useState } from 'react';

export default function ParkingForm({ refreshCount }) {
  const [carNumber, setCarNumber] = useState('');
  const [carType, setCarType] = useState('');
  const [message, setMessage] = useState('');

  const handlePark = async () => {
    if (!carNumber || !carType) {
      setMessage('차량 번호와 차량 종류를 입력하세요.');
      return;
    }
    try {
      const res = await fetch('http://localhost:5000/api/park', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ car_number: carNumber, car_type: carType }),
      });
      const data = await res.json();
      setMessage(data.message);
      if(data.status === 'success') {
        setCarNumber('');
        setCarType('');
        refreshCount();
      }
    } catch (error) {
      setMessage('서버 오류가 발생했습니다.');
      console.error(error);
    }
  };

  return (
    <div>
      <h2>입차 등록</h2>
      <input
        type="text"
        placeholder="차량 번호"
        value={carNumber}
        onChange={(e) => setCarNumber(e.target.value)}
      />
      <select value={carType} onChange={(e) => setCarType(e.target.value)}>
        <option value="">차량 종류 선택</option>
        <option value="승용차">승용차</option>
        <option value="SUV">SUV</option>
        <option value="경차">경차</option>
        <option value="기타">기타</option>
      </select>
      <button onClick={handlePark}>입차</button>
      <p>{message}</p>
    </div>
  );
}
