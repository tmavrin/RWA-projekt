import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { User } from './VO/User';
import { Offer } from './VO/Offer';

@Injectable({
  providedIn: 'root'
})
export class CoreService {

  private backendUrl = 'http://178.238.232.172:8080';

  constructor(private http: HttpClient) { }

  getAllUsers() {
    return this.http.get(this.backendUrl + '/users');
  }
  // TODO FIX
  getUserByUsername(username: string) {
    return this.http.get(this.backendUrl + '/users', {params: { username }});
  }

  addUser(user) {
    const httpParams = new HttpParams()
      .append('username', user.username)
      .append('password', user.password);
    const headers = new HttpHeaders();
    headers.set('Content-Type', 'application/json; charset=utf-8');
    return this.http.post(this.backendUrl + '/users', user, {headers});
  }

/*   changeUserPassword(user: User) {
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
*/
  getOffersByPage(pageNo: number, itemNo = 3) {
    const params = new HttpParams()
      .append('pageNo', String(pageNo))
      .append('itemNo', String(itemNo));
    return this.http.get(this.backendUrl + '/offers', { params });
  }

  addOffer(offer: Offer) {
    const headers = new HttpHeaders();
    headers.set('Content-Type', 'application/json; charset=utf-8');
    return this.http.post(this.backendUrl + '/offers', offer, { headers });
  }

  editOffer(offer: Offer) {
    const headers = new HttpHeaders();
    headers.set('Content-Type', 'application/json; charset=utf-8');
    return this.http.put(this.backendUrl + '/offers', offer, { headers });
  }

  deleteOffer(id: string) {
    const params = new HttpParams().append('id', id);
    return this.http.delete(this.backendUrl + '/offers', { params });
  }

  getTopList() {
    return this.http.get(this.backendUrl + '/top-offers');
  }

  addOfferToTopList(id: string) {
    const params = new HttpParams().append('id', id);
    return this.http.post(this.backendUrl + '/top-offers', {}, { params });
  }

  removeOfferFromTopList(id: string) {
    const params = new HttpParams().append('id', id);
    return this.http.delete(this.backendUrl + '/top-offers', { params });
  }
}
