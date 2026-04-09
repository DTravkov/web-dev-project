import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-button-component',
  imports: [],
  templateUrl: './button-component.html',
  styleUrl: './button-component.css',
})
export class ButtonComponent {
  id = input.required<number>();
  action = input.required<string>();
  clickedEvent = output<number>();
  onClicked() {
    const id = this.id();
    this.clickedEvent.emit(id);
  }

}
