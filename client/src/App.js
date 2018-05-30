import React, { Component } from 'react';
import axios from 'axios';
import './App.css';

class App extends Component {
  state = {"users": []};

  componentDidMount() {
    axios.get('api/users/list').then(res => console.log(res)).catch(err => console.log(err));
    // fetch('api/users/list').then(res => res.json()).then(users => this.setState(users));
  }

  render() {
    return (
      <div>
        Hello!World
      </div>
    );
  }
}

export default App;
