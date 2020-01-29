import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { User } from './VO/User';
import { Offer } from './VO/Offer';

@Injectable({
  providedIn: 'root'
})
export class CoreService {
  private backendUrl = 'http://178.238.232.172:8080';

  constructor(private http: HttpClient) {}

  login(user: User) {
    const headers = new HttpHeaders();
    headers.set('Content-Type', 'application/json; charset=utf-8');
    return this.http.post(this.backendUrl + '/auth', user, { headers });
  }

  register(user: User) {
    const headers = new HttpHeaders();
    headers.set('Content-Type', 'application/json; charset=utf-8');
    return this.http.post(this.backendUrl + '/register', user, { headers });
  }

  getNumberOfOffers() {
    return this.http.get(this.backendUrl + '/offers-count');
  }

  getOffersByPage(pageNo: number, itemNo = 3, searchQuery = '', priceSort?) {
    let params;
    if (priceSort !== undefined) {
      params = new HttpParams()
        .append('pageNo', String(pageNo))
        .append('itemNo', String(itemNo))
        .append('q', searchQuery)
        .append('price', priceSort ? '0' : '1');
    } else {
      params = new HttpParams()
        .append('pageNo', String(pageNo))
        .append('itemNo', String(itemNo))
        .append('q', searchQuery);
    }
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

  uploadPdf(id: string, pdf: File) {
    const formData = new FormData();
    formData.append('pdf', pdf, pdf.name);
    const params = new HttpParams().append('id', id);
    return this.http.post(this.backendUrl + '/pdf', formData, { params });
  }

  uploadImage(id: string, image: File) {
    const formData = new FormData();
    formData.append('pdf', image, image.name);
    const params = new HttpParams().append('id', id);
    return this.http.post(this.backendUrl + '/image', formData, { params });
  }
}
