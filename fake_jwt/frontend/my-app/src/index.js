import React from 'react';
import ReactDOM from 'react-dom';
import ApiService from './http';

class Input extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      val: "",
    }
  }

  render() {
    return (
      <div>
        <label>{this.props.labelName}</label>
        <input type={this.props.inputType} id={this.props.id} onChange={this.props.onInputChange} />
      </div>
    )
  }
}

class LoginForm extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      username: "",
      password: "",
    }
  }

  setUsername(e) {
    this.setState({ username: e.target.value })
  }

  setPassword(e) {
    this.setState({ password: e.target.value })
  }

  doLogin() {
    const service = new ApiService()
    service.login(this.state.username, this.state.password)
  }

  render() {
    return (
      <div className="col">
        <Input id="username" labelName="Username" inputType="text" onInputChange={(e) => this.setUsername(e)} />
        <Input id="password" labelName="Password: " inputType="password" onInputChange={(e) => this.setPassword(e)} />
        <button onClick={() => this.doLogin()}>Login</button>
      </div>
    );
  }
}

class MainBoard extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div className="col">
        <h1>MyApp</h1>
        <LoginForm />
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <MainBoard />,
  document.getElementById('root')
)
