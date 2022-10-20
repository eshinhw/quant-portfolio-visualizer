import { Table } from "react-bootstrap";
import { useSelector } from "react-redux";

export default function Cart() {
  let a = useSelector((state) => {return state})
  console.log(a)
  return (
    <>
      <Table>
        <thead>
          <tr>
            <th>1</th>
            <th>2</th>
            <th>3</th>
            <th>4</th>
          </tr>

        </thead>
        <tbody>
          <tr>
            <th>5</th>
            <th>6</th>
            <th>7</th>
            <th>8</th>
          </tr>
        </tbody>



      </Table>
    
    </>

  )
}