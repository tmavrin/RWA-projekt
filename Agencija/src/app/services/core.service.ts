import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { User } from '../VO/User';

@Injectable({
  providedIn: 'root'
})
export class CoreService {

  private backendUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) { }

  getAllUsers() {
    return this.http.get(this.backendUrl + '/users');
  }

  getUserByUsername(username: string) {
    return this.http.get(this.backendUrl + '/users', {params: {username}});
  }

  addUser(user: User) {
    const httpParams = new HttpParams()
      .append('username', user.username)
      .append('password', user.password);
    const headers = new HttpHeaders();
    headers.set('Content-Type', 'application/json; charset=utf-8');
    return this.http.post(this.backendUrl + '/users', httpParams, {headers});
  }

  changeUserPassword(user: User) {
    const httpParams = new HttpParams()
      .append('username', user.username)
      .append('password', user.password);
    const headers = new HttpHeaders();
    headers.set('Content-Type', 'application/json; charset=utf-8');
    return this.http.put(this.backendUrl + '/users', httpParams, {headers});
  }

  deleteUser(username: string) {
    return this.http.delete(this.backendUrl + '/users/' + username);
  }
}
