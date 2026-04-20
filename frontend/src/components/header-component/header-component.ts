import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth-service';
import { ApiService } from '../../services/api-service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-header-component',
  imports: [FormsModule, RouterLink],
  templateUrl: './header-component.html',
  styleUrl: './header-component.css',
})
export class HeaderComponent {
  private router = inject(Router);
  private api = inject(ApiService);
  auth = inject(AuthService);

  login = signal("");
  password = signal("");
  errMessage = signal("");

  userCanApprove = computed<boolean | null>(() => this.auth.isManager());
  loginStarted = signal(false);

  onSignupClicked() {
    this.auth.postSignup(this.login(), this.password()).subscribe(
      {
        next: (resp) => {
          window.location.reload();
        },
        error: (err) => {
          const body: Object | undefined | null = err.error;
          if (!body) {
            this.errMessage.set("Unknown error");
            return;
          }
          this.errMessage.set(Object.values(body)[0]);
        }
      }
    );
  }
  onLoginClicked() {
    this.auth.postLogin(this.login(), this.password()).subscribe(
      {
        next: (resp) => {
          window.location.reload();
        },
        error: (err) => {
          const body: Object | undefined | null = err.error;
          console.log(err.error);
          if (!body) {
            this.errMessage.set("Unknown error");
            return;
          }
          this.errMessage.set(Object.values(body)[0]);
        }
      }
    );
  }
  onDisciplineListClicked() {
    this.api.refreshDisciplines();
    this.router.navigate(['/disciplines']);
  }
  onLogoutClicked() {
    this.auth.logout();
  }
  // onOfferDisciplineClicked() {
  //   this.router.navigate(['/disciplines', 'offer']);
  // }
  // onApproveListClicked() {
  //   this.router.navigate(['/disciplines', 'approve-list']);
  // }

}
