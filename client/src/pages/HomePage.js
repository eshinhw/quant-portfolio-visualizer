import React, { useEffect, useState } from "react";
import styled from "styled-components";
import StockInput from "../components/StockInput";
import NavBar from "../components/Navbar";

// why use back tick?
let YellowBtn = styled.button`
  background: yellow;
  color: black;
  padding: 10px;
`;

let BlackBox = styled.div`
  background: blue;
  color: white;
  padding: 25px;
`;

let GeneralBtn = styled.button`
  background: ${(props) => props.bg};
  color: ${(props) => (props.bg == "blue" ? "white" : "black")};
  padding: 10px;
`;

let ExtendedButton = styled.button(GeneralBtn); // use the same style of GeneralBtn

export default function HomePage() {
  let [alert, setAlert] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setAlert(false);
    }, 2000);
  });
  return (
    <>
      <NavBar />
      <StockInput />
    </>
  );
}
