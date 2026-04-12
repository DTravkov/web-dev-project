import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { IComment } from '../../model/i-comment';
import { ApiService } from '../../services/api-service';
import { ActivatedRoute } from '@angular/router';
import { IDiscipline } from '../../model/i-discipline';
import { FormsModule } from '@angular/forms';
import { StarRatingComponent } from '../../components/star-rating-component/star-rating-component';
import { CommentComponent } from '../../components/comment-component/comment-component';
import { concatMap, switchMap } from 'rxjs';

@Component({
  selector: 'app-discipline-page',
  imports: [FormsModule, StarRatingComponent, CommentComponent],
  templateUrl: './discipline-page.html',
  styleUrl: './discipline-page.css',
})
export class DisciplinePage implements OnInit {
  private route = inject(ActivatedRoute);
  private api = inject(ApiService);
  private id: number = Number(this.route.snapshot.paramMap.get('id'))!;


  discipline = signal<IDiscipline | null>(null);
  commentsMap = signal<Record<number, IComment>>({});
  commentsArr = computed(() => Object.values(this.commentsMap()))


  currentComment = signal<string>("");
  currentRating = signal<number>(0);

  errorMsg = signal<string | null>(null);

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
    if (this.currentComment().trim() === "" || this.currentComment().length < 3) {
      console.error("The comment is too short.");
      this.errorMsg.set("The comment is too short.");
      return;
    }
    if (this.currentRating() <= 0 || this.currentRating() > 5) {
      this.errorMsg.set("The rating must be in range (1-5).");
      return;
    }
    this.api.postComment(this.discipline()!.id, this.currentComment(), this.currentRating()).subscribe({
      next: (response) => {
        this.fetchComments();
        this.currentComment.set("");
        this.currentRating.set(0);
      },
      error: (err) => {
        console.error('Login failed');
      },
    });
  }
  fetchComments() {
    this.api.getCommentsByDisciplineId(this.id).subscribe({
      next: (arr) => {
        arr = arr.reverse();
        const map: Record<string, IComment> = {};
        for (let i = 0; i < arr.length; i++) {
          if (map[arr[i].id]) continue;
          map[arr[i].id] = arr[i];
        }
        this.commentsMap.set(map);
      },
      error: (err) => {
        console.log(err);
      }
    })
  }


  onLikeClicked(id: number) {
    this.api.postLikeComment(id).pipe(
      concatMap(() => this.api.getComment(id))
    ).subscribe({
      next: (updatedComment) => { this.updateCommentsMap(id, updatedComment) },
      error(err) { console.log(err) }
    });
  }
  onDislikeClicked(id: number) {
    this.api.postDislikeComment(id).pipe(
      concatMap(() => this.api.getComment(id))
    ).subscribe({
      next: (updatedComment) => { console.log(updatedComment.likes_count, updatedComment.dislikes_count); this.updateCommentsMap(id, updatedComment) },
      error(err) { console.log(err) }
    });
  }

  onRatingChanged(value: number) {
    this.clearErrorMsg();
    this.currentRating.set(value);
  }

  clearErrorMsg() {
    this.errorMsg.set(null)
  }

  updateCommentsMap(id: number, comment: IComment) {
    this.commentsMap.update(map => {
      return {
        ...map,
        [id]: comment
      };
    })
  }

}
