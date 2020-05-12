import React from "react";
import PropTypes from "prop-types";

import { HashLink } from "react-router-hash-link";

import { findTerm } from "../db";
import { RawContent } from "./Content";

import "./Term.css";

export function TermLink({ name }) {
  return <HashLink to={"/begrippen#" + name}>{name}</HashLink>;
}

export function Term({ name, term, refs, nr }) {
  if (term === "UNDEFINED") {
    const definition = findTerm(name);
    if (!term) {
      console.warn(`No term for [${name}]`);
    } else {
      refs = definition.refs;
      term = definition.definition;
    }
  }
  return (
    <tr id={name} className="terms">
      <td>{name}</td>
      <td>
        <RawContent>{term}</RawContent>
      </td>
      <td>
        {refs && refs.length > 0 && (
          <>
            {refs
              .map(ref => <TermLink key={ref} name={ref} />)
              .map((link, nr) => [nr > 0 && ", ", link])}
          </>
        )}
      </td>
    </tr>
  );
}

Term.propTypes = {
  name: PropTypes.string.isRequired,
  term: PropTypes.string
};

Term.defaultProps = {
  term: "UNDEFINED",
  refs: []
};

export function Terms({ terms }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Begrip</th>
          <th>Definitie</th>
          <th>Zie ook</th>
        </tr>
      </thead>
      <tbody>
        {terms.map((term, nr) => {
          return <Term key={term.name} {...term} nr={nr} />;
        })}
      </tbody>
    </table>
  );
}
