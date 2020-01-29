export class User {
  username: string;
  password: string;
  jwtToken: string;
  role: string;

  constructor(username, password) {
    this.username = username;
    this.password = password;
  }
}
