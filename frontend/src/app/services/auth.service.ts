import { Injectable } from '@angular/core';
import {Router} from "@angular/router";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {LoginResponse} from "../models/login-response";
import Swal from "sweetalert2"

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:8001/auth';

  constructor(
    private http: HttpClient,
    private router: Router,
  ) { }


  login(email: string, password: string) {
    const headers = new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded  ');

    const body = new URLSearchParams();
    body.set('grant_type', 'password');
    body.set('username', email);
    body.set('password', password);
    body.set('scope', '');
    body.set('client_id', '');
    body.set('client_secret', '');

    return this.http.post<LoginResponse>(`${this.apiUrl}/token`,
      body.toString(),
      { headers: headers }
    );
  }

  register(email: string, password: string, fullName: string) {
    return this.http.post(`${this.apiUrl}/register`, {
      email: email,
      password: password,
      full_name: fullName
    });
  }

  setToken(token:string, role: string, tokenExpiration: number) {
    localStorage.setItem('token', token);
    localStorage.setItem('role', role);
    const expirationTime = new Date().getTime() + tokenExpiration * 1000;
    localStorage.setItem('token_expiration', expirationTime.toString());
  }

  getToken() :string | null{
    return localStorage.getItem('token');
  }

  getRole() :string | null {
    return localStorage.getItem('role');
  }

  isLoggedIn(): boolean {
    const token = this.getToken();
    if (!token) return false;

    const expiration = localStorage.getItem('token_expiration');
    if (expiration) {
      const isExpired = new Date().getTime() > parseInt(expiration);
      if (isExpired) {
        this.clearTokens();
        return false;
      }
    }
    return true;
  }

  clearTokens() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('token_expiration');
  }

  logout() {
    this.clearTokens();
    this.router.navigate(['/login']);
  }

  showSuccess(message:string){
    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: message,
      timer: 2000,
      showConfirmButton: false,
    });
  }

  showError(message: string) {
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: message,
    });
  }

  showLoading(title :string = 'Loading...') {
    Swal.fire({
      title: title,
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading();
      }
    });
  }

  closeLoading() {
    Swal.close();
  }
}
