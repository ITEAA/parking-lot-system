function ParkedList({ vehicles, maxCapacity }) {
  return (
    <div>
      <h2>주차 중인 차량 목록 ({vehicles.length} / {maxCapacity})</h2>
      <ul>
        {vehicles.map((v) => (
          <li key={v.plate_number}>
            {v.plate_number} - 입차 시간: {new Date(v.entry_time).toLocaleString()} - {v.is_compact ? "경차" : "일반"}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ParkedList;
