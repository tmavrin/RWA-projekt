export class User {
  username: string;
  password: string;
  jwtToken: string;
  role: string;

  constructor(username, jwtToken) {
    this.username = username;
    this.jwtToken = jwtToken;
  }
}
