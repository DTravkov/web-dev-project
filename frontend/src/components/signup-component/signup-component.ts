import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api-service';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth-service';

@Component({
  selector: 'app-signup-component',
  imports: [FormsModule],
  templateUrl: './signup-component.html',
  styleUrl: './signup-component.css',
})
export class SignupComponent {
  username = signal("");
  password = signal("");
  private api = inject(ApiService);
  private auth = inject(AuthService);
  private router = inject(Router);

  onSubmitPressed() {
    this.auth.postSignup(this.username(), this.password()).subscribe();
  }
  onRedirectPressed() {
    this.router.navigate(['/login']);
  }
}
