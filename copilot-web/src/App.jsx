import { useEffect, useState } from "react";

function App() {
  const [incidents, setIncidents] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/incidents")
      .then((res) => res.json())
      .then((data) => setIncidents(data))
      .catch((err) => console.error(err));
  }, []);

  const loadIncidentDetails = async (id) => {
    try {
      const res = await fetch(`http://localhost:8000/incidents/${id}`);
      const data = await res.json();
      setSelectedIncident(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div
      style={{
        padding: "20px",
        maxWidth: "1000px",
        margin: "0 auto",
      }}
    >
      <h1 style={{ textAlign: "center" }}>On-Call Copilot</h1>

      <h2>Incidents</h2>

      {incidents.map((incident) => (
        <div
          key={incident.id}
          onClick={() => loadIncidentDetails(incident.id)}
          style={{
            border: "1px solid gray",
            padding: "10px",
            marginBottom: "10px",
            cursor: "pointer",
          }}
        >
          <h3>{incident.title}</h3>
          <p>Status: {incident.status}</p>
          <p>ID: {incident.id}</p>
        </div>
      ))}

      {selectedIncident && (
        <div
          style={{
            marginTop: "30px",
            border: "2px solid white",
            padding: "20px",
          }}
        >
          <h2>Incident Details</h2>

          <h3>{selectedIncident.incident.title}</h3>

          <p>
            Status: {selectedIncident.incident.status}
          </p>

          <hr />

          <h3>Timeline</h3>

          {selectedIncident.events.length === 0 ? (
            <p>No events found</p>
          ) : (
            selectedIncident.events.map((event, index) => (
              <div
                key={index}
                style={{
                  borderLeft: "3px solid #666",
                  paddingLeft: "10px",
                  marginBottom: "10px",
                }}
              >
                <strong>{event.type}</strong>
                <br />
                Source: {event.source}
                <br />
                Title: {event.title}
                <br />
                Time: {event.occurred_at}
              </div>
            ))
          )}

          <hr />

          <h3>Insights</h3>

          {selectedIncident.insights.length === 0 ? (
            <p>No insights generated</p>
          ) : (
            selectedIncident.insights.map((insight, index) => (
              <div
                key={index}
                style={{
                  marginBottom: "10px",
                }}
              >
                • {insight.title}
              </div>
            ))
          )}

          <hr />

         <h3 style={{ color: "red" }}>
🚀 AI Analysis Working
</h3>

          <div
            style={{
              border: "1px solid gray",
              padding: "15px",
              marginTop: "10px",
              borderRadius: "8px",
            }}
          >
            <p>
              <strong>Summary:</strong>
              <br />
              {selectedIncident.ai_analysis?.summary}
            </p>

            <p>
              <strong>Possible Cause:</strong>
              <br />
              {selectedIncident.ai_analysis?.possible_cause}
            </p>

            <p>
              <strong>Recommendation:</strong>
              <br />
              {selectedIncident.ai_analysis?.recommendation}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;