import * as React from "react";
import * as ReactDom from "react-dom/client";

export default class App extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return <h1>The Fu**ing Sorcerers</h1>;
    }
}

const appDiv = document.getElementById("root");
const root = ReactDom.createRoot(appDiv);
root.render(<App/>)
