import React, { useState } from 'react';

export default function ExitForm({ refreshCount }) {
  const [carNumber, setCarNumber] = useState('');
  const [message, setMessage] = useState('');

  const handleExit = async () => {
    if (!carNumber) {
      setMessage('차량 번호를 입력하세요.');
      return;
    }
    try {
      const res = await fetch('http://localhost:5000/api/exit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ car_number: carNumber }),
      });
      const data = await res.json();
      setMessage(data.message);
      if(data.status === 'success') {
        setCarNumber('');
        refreshCount();
      }
    } catch (error) {
      setMessage('서버 오류가 발생했습니다.');
      console.error(error);
    }
  };

  return (
    <div>
      <h2>출차 등록</h2>
      <input
        type="text"
        placeholder="차량 번호"
        value={carNumber}
        onChange={(e) => setCarNumber(e.target.value)}
      />
      <button onClick={handleExit}>출차</button>
      <p>{message}</p>
    </div>
  );
}
