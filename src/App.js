import "./App.css";
import { Routes, Route, Link } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/login" element={<div>This is login page!</div>}/>
        <Route path="/signup" />
      </Routes>
    </div>
  );
}

export default App;
