import React, { Component } from 'react';
import './App.css';

class App extends Component {
  state = {"users": []};

  componentDidMount() {
    fetch('/users/list').then(res => res.json()).then(users => this.setState(users));
  }

  render() {
    console.log(this.state);
    return (
      <div>
        {this.state.users}
      </div>
    );
  }
}

export default App;
