import { Component, inject, input, OnInit, signal } from '@angular/core';
import { IComment } from '../../model/i-comment';
import { ApiService } from '../../services/api-service';
import { ActivatedRoute } from '@angular/router';
import { IDiscipline } from '../../model/i-discipline';
import { FormsModule } from '@angular/forms';
import { timer } from 'rxjs';

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

  errorMsg = signal<string | null>(null);
  errorTimer = timer(3000);

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
    if (this.currentComment().trim() === "" || this.currentComment().length < 5) {
      console.error("The comment is too short.");
      this.errorMsg.set("The comment is too short.");
      this.errorTimer.subscribe(() => this.errorMsg.set(""));
      return;
    }
    if (this.currentRating() <= 0 || this.currentRating() >= 5) {
      this.errorMsg.set("The rating must be in range (1-5).");
      this.errorTimer.subscribe(() => this.errorMsg.set(""));
      return;
    }
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
