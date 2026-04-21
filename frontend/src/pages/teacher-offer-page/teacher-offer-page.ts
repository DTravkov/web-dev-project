import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { IPendingTeacher } from '../../model/i-pending-teacher';
import { ApiService } from '../../services/api-service';
import { AuthService } from '../../services/auth-service';

@Component({
  selector: 'app-teacher-offer-page',
  imports: [FormsModule, RouterLink],
  templateUrl: './teacher-offer-page.html',
  styleUrl: './teacher-offer-page.css',
})
export class TeacherOfferPage {
  api = inject(ApiService);
  auth = inject(AuthService);
  disciplines = this.api.getDisciplineList();
  teacherName = signal('');
  teacherSurname = signal('');
  teacherDiscipline = signal('');
  pendingTeachers = signal<IPendingTeacher[]>([]);
  statusMsg = signal<string | null>(null);

  constructor() {
    this.loadPendingTeachers();
  }

  clearStatus() {
    this.statusMsg.set(null);
  }

  loadPendingTeachers() {
    if (!this.auth.isLoggedIn()) {
      this.pendingTeachers.set([]);
      return;
    }

    const request = this.auth.isManager() ? this.api.getAllPendingTeachers() : this.api.getMyPendingTeachers();

    request.subscribe({
      next: (response) => {
        this.pendingTeachers.set(response);
      },
      error: () => {
        this.pendingTeachers.set([]);
      }
    });
  }

  onSubmitClicked() {
    const name = this.teacherName().trim();
    const surname = this.teacherSurname().trim();
    const disciplineValue = this.teacherDiscipline();
    const disciplineId = disciplineValue === '' ? null : Number(disciplineValue);

    if (!name || !surname) {
      this.statusMsg.set('Please enter both teacher name and surname.');
      return;
    }

    this.api.postPendingTeacher(name, surname, disciplineId).subscribe({
      next: () => {
        this.statusMsg.set('Teacher offer sent successfully!');
        this.teacherName.set('');
        this.teacherSurname.set('');
        this.teacherDiscipline.set('');
        this.loadPendingTeachers();
      },
      error: (err) => {
        if (err.status === 400) {
          this.statusMsg.set('Teacher with these details already exists or is already pending.');
          return;
        }
        this.statusMsg.set('Could not send your teacher offer.');
      }
    });
  }

  onApproveClicked(id: number) {
    this.api.approvePendingTeacher(id).subscribe({
      next: () => {
        this.loadPendingTeachers();
      },
      error: () => {
        this.statusMsg.set('Could not approve this teacher.');
      }
    });
  }
}
