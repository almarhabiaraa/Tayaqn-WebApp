// register.component.ts
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
})
export class RegisterComponent {
  email = '';
  password = '';
  fullName = '';

  constructor(private authService: AuthService, private router: Router) {}

  onRegister() {
    this.authService.showLoading();
    this.authService.register(this.email, this.password, this.fullName).subscribe({
      next: (res) => {
        this.authService.closeLoading();
        this.authService.showSuccess('Registered successfully!');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.authService.closeLoading();
        this.authService.showError(err.error.detail || 'Register error');
      },
    });
  }
}
