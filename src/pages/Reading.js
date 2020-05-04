import React from "react";

import { cards, cleanRecords } from "../db";
import { Thumbnail, CardInfo } from "../components/Card";
import { Page } from "../components/Page";

function shuffleFisherYates(array) {
  let i = array.length;
  while (i--) {
    const ri = Math.floor(Math.random() * (i + 1));
    [array[i], array[ri]] = [array[ri], array[i]];
  }
  return array;
}

function FormRow({ label, onChange, ...props }) {
  return (
    <tr>
      <td>{label}</td>
      <td>
        <input {...props} onChange={e => onChange(e.target)} />
      </td>
    </tr>
  );
}

export function Reading() {
  const [size, setSize] = React.useState(3);
  const [reversed, setReversed] = React.useState(false);
  const [majors, setMajors] = React.useState(false);
  const [reading, setReading] = React.useState([]);
  const [info, setInfo] = React.useState(-1);

  function draw() {
    setInfo(-1);
    var shuffled = cards();
    if (majors) {
      shuffled = shuffled.filter({ suite: "groot" });
    }
    shuffled = shuffleFisherYates(shuffled.get());
    setReading(cleanRecords(shuffled.splice(0, size)));
  }

  return (
    <Page title="Legging">
      {reading.length > 0 && (
        <div style={{ marginBottom: "20pt", display: "flex" }}>
          {reading.map((card, nr) => (
            <div
              key={nr}
              style={{
                marginLeft: "10pt"
              }}
            >
              <Thumbnail {...card} height="300pt" onClick={e => setInfo(nr)} />
            </div>
          ))}
        </div>
      )}
      {info >= 0 && <CardInfo {...reading[info]} />}
      <table className="pure-table" style={{ marginTop: "20pt" }}>
        <tbody>
          <FormRow
            type="number"
            label="Aantal kaarten"
            value={size}
            onChange={({ value }) => setSize(value)}
          />
          <FormRow
            type="checkbox"
            label="Ondersteboven"
            checked={reversed}
            onChange={({ checked }) => setReversed(checked)}
          />
          <FormRow
            type="checkbox"
            label="Alleen Grote Arcana"
            checked={majors}
            onChange={({ checked }) => setMajors(checked)}
          />
          <FormRow
            type="button"
            label=""
            value="Nieuwe legging"
            onClick={draw}
          />
        </tbody>
      </table>
    </Page>
  );
}
