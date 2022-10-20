import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";

function SymbolCard(props) {
  return (
    <Card style={{ width: "18rem" }}>
      {/* <Card.Img variant="top" src="holder.js/100px180" /> */}
      <Card.Body>
        <Card.Title>{props.symbol}</Card.Title>
        <Card.Text>{props.description}</Card.Text>
        <Button variant="primary">Learn More</Button>
      </Card.Body>
    </Card>
  );
}

export default SymbolCard;
