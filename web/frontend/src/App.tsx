import * as React from 'react';
import { Tabs, Row, Col, Layout, Button, Modal, Input, Form, message } from 'antd';
import { displayError } from './utils';

const FormItem = Form.Item;
const DOMAINROOT = 'http://localhost:80';
const { localStorage } = window;

import {
  BrowserRouter as Router,
  Route, Link, Redirect
} from 'react-router-dom';

import './App.css';

import { Home } from './Home';
import { AnalysisBuilder } from './Builder';

const { Footer, Content, Header } = Layout;

interface AppState {
  loggedIn: boolean;
  openLogin: boolean;
  openSignup: boolean;
  email: string | null;
  password: string | null;
  jwt: string | null;
  nextURL: string | null; // will probably remove this and find a better solution to login redirects
}

const Browse = () => (
  <Row type="flex" justify="center">
    <Col span={16}>
      <h2>Browser Public Analyses</h2>
    </Col>
  </Row>
);

class App extends React.Component<{}, AppState>{
  constructor(props) {
    super(props);
    window.localStorage.clear()
    const jwt = localStorage.getItem('jwt');
    this.state = {
      loggedIn: !!jwt,
      openLogin: false,
      openSignup: false,
      email: localStorage.getItem('email'),
      jwt: jwt,
      password: '',
      nextURL: null
    };
  }

  authenticate = () => new Promise((resolve, reject) => {
    const { email, password } = this.state;
    fetch(DOMAINROOT + '/api/auth', {
      method: 'post',
      body: JSON.stringify({ email: email, password: password }),
      headers: {
        'Content-type': 'application/json'
      }
    })
      .then((response) => {
        response.json().then((data: { access_token: string }) => {
          if (data.access_token) {
            message.success('Authentication successful');
            window.localStorage.setItem('jwt', data.access_token);
            resolve(data.access_token);
          } else {
            reject('Authentication failed');
          }
        });
      })
      .catch(displayError);
  });

  login = () => {
    const { email, password, loggedIn, openLogin, nextURL } = this.state;
    return this.authenticate()
      .then((jwt: string) => {
        this.setState({
          jwt: jwt, password: '', loggedIn: true, openLogin: false, nextURL: null
        }, () => { if (nextURL) document.location.href = nextURL });
      })
      .catch(displayError);
  }

  logout = () => {
    localStorage.removeItem('jwt');
    localStorage.removeItem('email');
    this.setState({ loggedIn: false, email: null, jwt: null });
  }

  // loginAndNavigate = (nextURL: string) => {
  //   if (this.state.loggedIn) {
  //     document.location.href = nextURL;
  //     return;
  //   }
  //   this.setState({ openLogin: true, nextURL });
  // }

  // ensureLoggedIn = () => new Promise((resolve, reject) => {
  //   if (this.state.loggedIn) {
  //     resolve();
  //   } else {
  //     this.setState({ openLogin: true });
  //     this.login().then(() => resolve()).catch(() => reject());
  //   }
  // });

  render() {
    const { loggedIn, email, openLogin, openSignup, password } = this.state;
    const loginModal = (
      <Modal
        title="Log into Neuroscout"
        visible={openLogin}
        footer={null}
        maskClosable={true}
        onCancel={e => { this.setState({ openLogin: false }); }}
      >
        <p>{"For development try 'test2@test.com' and 'password'"}</p><br />
        <Form>
          <FormItem>
            <Input placeholder="Email"
              type="email"
              size="large"
              value={email}
              onChange={(e: any) => this.setState({ email: e.target.value })}
            />
          </FormItem>
          <FormItem>
            <Input placeholder="Password"
              type="password"
              value={password}
              onChange={(e: any) => this.setState({ password: e.target.value })}
            />
          </FormItem>
          <FormItem>
            <Button
              style={{ width: '100%' }}
              type="primary"
              onClick={e => { this.login(); }}
            >Log in</Button>
          </FormItem>
        </Form>
      </Modal>
    );
    return (
      <Router>
        <div>
          {openLogin && loginModal}
          <Layout>
            <Header style={{ background: '#fff', padding: 0 }}>
              <Row type="flex" justify="center">
                <Col span={12}>
                  <h1><a href="/">Neuroscout</a></h1>
                </Col>
                <Col span={4}>
                  {loggedIn ?
                    <span>{`Logged in as ${email}`}
                      <Button onClick={e => this.logout()}>Log out</Button>
                    </span> :
                    <Button onClick={e => this.setState({ openLogin: true })}>Log in</Button>}
                </Col>
              </Row>
            </Header>
            <Content style={{ background: '#fff' }}>
              <Route exact path="/" render={(props) => <Home />} />
              <Route path="/builder" render={(props) => <AnalysisBuilder />} />
              <Route exact path="/browse" component={Browse} />
            </Content>
            <Footer style={{ background: '#fff' }}>
              <Row type="flex" justify="center">
                <Col span={4}>
                  <br />
                  <p>Neuroscout - Copyright 2017</p>
                </Col>
              </Row>
            </Footer>
          </Layout>
        </div>
      </Router >
    );
  }
}

const init = () => {
  // window.localStorage.clear(); // Dev-only, will remove later once there is user/password prompt functionality
};

init();
export default App;
