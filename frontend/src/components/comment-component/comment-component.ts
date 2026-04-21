import { Component, input, output } from '@angular/core';
import { RouterLink } from '@angular/router';
import { IComment } from '../../model/i-comment';

@Component({
  selector: 'app-comment-component',
  imports: [RouterLink],
  templateUrl: './comment-component.html',
  styleUrl: './comment-component.css',
})
export class CommentComponent {
  commentData = input.required<IComment>();
  likeEvent = output<number>();
  dislikeEvent = output<number>();
  onLikeClicked() {
    this.likeEvent.emit(this.commentData().id);
  }
  onDislikeClicked() {
    this.dislikeEvent.emit(this.commentData().id);
  }
}
