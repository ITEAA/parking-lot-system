import { useState, useEffect } from "react";

function EntryForm({ onEntry, onExit, parkedCount, maxCapacity }) {
  const [entryPlate, setEntryPlate] = useState("");
  const [isCompact, setIsCompact] = useState(false);
  const [exitPlate, setExitPlate] = useState("");

  const handleEntrySubmit = (e) => {
    e.preventDefault();
    if (entryPlate.trim() && parkedCount < maxCapacity) {
      onEntry(entryPlate.trim(), isCompact);
      setEntryPlate("");
      setIsCompact(false);
    }
  };

  const handleExitSubmit = (e) => {
    e.preventDefault();
    if (exitPlate.trim()) {
      onExit(exitPlate.trim());
      setExitPlate("");
    }
  };

  return (
    <div>
      <h3>🚗 현재 주차 차량 수: {parkedCount} / {maxCapacity}</h3>
      {parkedCount >= maxCapacity && (
        <div style={{ color: "red" }}>⚠️ 만차입니다.</div>
      )}

      <form onSubmit={handleEntrySubmit}>
        <h2>입차</h2>
        <input
          type="text"
          placeholder="차량 번호 입력"
          value={entryPlate}
          onChange={(e) => setEntryPlate(e.target.value)}
          disabled={parkedCount >= maxCapacity}
        />
        <label>
          <input
            type="checkbox"
            checked={isCompact}
            onChange={(e) => setIsCompact(e.target.checked)}
            disabled={parkedCount >= maxCapacity}
          />
          경차
        </label>
        <button type="submit" disabled={parkedCount >= maxCapacity}>입차 등록</button>
      </form>

      <form onSubmit={handleExitSubmit}>
        <h2>출차</h2>
        <input
          type="text"
          placeholder="차량 번호 입력"
          value={exitPlate}
          onChange={(e) => setExitPlate(e.target.value)}
        />
        <button type="submit">출차 처리</button>
      </form>
    </div>
  );
}

export default EntryForm;
