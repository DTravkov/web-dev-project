import { Component, computed, inject } from '@angular/core';
import { ApiService } from '../../services/api-service';
import { Router } from '@angular/router';
import { ButtonComponent } from '../../components/button-component/button-component';

@Component({
  selector: 'app-professor-list-page',
  imports: [ButtonComponent],
  templateUrl: './professor-list-page.html',
  styleUrl: './professor-list-page.css',
})
export class ProfessorListPage {
  private api = inject(ApiService);
  private teacherMap = this.api.getTeacherMap();
  private router = inject(Router);
  buttons = computed(() => {
    return Object.values(this.teacherMap())
  });

  onButtonClicked(id: number) {
    const trueId = this.teacherMap()[id].id;
    this.router.navigate(['/professors/', trueId.toString()]);
  }
}

