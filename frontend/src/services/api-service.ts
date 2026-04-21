import { HttpClient } from '@angular/common/http';
import { computed, inject, Injectable, signal } from '@angular/core';
import { IDiscipline } from '../model/i-discipline';
import { IComment } from '../model/i-comment';
import { IPendingDiscipline } from '../model/i-pending-discipline';
import { IPendingTeacher } from '../model/i-pending-teacher';
import { IProfile } from '../model/i-profile';
import { IStats } from '../model/i-stats';
import { ITeacher } from '../model/i-teacher';
import { toSignal } from '@angular/core/rxjs-interop';

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
  private teacherList = signal<ITeacher[]>([]);
  private teacherMap = computed<Record<number, ITeacher>>(() => {
    let map = {};
    this.teacherList().forEach(e => {
      map = { ...map, [e.id]: e };
    });
    return map;
  }
  )

  private statsInner = signal<IStats | null>(null);
  private statsLoaded = false;

  stats = computed(() => {
    if (!this.statsLoaded) {
      this.statsLoaded = true;

      this.getStats().subscribe({
        next: (res) => this.statsInner.set(res),
        error: (err) => console.log(err)
      });
    }

    return this.statsInner();
  });


  getDisciplineList() {
    this.getDisciplines().subscribe({
      next: (list) => {
        this.disciplineList.set(list);
      },
      error: (err) => console.log(err)
    });
    return this.disciplineList;
  }

  getDisciplineMap() {
    this.getDisciplineList();
    return this.disciplineMap;
  }

  getTeacherList() {
    if (this.teacherList().length === 0) {
      this.refreshTeachers();
    }
    return this.teacherList;
  }

  getTeacherMap() {
    this.getTeacherList();
    return this.teacherMap;
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


  refreshTeachers() {
    this.getTeachers().subscribe({
      next: (list) => {
        this.teacherList.set(list);
      },
      error: (err) => {
        console.log(err);
      }
    })
  }
  getTeachers() {
    return this.http.get<ITeacher[]>('http://localhost/api/professors/');
  }
  getMyPending() {
    return this.http.get<IPendingDiscipline[]>('http://localhost/api/pending/mypending/');
  }
  getAllPending() {
    return this.http.get<IPendingDiscipline[]>('http://localhost/api/pending/allpending/');
  }
  getMyPendingTeachers() {
    return this.http.get<IPendingTeacher[]>('http://localhost/api/pending-professors/mypending/');
  }
  getAllPendingTeachers() {
    return this.http.get<IPendingTeacher[]>('http://localhost/api/pending-professors/allpending/');
  }
  getStats() {
    return this.http.get<IStats>('http://localhost/api/stats/');
  }
  getUserProfile(id: number) {
    return this.http.get<IProfile>('http://localhost/api/users/' + id.toString() + '/profile/');
  }
  getDisciplines() {
    return this.http.get<IDiscipline[]>('http://localhost/api/disciplines/');
  }
  getDiscipline(id: number) {
    return this.http.get<IDiscipline>('http://localhost/api/disciplines/' + id.toString());
  }

  getPending() {
    return this.http.get<IPendingDiscipline[]>('http://localhost/api/pending/');
  }

  getCommentsByDisciplineId(id: number) {
    return this.http.get<IComment[]>('http://localhost/api/disciplines/' + id.toString() + "/comments/");
  }

  getComment(id: number) {
    return this.http.get<IComment>('http://localhost/api/comments/' + id.toString() + "/comment_detail/", { headers: { "Content-Type": "application/json" } });
  }

  postComment(id: number, content: string, rating: number, professor: number) {
    return this.http.post(
      'http://localhost/api/comments/',
      { discipline: id, content: content, rating: rating, professor: professor },
      { headers: { "Content-Type": "application/json" } }
    );
  }
  postLikeComment(id: number) {
    return this.http.post('http://localhost/api/comments/' + id.toString() + "/like/", { discipline: id, }, { headers: { "Content-Type": "application/json" } });
  }
  postDislikeComment(id: number) {
    return this.http.post('http://localhost/api/comments/' + id.toString() + "/dislike/", { discipline: id, }, { headers: { "Content-Type": "application/json" } });
  }

  postLogout(refresh: string) {
    return this.http.post('http://localhost/api/comments/', { refresh: refresh }, { headers: { "Content-Type": "application/json" } });
  }

  postPending(name: string) {
    return this.http.post('http://localhost/api/pending/', { name: name }, { headers: { "Content-Type": "application/json" } });
  }
  postPendingTeacher(name: string, surname: string, discipline: number | null) {
    return this.http.post(
      'http://localhost/api/pending-professors/',
      { name, surname, discipline },
      { headers: { "Content-Type": "application/json" } }
    );
  }
  postBlacklist(refresh: string) {
    return this.http.post('http://localhost/api/token/blacklist/', { refresh: refresh }, { headers: { "Content-Type": "application/json" } });
  }
  approvePending(id: number) {
    return this.http.post('http://localhost/api/pending/' + id.toString() + "/approve/", { headers: { "Content-Type": "application/json" } });
  }
  approvePendingTeacher(id: number) {
    return this.http.post('http://localhost/api/pending-professors/' + id.toString() + "/approve/", { headers: { "Content-Type": "application/json" } });
  }
  setActive(id: number) {
    this.activeDiscipline.set(this.disciplineMap()[id]);
  }
}
