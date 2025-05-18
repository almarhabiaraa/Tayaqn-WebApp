import { Component } from '@angular/core';
import { Router } from '@angular/router';
import {AuthService} from "../../services/auth.service";
import Swal from "sweetalert2";


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  email = '';
  password = '';

  constructor(private authService: AuthService, private router: Router) {}

  public onLogin() {

    this.authService.showLoading();
    this.authService.login(this.email, this.password).subscribe({
      next: (res) => {
        Swal.close();
        this.authService.showSuccess('Logged in successfully!');
        this.authService.setToken(res.access_token, res.role, res.exp);
        this.authService.showSuccess('Logged in successfully!');
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.authService.closeLoading();
        this.authService.showError(err.error.detail || 'Login error');
        this.authService.showError(err.error.detail || 'Login error');
      },
    });
  }

}
