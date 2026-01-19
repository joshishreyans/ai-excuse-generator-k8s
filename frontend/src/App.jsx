import { useState } from "react";
import { generateExcuse } from "./api";

export default function App() {
  const [tone, setTone] = useState("funny");
  const [days, setDays] = useState(1);
  const [excuse, setExcuse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setExcuse("");

    try {
      const res = await generateExcuse(tone, days);
      setExcuse(res.excuse);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>AI Leave Excuse Generator</h1>

      <form onSubmit={handleSubmit}>
        <label>
          Tone:
          <select value={tone} onChange={(e) => setTone(e.target.value)}>
            <option value="funny">Funny</option>
            <option value="corporate">Corporate</option>
            <option value="absurd">Absurd</option>
            <option value="Like a 10-year-old">Like a 10-year-old</option>
          </select>
        </label>

        <br /><br />

        <label>
          Number of days:
          <input
            type="number"
            min="1"
            max="30"
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
          />
        </label>

        <br /><br />

        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Excuse"}
        </button>
      </form>

      <br />

      {error && <p style={{ color: "red" }}>{error}</p>}

      {excuse && (
        <div style={{ marginTop: 20, padding: 15, border: "1px solid #ccc" }}>
          <strong>Your excuse:</strong>
          <p>{excuse}</p>
        </div>
      )}
    </div>
  );
}
