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
import { User } from './VO/User';

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
    if (this.shouldAddToken(request)) {
      if (this.authService.currentUserValue) {
        request = request.clone({
          headers: new HttpHeaders({
            Authorization: this.authService.currentUserValue.jwtToken
          })
        });
      }
    }

    return next.handle(request);
  }

  shouldAddToken(req: HttpRequest<any>) {
    const addr = req.url.split('/')[3];
    if (
      (addr === 'offers' ||
        addr === 'top-offers' ||
        addr === 'image' ||
        addr === 'pdf' ||
        addr === 'offers-count') &&
      req.method === 'GET'
    ) {
      return false;
    } else {
      return true;
    }
  }
}
