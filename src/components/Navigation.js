import React from "react";
import { Switch, Route, Link } from "react-router-dom";

import { Index } from "../pages/Index";
import { Help } from "../pages/Help";
import { Card, CardByNumber } from "../pages/Card";
import { Reading } from "../pages/Reading";
import { Terms } from "../pages/Term";

function NavLink({ name }) {
  return (
    <li className="pure-menu-item">
      <Link className="pure-menu-link" to={"/" + name.toLowerCase()}>
        {name}
      </Link>
    </li>
  );
}

export function Navigation() {
  return (
    <nav className="pure-menu pure-menu-horizontal">
      <NavLink name="Overzicht" />
      <NavLink name="Begrippen" />
      <NavLink name="Legging" />
      <NavLink name="Uitleg" />
    </nav>
  );
}

export function Routes() {
  return (
    <Switch>
      <Route path="/overzicht">
        <Index />
      </Route>
      <Route path="/begrippen">
        <Terms />
      </Route>
      <Route path="/legging">
        <Reading />
      </Route>
      <Route path="/card/number/:seqnr">
        <CardByNumber />
      </Route>
      <Route path="/card/:suite/:name">
        <Card />
      </Route>
      <Route path="/uitleg">
        <Help />
      </Route>
      <Route path="/">
        <Index />
      </Route>
    </Switch>
  );
}
