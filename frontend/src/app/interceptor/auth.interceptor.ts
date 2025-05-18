import { Injectable } from '@angular/core';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpHeaders, HttpErrorResponse
} from '@angular/common/http';
import {catchError, Observable} from 'rxjs';
import { AuthService } from '../services/auth.service';
import Swal from "sweetalert2";
import {Router} from "@angular/router";

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService, private router: Router) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.authService.getToken();
    if (req.url.includes('/api') && token) {
      const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
      const authReq = req.clone({ headers });
      return next.handle(authReq).pipe(
        catchError((error:HttpErrorResponse)=>{
          if (error.status === 401) {
            this.handleAuthError();
          }
          throw error;
        })
      );
    }
    return next.handle(req);
  }

  private handleAuthError(): void {
    this.authService.clearTokens();

    Swal.fire({
      title: 'Session Expired',
      text: 'Your session has expired. Please log in again.',
      icon: 'warning',
      confirmButtonText: 'OK'
    }).then((result) => {
      if (result.isConfirmed) {
        this.router.navigate(['/login']);
      }
    });
  }
}
