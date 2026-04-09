import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth-service';

@Component({
  selector: 'app-header-component',
  imports: [],
  templateUrl: './header-component.html',
  styleUrl: './header-component.css',
})
export class HeaderComponent {
  private router = inject(Router);
  auth = inject(AuthService);

  onSignupClicked() {
    this.router.navigate(['/signup']);
  }
  onLoginClicked() {
    this.router.navigate(['/login']);
  }
  onLogoClicked() {
    this.router.navigate(['']);
  }
  onLogoutClicked() {
    this.auth.logout();
  }
}
