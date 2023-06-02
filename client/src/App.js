import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState([{}]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    fetch("/members")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
        setLoaded(true);
      });
  }, []);

  return (
    <div>
      {!loaded ? (
        <p>Loading...</p>
      ) : (
        data.members.map((d, i) => <p key={i}>{d}</p>)
      )}
    </div>
  );
}

export default App;
