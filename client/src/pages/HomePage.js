import React, { useEffect, useState } from "react";
import NavBarDark from "../components/Navbar";
import styled from "styled-components";
import SymbolInput from "../components/Inputs";

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
      {/* {alert ? (
        <GeneralBtn id="btn" bg="blue">
          Button
        </GeneralBtn>
      ) : null} */}

      {/* <ExtendedButton>Hello</ExtendedButton>
      <BlackBox>Hello</BlackBox> */}
      <NavBarDark />
      <SymbolInput />
    </>
  );
}
