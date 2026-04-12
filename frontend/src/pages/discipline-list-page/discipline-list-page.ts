import { Component, computed, inject, OnInit, Signal, signal, WritableSignal } from '@angular/core';
import { ButtonComponent } from '../../components/button-component/button-component';
import { ApiService } from '../../services/api-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-discipline-list-page',
  imports: [ButtonComponent],
  templateUrl: './discipline-list-page.html',
  styleUrl: './discipline-list-page.css',
})
export class DisciplineListPage {
  private api = inject(ApiService);
  private disciplineMap = this.api.getDisciplineMap();
  private router = inject(Router);
  buttons = computed(() => {
    return Object.values(this.disciplineMap())
  });

  onButtonClicked(id: number) {
    const trueId = this.disciplineMap()[id].id;
    this.router.navigate(['/disciplines/', trueId.toString()]);
  }


}
