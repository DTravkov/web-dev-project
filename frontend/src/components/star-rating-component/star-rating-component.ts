import { Component, computed, input, OnInit, output, signal } from '@angular/core';

@Component({
  selector: 'app-star-rating-component',
  imports: [],
  templateUrl: './star-rating-component.html',
  styleUrl: './star-rating-component.css',
})
export class StarRatingComponent implements OnInit {
  numberOfStars = input.required<number>();
  starArray = signal<number[]>([]);
  clickedCount = signal<number>(0);
  clickedEvent = output<number>();

  ngOnInit(): void {
    this.starArray.update(arr => {
      for (let i = 1; i <= this.numberOfStars(); i++) arr.push(i);
      return arr;
    });
  }


  onClicked(value: number) {
    this.clickedEvent.emit(value);
    this.clickedCount.set(value);
  }
}
