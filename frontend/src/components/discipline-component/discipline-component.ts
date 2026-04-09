import { Component, inject, input, OnInit, signal } from '@angular/core';
import { IComment } from '../../model/i-comment';
import { ApiService } from '../../services/api-service';
import { ActivatedRoute } from '@angular/router';
import { IDiscipline } from '../../model/i-discipline';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-discipline-component',
  imports: [FormsModule],
  templateUrl: './discipline-component.html',
  styleUrl: './discipline-component.css',
})
export class DisciplineComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private api = inject(ApiService);
  private id: number = Number(this.route.snapshot.paramMap.get('id'))!;


  discipline = signal<IDiscipline | null>(null);
  comments = signal<IComment[]>([]);

  currentComment = signal<string>("");
  currentRating = signal<number>(0);

  ngOnInit(): void {

    const disciplineFromMap = this.api.getDisciplineMap()()[this.id];
    if (disciplineFromMap) this.discipline.set(disciplineFromMap);
    else {
      this.api.getDiscipline(this.id).subscribe({
        next: (value) => {
          this.discipline.set(value);
        },
        error: (err) => console.log(err)
      });
    }

    this.fetchComments();
  }

  onCommentSubmit() {
    this.api.postComment(this.discipline()!.id, this.currentComment(), this.currentRating()).subscribe({
      next: (response) => {
        this.fetchComments();
      },
      error: (err) => {
        console.error('Login failed');
      },
    });
  }

  fetchComments() {
    this.api.getCommentsByDisciplineId(this.id).subscribe({
      next: (list) => {
        console.log(list)
        this.comments.set(list);
      },
      error: (err) => {
        console.log(err);
      }
    })
  }


}
