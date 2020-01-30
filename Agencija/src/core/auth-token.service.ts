import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpHeaders
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthTokenService implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    /*

    request = request.clone({
      headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    });

    */
    if (this.authService.currentUserValue) {
      request = request.clone({
        headers: new HttpHeaders({
          Authorization: this.authService.currentUserValue.jwtToken
        })
      });
    }
  //  console.log(request);
    return next.handle(request);
  }
}
