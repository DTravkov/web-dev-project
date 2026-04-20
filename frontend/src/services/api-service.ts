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
      this.refreshDisciplines();
    }
    return this.disciplineList;
  }

  getDisciplineMap() {
    this.getDisciplineList();
    return this.disciplineMap;
  }

  refreshDisciplines() {
    this.getDisciplines().subscribe({
      next: (list) => {
        this.disciplineList.set(list);
      },
      error: (err) => {
        console.log(err);
      }
    })
  }

  getDisciplines() {
    return this.http.get<IDiscipline[]>('/api/disciplines');
  }
  getDiscipline(id: number) {
    return this.http.get<IDiscipline>('/api/disciplines/' + id.toString());
  }

  getPending() {
    return this.http.get<IPendingDiscipline[]>('/api/pending/');
  }

  getCommentsByDisciplineId(id: number) {
    return this.http.get<IComment[]>('/api/disciplines/' + id.toString() + "/comments/");
  }

  getComment(id: number) {
    return this.http.get<IComment>('/api/comments/' + id.toString() + "/comment_detail/", { headers: { "Content-Type": "application/json" } });
  }

  postComment(id: number, content: string, rating: number) {
    
    return this.http.post('/api/comments/', { discipline: id, content: content, rating: rating }, { headers: { "Content-Type": "application/json" } });
  }
  postLikeComment(id: number) {
    return this.http.post('/api/comments/' + id.toString() + "/like/", { discipline: id, }, { headers: { "Content-Type": "application/json" } });
  }
  postDislikeComment(id: number) {
    return this.http.post('/api/comments/' + id.toString() + "/dislike/", { discipline: id, }, { headers: { "Content-Type": "application/json" } });
  }

  postLogout(refresh: string) {
    return this.http.post('/api/comments/', { refresh: refresh }, { headers: { "Content-Type": "application/json" } });
  }

  postPending(name: string) {
    return this.http.post('/api/pending/', { name: name }, { headers: { "Content-Type": "application/json" } });
  }
  postBlacklist(refresh: string) {
    return this.http.post('/api/token/blacklist/', { refresh: refresh }, { headers: { "Content-Type": "application/json" } });
  }
  approvePending(id: number) {
    return this.http.post('/api/pending/' + id.toString() + "/approve/", { headers: { "Content-Type": "application/json" } });
  }
  setActive(id: number) {
    this.activeDiscipline.set(this.disciplineMap()[id]);
  }
}
