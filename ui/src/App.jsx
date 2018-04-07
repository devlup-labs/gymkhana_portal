import React from "react"
import {render} from "react-dom"

import AppContainer from "./containers/AppContainer"

class App extends React.Component {
    render() {
        return (
            <AppContainer/>
        )
    }
}

render(<App1/>, document.getElementById('App'))