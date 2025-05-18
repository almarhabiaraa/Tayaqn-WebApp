import {CanActivateFn, Router} from '@angular/router';
import {inject} from "@angular/core";
import {AuthService} from "../services/auth.service";

export const AdminGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isLoggedIn() && authService.getRole() === 'ADMIN') {
    return true;
  }

  authService.showError('You are not authorized to access this page');
  router.navigate(['/dashboard']);
  return false;
};
