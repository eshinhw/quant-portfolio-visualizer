import React from "react";
import NavBarDark from "../components/Navbar";
import styled from "styled-components";

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

let ExtendedButton = styled.button(GeneralBtn) // use the same style of GeneralBtn

export default function HomePage() {
  return (
    <>
      <GeneralBtn bg="blue">Button</GeneralBtn>
      <ExtendedButton>Hello</ExtendedButton>
      <BlackBox>Hello</BlackBox>
      <NavBarDark />
    </>
  );
}
