import React from "react";
import { BrowserRouter as Router } from "react-router-dom";

import { Navigation, Routes } from "./components/Navigation";

export default function App() {
  return (
    <Router>
      <Navigation />
      <Routes />
    </Router>
  );
}
