import React from "react";

import { cards } from "../db";
import { Page } from "../components/Page";
import { Layout } from "../components/Layout";

export function Home(props) {
  return (
    <Page className="container" title="Tarot">
      <Layout cards={cards()} />
    </Page>
  );
}
