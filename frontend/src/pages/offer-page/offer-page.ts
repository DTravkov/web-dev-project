import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api-service';
import { AuthService } from '../../services/auth-service';
import { IPendingDiscipline } from '../../model/i-pending-discipline';

@Component({
  selector: 'app-offer-page',
  imports: [FormsModule, RouterLink],
  templateUrl: './offer-page.html',
  styleUrl: './offer-page.css',
})
export class OfferPage {
  api = inject(ApiService);
  auth = inject(AuthService);
  currentComment = signal<string>("");
  errorMsg = signal<string | null>(null);
  pendingDisciplines = signal<IPendingDiscipline[]>([]);

  constructor() {
    this.loadPendingDisciplines();
  }

  clearErrorMsg() {
    this.errorMsg.set(null)
  }

  loadPendingDisciplines() {
    if (!this.auth.isLoggedIn()) {
      this.pendingDisciplines.set([]);
      return;
    }

    const request = this.auth.isManager() ? this.api.getAllPending() : this.api.getMyPending();

    request.subscribe({
      next: (response) => {
        this.pendingDisciplines.set(response);
      },
      error: () => {
        this.pendingDisciplines.set([]);
      }
    });
  }

  onSubmitClicked() {
    this.api.postPending(this.currentComment()).subscribe({
      next: (value) => {
        this.errorMsg.set("Sent successfully!");
        this.currentComment.set("");
        this.loadPendingDisciplines();
      },
      error: (err) => {
        if (err.status === 400) {
          this.errorMsg.set("Discipline with such name already exists.");
          return;
        }
        this.errorMsg.set("Could not send your offer.");
      }
    });
  }

  onApproveClicked(id: number) {
    this.api.approvePending(id).subscribe({
      next: () => {
        this.loadPendingDisciplines();
      },
      error: () => {
        this.errorMsg.set("Could not approve this discipline.");
      }
    });
  }
}
