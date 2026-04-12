import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../services/auth-service';
import { ApiService } from '../../services/api-service';

@Component({
  selector: 'app-header-component',
  imports: [RouterLinkActive, RouterLink],
  templateUrl: './header-component.html',
  styleUrl: './header-component.css',
})
export class HeaderComponent {
  private router = inject(Router);
  private api = inject(ApiService);
  auth = inject(AuthService);

  userCanApprove = computed<boolean | null>(() => this.auth.isManager());

  onSignupClicked() {
    this.router.navigate(['/signup']);
  }
  onLoginClicked() {
    this.router.navigate(['/login']);
  }
  onDisciplineListClicked() {
    this.api.refreshDisciplines();
    this.router.navigate(['']);
  }
  onLogoutClicked() {
    this.auth.logout();
  }
  onOfferDisciplineClicked() {
    this.router.navigate(['/disciplines', 'offer']);
  }
  onApproveListClicked() {
    this.router.navigate(['/disciplines', 'approve-list']);
  }

}
