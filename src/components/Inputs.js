import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";

function SymbolInput() {
  let [symbol, setSymbol] = useState("");

  const onChangeInput = (e) => {
    console.log(e);
    setSymbol(e.currentValue);
  };

  return (
    <>
      <InputGroup className="mb-3">
        <Form.Control placeholder="Type Stock Symbol" onChange={onChangeInput} value={symbol} />
        <Button variant="outline-secondary" id="button-addon2">
          Add
        </Button>
      </InputGroup>
    </>
  );
}

export default SymbolInput;
