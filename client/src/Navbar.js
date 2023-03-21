import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";

export default function NavBar() {
  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="/">Trading Automated</Navbar.Brand>
          <Nav className="ml-auto">
            <Nav.Link href="/sector-etf">Sector Analysis</Nav.Link>
            <Nav.Link href="/price-alert">Price Alert</Nav.Link>
            <Nav.Link href="/screener">Screener</Nav.Link>
            <Nav.Link href="/position-calculator">Position Calculator</Nav.Link>
            <Nav.Link href="/login">Log In</Nav.Link>
            <Nav.Link href="/signup">Sign Up</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </>
  );
}
