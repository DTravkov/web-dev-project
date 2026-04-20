import { Component, input } from '@angular/core';
import { IProfile } from '../../model/i-profile';

@Component({
  selector: 'app-profile-page',
  imports: [],
  templateUrl: './profile-page.html',
  styleUrl: './profile-page.css',
})
export class ProfilePage {
  profile = input.required<IProfile>();

}
