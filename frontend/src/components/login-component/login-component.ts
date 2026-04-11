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
  private api = inject(ApiService);
  private auth = inject(AuthService);
  private router = inject(Router);

  username = signal<string>("");
  password = signal<string>("");
  errMessage = signal<string>("");
  onSubmitPressed() {
    this.auth.postLogin(this.username(), this.password()).subscribe(
      {
        next: (resp) => this.router.navigate(['']),
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
  onRedirectPressed() {
    this.router.navigate(['/signup']);
  }
}
