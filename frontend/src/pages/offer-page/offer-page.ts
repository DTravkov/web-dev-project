import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api-service';
import { AuthService } from '../../services/auth-service';

@Component({
  selector: 'app-offer-page',
  imports: [FormsModule],
  templateUrl: './offer-page.html',
  styleUrl: './offer-page.css',
})
export class OfferPage {
  private api = inject(ApiService);
  currentComment = signal<string>("");
  errorMsg = signal<string | null>(null);

  clearErrorMsg() {
    this.errorMsg.set(null)
  }
  onSubmitClicked() {
    this.api.postPending(this.currentComment()).subscribe({
      next: (value) => {
        this.errorMsg.set("Sent successfully!");
        this.currentComment.set("");
      },
      error: (err) => {
        if (err.status === 400) {
          this.errorMsg.set("Discipline with such name already exists.");
        }
      }
    });
  }
}
