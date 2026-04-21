import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api-service';
import { IProfile } from '../../model/i-profile';

@Component({
  selector: 'app-profile-page',
  imports: [RouterLink],
  templateUrl: './profile-page.html',
  styleUrl: './profile-page.css',
})
export class ProfilePage {
  private route = inject(ActivatedRoute);
  private api = inject(ApiService);
  private userId = Number(this.route.snapshot.paramMap.get('id'));

  profile = signal<IProfile | null>(null);
  likes = signal(0)
  dislikes = signal(0)
  errorMsg = signal<string | null>(null);

  constructor() {
    this.loadProfile();
  }

  loadProfile() {
    this.api.getUserProfile(this.userId).subscribe({
      next: (response) => {
        this.profile.set(response);
        for (const c of response.comments!) {
          this.likes.update(value => value + c.likes_count);
          this.dislikes.update(value => value + c.dislikes_count);
          console.log(this.likes())
        }
      },
      error: () => {
        this.errorMsg.set('Could not load this profile.');
      }
    });
  }
}
