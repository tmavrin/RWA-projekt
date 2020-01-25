import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class OfferService {
  private backendUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  public getAllOffers() {
    const headers = new HttpHeaders();
    headers.set('Content-Type', 'application/json; charset=utf-8');
    return this.http.get(this.backendUrl + '/offers');
  }
}
