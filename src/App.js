import React from "react";
import { Routes, Route, Link, Outlet } from "react-router-dom";
import HomePage from "./pages/HomePage";


function App() {
  return (
    <div className="App">
      <HomePage />
      <Routes>
        <Route path="/" element={HomePage} />
        <Route path="/login" element={<div>This is login page!</div>} />
        <Route path="/signup" />
        <Route path="*" element={<div>404 Not Found</div>} />
        <Route path="event" element={<Event />}>
          <Route path="one" element={<div>First order free shipping!</div>}/>
          <Route path="two" element={<div>Second order $100 coupon!</div>}/>
        </Route>
      </Routes>
    </div>
  );
}

function Event() {
  return (
    <>
      <p>This is Event Page.</p>
      <Outlet></Outlet>
    </>
  );
}

export default App;
