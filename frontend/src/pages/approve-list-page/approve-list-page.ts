import { Component, computed, inject, signal } from '@angular/core';
import { ApiService } from '../../services/api-service';
import { Router } from '@angular/router';
import { IPendingDiscipline } from '../../model/i-pending-discipline';
import { ButtonComponent } from '../../components/button-component/button-component';
import { AuthService } from '../../services/auth-service';

@Component({
  selector: 'app-approve-list-page',
  imports: [ButtonComponent],
  templateUrl: './approve-list-page.html',
  styleUrl: './approve-list-page.css',
})
export class ApproveListPage {
  private api = inject(ApiService);

  buttons = signal<IPendingDiscipline[]>([]);

  ngOnInit(): void {
    this.refreshPending();
  }

  onButtonClicked(id: number) {
    this.api.approvePending(id).subscribe({
      next: (value) => this.refreshPending()
    });
  }

  refreshPending() {
    this.api.getPending().subscribe({
      next: (list) => this.buttons.set(list)
    });
  }
}
