import { Component, computed, inject, OnInit, Signal, signal, WritableSignal } from '@angular/core';
import { ButtonComponent } from '../button-component/button-component';
import { IButton } from '../../model/i-button';
import { ApiService } from '../../services/api-service';
import { IDiscipline } from '../../model/i-discipline';
import { Router } from '@angular/router';

@Component({
  selector: 'app-discipline-list-component',
  imports: [ButtonComponent],
  templateUrl: './discipline-list-component.html',
  styleUrl: './discipline-list-component.css',
})
export class DisciplineListComponent implements OnInit {
  private api = inject(ApiService);
  private disciplineMap = this.api.getDisciplineMap();
  private router = inject(Router);
  buttons = computed(() => {
    console.log(this.disciplineMap());
    return Object.values(this.disciplineMap())
  });

  ngOnInit(): void {
    this.disciplineMap = this.api.getDisciplineMap();
  }

  onButtonClicked(id: number) {
    const trueId = this.disciplineMap()[id].id;
    this.router.navigate(['/disciplines/', trueId.toString()]);
  }


}
