import {Component, HostListener} from '@angular/core';
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrl: './nav.component.css'
})
export class NavComponent {
  isMenuOpen = false;

  constructor(
    private authService: AuthService,
  ) {
  }

  getRole() {
    return this.authService.getRole();
  }

  logout() {
    this.authService.logout();
  }

  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
  }

  @HostListener('window:resize')
  onResize() {
    if (window.innerWidth > 768) {
      this.isMenuOpen = false;
    }
  }

}
