import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api-service';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth-service';

@Component({
  selector: 'app-login-component',
  imports: [FormsModule],
  templateUrl: './login-component.html',
  styleUrl: './login-component.css',
})
export class LoginComponent {
  username = signal("");
  password = signal("");
  private api = inject(ApiService);
  private auth = inject(AuthService);
  private router = inject(Router);
  onSubmitPressed() {
    this.auth.postLogin(this.username(), this.password()).subscribe(
      {
        next: (resp) => this.router.navigate([''])
      }
    );
  }
  onRedirectPressed() {
    this.router.navigate(['/signup']);
  }
}
