import { useEffect, useState } from "react";
import EntryForm from "./components/EntryForm";
import ParkedList from "./components/ParkedList";

function App() {
  const [vehicles, setVehicles] = useState([]);
  const API = "http://localhost:5000";
  const MAX_CAPACITY = 10;

  const fetchParked = async () => {
    const res = await fetch(`${API}/parked`);
    const data = await res.json();
    setVehicles(data);
  };

  const handleEntry = async (plate, isCompact) => {
    if (vehicles.length >= MAX_CAPACITY) {
      alert("⚠️ 만차입니다. 입차할 수 없습니다.");
      return;
    }
    await fetch(`${API}/entry`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plate_number: plate, is_compact: isCompact }),
    });
    fetchParked();
  };

  const handleExit = async (plate) => {
    const res = await fetch(`${API}/exit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plate_number: plate }),
    });
    const data = await res.json();
    alert(`출차 완료 - 요금: ${data.fee}원`);
    fetchParked();
  };

  useEffect(() => {
    fetchParked();
  }, []);

  return (
    <div>
      <h1>차량 입출차 시스템</h1>
      <EntryForm
        onEntry={handleEntry}
        onExit={handleExit}
        parkedCount={vehicles.length}
        maxCapacity={MAX_CAPACITY}
      />
      <ParkedList vehicles={vehicles} maxCapacity={MAX_CAPACITY} />
    </div>
  );
}

export default App;
