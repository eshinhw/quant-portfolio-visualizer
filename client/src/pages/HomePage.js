import React, { useEffect, useState } from "react";
import styled from "styled-components";
import StockInput from "../components/StockInput";
import NavBar from "../components/Navbar";

let GeneralBtn = styled.button`
  background: ${(props) => props.bg};
  color: ${(props) => (props.bg == "blue" ? "white" : "black")};
  padding: 10px;
`;

let ExtendedButton = styled.button(GeneralBtn); // use the same style of GeneralBtn

export default function HomePage() {

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
