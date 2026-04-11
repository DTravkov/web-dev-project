import { HttpClient } from '@angular/common/http';
import { computed, inject, Injectable, signal } from '@angular/core';
import { IDiscipline } from '../model/i-discipline';
import { IComment } from '../model/i-comment';
import { IPendingDiscipline } from '../model/i-pending-discipline';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private http = inject(HttpClient);

  private activeDiscipline = signal<IDiscipline | null>(null);
  private disciplineList = signal<IDiscipline[]>([]);
  private disciplineMap = computed<Record<number, IDiscipline>>(() => {
    let map = {};
    this.disciplineList().forEach(e => {
      map = { ...map, [e.id]: e };
    });
    return map;
  }
  )


  getDisciplineList() {
    if (this.disciplineList().length === 0) {
      this.getDisciplines().subscribe({
        next: (list) => {
          this.disciplineList.set(list);
        },
        error: (err) => {
          console.log(err);
        }
      })
    }
    return this.disciplineList;
  }

  getDisciplineMap() {
    this.getDisciplineList();
    return this.disciplineMap;
  }

  getIsModerator() {
    return this.http.get('http://127.0.0.1:80/api/is-moderator');
  }

  getDisciplines() {
    return this.http.get<IDiscipline[]>('http://127.0.0.1:80/api/disciplines');
  }
  getDiscipline(id: number) {
    return this.http.get<IDiscipline>('http://127.0.0.1:80/api/disciplines/' + id.toString());
  }

  getPending() {
    return this.http.get<IPendingDiscipline[]>('http://127.0.0.1:80/api/pending/');
  }

  getCommentsByDisciplineId(id: number) {
    return this.http.get<IComment[]>('http://127.0.0.1:80/api/disciplines/' + id.toString() + "/comments/");
  }

  postComment(id: number, content: string, rating: number) {
    return this.http.post('http://127.0.0.1:80/api/comments/', { discipline: id, content: content, rating: rating }, { headers: { "Content-Type": "application/json" } });
  }

  postLogout(refresh: string) {
    return this.http.post('http://127.0.0.1:80/api/comments/', { refresh: refresh }, { headers: { "Content-Type": "application/json" } });
  }

  postPending(name: string) {
    return this.http.post('http://127.0.0.1:80/api/pending/', { name: name }, { headers: { "Content-Type": "application/json" } });
  }
  postBlacklist(refresh: string) {
    return this.http.post('http://127.0.0.1:80/api/token/blacklist/', { refresh: refresh }, { headers: { "Content-Type": "application/json" } });
  }
  approvePending(id: number) {
    return this.http.post('http://127.0.0.1:80/api/pending/' + id.toString() + "/approve/", { headers: { "Content-Type": "application/json" } });
  }
  setActive(id: number) {
    this.activeDiscipline.set(this.disciplineMap()[id]);
  }
}
