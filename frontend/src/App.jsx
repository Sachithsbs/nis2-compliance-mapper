import { useMemo, useState } from "react";
import { PieChart, Pie, Tooltip, Legend } from "recharts";

const API = "http://127.0.0.1:8000/api/v1";

export default function App() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [threshold, setThreshold] = useState(0.5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analyze() {
    if (!file) return;

    try {
      setError("");
      setLoading(true);

      const fd = new FormData();
      fd.append("file", file);

      // Step 1 → submit file
      const r = await fetch(`${API}/analyze`, {
        method: "POST",
        body: fd
      });

      if (!r.ok) throw new Error("Analyze request failed");

      const { analysis_id } = await r.json();

      // Step 2 → fetch results
      const rr = await fetch(`${API}/results/${analysis_id}`);

      if (!rr.ok) throw new Error("Fetching results failed");

      const data = await rr.json();

      console.log("RESULT =", data);
      setAnalysis(data);
    } catch (e) {
      console.error(e);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  const findings = analysis?.findings || [];

  const filtered = useMemo(
    () => findings.filter(f => f.confidence >= threshold),
    [findings, threshold]
  );

  const chartData = useMemo(() => {
    const counts = {};
    filtered.forEach(f => {
      counts[f.nis2_domain] = (counts[f.nis2_domain] || 0) + 1;
    });
    return Object.entries(counts).map(([name, value]) => ({ name, value }));
  }, [filtered]);

  return (
    <div style={{ padding: 20, fontFamily: "system-ui" }}>
      <h2>NIS2 Multi-Source Compliance Mapper</h2>

      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={analyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {analysis && (
        <>
          <h3>Model</h3>
          <p>{analysis.model_metadata.model_name}</p>

          <h3>Confidence Threshold: {threshold}</h3>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={threshold}
            onChange={e => setThreshold(Number(e.target.value))}
          />

          <h3>Domain Distribution</h3>
          <PieChart width={400} height={300}>
            <Pie
              dataKey="value"
              data={chartData}
              cx="50%"
              cy="50%"
              outerRadius={80}
              label
            />
            <Tooltip />
            <Legend />
          </PieChart>

          <h3>Findings ({filtered.length})</h3>
          <table border="1" cellPadding="6" style={{ width: "100%" }}>
            <thead>
              <tr>
                <th>Text</th>
                <th>Control</th>
                <th>Domain</th>
                <th>Confidence</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((f, i) => (
                <tr key={i}>
                  <td>{f.source_text}</td>
                  <td>{f.identified_control}</td>
                  <td>{f.nis2_domain}</td>
                  <td>{(f.confidence * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

