import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import HomePage from "./pages/HomePage";
// import HomePage from "./pages/Homepage.js";

function App() {
  return (
    <div className="App">
      <HomePage/>
      <Routes>
        {/* <Route path="/" element={HomePage} /> */}
        <Route path="/login" element={<div>This is login page!</div>} />
        <Route path="/signup" />
      </Routes>
    </div>
  );
}

export default App;
